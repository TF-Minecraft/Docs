# PostgreSQL storage and migration

All site records use PostgreSQL 17: accounts, Discord/Microsoft links, codes and sessions, skins, drinks,
Characters, Patreon, LuckPerms snapshots, Chronicle, Ledger and staff tools. `DATABASE_URL` is required at
startup. CoreProtect remains an external SQLite database opened read-only. PNGs, uploaded assets and map
history files remain on disk.

Source: [database package](https://github.com/TF-Minecraft/ProvinceSystem/tree/main/backend/src/database),
[copy tool](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/backend/src/scripts/tools/copy_province_db.py).
See [previews and deploys](../../DEPLOY.md) for host paths and Actions, and
[Database Studio](database-studio.md) for its separate restricted login.

## Runtime and configuration

Each site's existing `pgvector/pgvector:pg17` Compose `db` service stores site records alongside Precedent and
patch notes. The named PostgreSQL volume and asset mounts are separate persistence boundaries; copying
`backend/src/data/` does not copy site records. Main and Dev use separate databases and volumes.

| Setting | Purpose |
| --- | --- |
| `DATABASE_URL` | Required application connection to this site's PostgreSQL database |
| `DATABASE_STUDIO_URL` | Separate restricted login to the same database; absent configuration returns 503 in Studio |
| `DATABASE_POOL_MIN_SIZE` | Application pool minimum, default 1 |
| `DATABASE_POOL_MAX_SIZE` | Application pool maximum, default 10; previews use 3 |
| `TEST_DATABASE_URL` | Isolated test server where the login can create databases; never the serving database |

Keep connection strings in protected environment files. Do not print them in logs, Actions summaries or
command arguments. The host's Dev `environment: !override` requires its private override to include the
Studio connection; adding it only to the base Compose file is insufficient.

The native connection context borrows one pooled connection for a transaction, committing on success and
rolling back on error. Rows are dictionaries. UTC timestamps, JSONB, booleans and identity columns use their
PostgreSQL types; timestamp serialization and public JSON formats stay compatible with callers. Session
settings bound queries and locks. Domain advisory locks coordinate checks that span multiple rows or the
absence of a row; file guards coordinate wardrobe and map assets across workers.

## Schema migrations

Ordered SQL files in `backend/src/database/migrations/` are recorded with checksums in `schema_migrations`.
Startup applies pending migrations under a database advisory lock and then seeds required singleton rows.
Edited or reordered applied migrations are refused. Native deployment and startup retain verbatim SQL files
in the private data mount's `postgres-migrations/`. When restoring older compatible native code, the migrator
uses checksum-verified retained definitions only for newer versions already applied to that database; it
never applies a newer retained file absent from the selected code. Missing or changed definitions still
refuse startup. Add a new numbered migration for a schema change;
do not edit an applied file or restore the removed SQLite startup upgrader. During the rollback window,
a schema change must also preserve the reviewed import/export contract and include compatible tool updates
and round-trip proof. The one-off copier refuses unexpected schema drift rather than exporting incomplete
rows; defer a schema change if its rollback representation has not been verified.

The one-off copier migrates **without seeds**, because its target site tables must be empty. Precedent and
patch-note migrations remain separate and retain their existing data. Their active PostgreSQL driver
dependencies remain required.

## Per-site cutover

Use **Actions → Deploy** and the reviewed host tooling. A merge to `main` deploys Dev after Build passes.
Main/www changes only through an explicit manual `www` deployment; a Dev cutover does not migrate Main.

Before a site's first native deployment:

1. Install the merged `site-deploy`, `ps-compose` and `ps-preview` host scripts. Preserve private Compose
   overrides and back them up before editing.
2. Keep the existing PostgreSQL database/volume and owner URL. Configure a generated separate
   `DATABASE_STUDIO_URL` for that same database. Do not pass the owner connection to Studio or preview images.
3. Verify the SQLite source and exercise a copy and reverse export on an isolated PostgreSQL target.
   Preserve the report privately; report counts and checksums rather than player rows or tokens.
4. Deploy through Actions. The target backend image is built before the forward downtime. The host stops
   the backend, takes a full custom PostgreSQL dump and final consistent SQLite backup, and runs
   `src.database.operations prepare` from the reviewed target image before normal seeded startup.
5. Provision Studio using the administrator connection. The reviewed deployment operation explicitly
   restricts PUBLIC large-object constructor access while preserving owner/direct grants, then creates or
   refreshes the restricted login. Start the backend only after copy and grant verification succeed.
6. Check API/UI health, database identity, row/hash verification, identities, Studio restrictions and the
   integrations appropriate to that site.

The copy validates all 61 site tables before target row writes, imports and verifies counts/canonical
hashes in a transaction, and preserves identity high-water marks, including deleted SQLite IDs. It archives
retired columns/tables with their DDL. Unrelated Precedent and patch-note tables are preserved.

The private `data/.postgres-authority.json` records the verified target's name and migration history,
source snapshot hash and table checks. Normal deployments validate that identity and migrate without
recopying stale SQLite. If copy committed before marker publication failed, a retry adopts the target only
after exact source verification. The first copy attempt is recorded before import, so if legacy code resumes
and accepts more SQLite writes, retry can restore those writes against its recorded PostgreSQL baseline.
Inconsistent untracked nonempty targets are refused, never cleared.

`/home/tfmc/.site-deployed-<site>` separately records the last healthy revision. Git HEAD can already point
at a target whose build or cutover was interrupted; it is not sufficient evidence of deployment success.
A private `.site-images-<site>.json` Compose overlay selects immutable tags for both services. Cached builds
and running-image verification bind successful deployment to that exact revision, even after interruption.

## Standalone copy and verification

These commands are for an isolated rehearsal or an explicitly stopped site. Run from `backend/` with its
reviewed dependencies and `DATABASE_URL` supplied privately. Stop all writers before either direction.

```bash
python -m src.scripts.tools.copy_province_db to-postgres \
  --sqlite /private/province.snapshot.db --archive-legacy /private/legacy-archive
python -m src.scripts.tools.copy_province_db to-postgres \
  --sqlite /private/province.snapshot.db --verify-only
python -m src.scripts.tools.copy_province_db to-sqlite --sqlite /private/province.rollback.db
```

The source SQLite file is opened read-only with integrity and foreign-key checks. Import requires empty
site tables. `--verify-only` changes no rows; compare with the frozen source before opening the site to
writes. After PostgreSQL accepts new writes, that old SQLite snapshot is no longer an equality baseline.
Reverse export reads a consistent PostgreSQL snapshot and publishes a new mode-0600 SQLite file only after
verification. It refuses an existing destination.

## Backups and rollback window

Routine native deployment backups are private custom PostgreSQL dumps in the site's `deploy-backups/`,
published from a `.part` file after `pg_dump` succeeds; the newest 10 are retained. These full dumps include
Precedent and patch notes. Restoring one is a separate stopped-site database restore, not a code-only rollback.

Keep the original `province.db`, consistent cutover backups, `data/migration-rollback/` snapshots and legacy
archives, and the one-off copier plus frozen `legacy_sqlite.sql` for **at least 30 days** after cutover. They
are outside newest-ten PostgreSQL pruning. Remove them only after the rollback window closes and retention
is explicitly reviewed. The frozen SQLite schema is an offline rollback resource, not a runtime migration.

When returning to legacy code, `site-deploy` stops the backend and uses the retained native tool to export
and verify current PostgreSQL rows before atomically replacing the serving SQLite file. This includes
writes accepted since cutover and during a failed target's health-check window. Original snapshots and each
reverse export remain retained. If export fails, the backend stays stopped; do not start legacy code against
the old SQLite copy.

The private `data/.postgres-rollback-transition.json` records SQLite authority and the immutable, verified
export baseline before legacy code starts. If that legacy release accepts writes and then fails health,
recovery stops it, snapshots SQLite and imports its accepted writes back only after PostgreSQL exactly
matches a recorded baseline, including all identity counters. All 61 site tables are locked and replaced
in one transaction; unrelated tables remain untouched and outside foreign keys refuse replacement.
Snapshots and import attempts remain recorded so a retry after commit but before marker publication can
verify and continue. Unexpected PostgreSQL writes are refused instead of overwritten.

A rollback between native revisions keeps PostgreSQL data and uses the retained, checksum-verified SQL
definitions described above. These must be compatible with the previous application release; retaining a
file does not make a destructive schema change compatible. No rollback restores a full dump automatically.

## Preview provisioning

After Dev's verified cutover, explicitly run the trusted Dev administrator setup:

```bash
sudo -n -u tfmc /usr/local/sbin/ps-compose dev exec -T backend \
  python3 -m src.database.preview setup
```

This removes PUBLIC database CONNECT while retaining database-owner access and existing direct grants.
Each preview owner and Studio login then receives CONNECT only to its own database. Run this on Dev's
cluster; Main's separate cluster is unchanged. After Dev and this isolation setup pass, set the repository
variable `NATIVE_POSTGRES_PREVIEWS_READY=true` for a controlled Preview workflow run on a reviewed native
branch. Verify creation, redeployment and teardown, including removal of its database and roles. Keep the
variable enabled only if that lifecycle passes; disable it again on any failure.

The trusted controller creates the schema under the preview owner, clones only site-table data, scrubs
credentials and validates Studio before starting branch images. Its credentials stay inside trusted Dev
tooling. Failed creation, redeploy, expiry, branch deletion and orphan cleanup retain their metadata until
the marked database and roles have been removed. Detailed environment, networking and lifecycle behavior
is in [DEPLOY.md](../../DEPLOY.md#branch-previews).

## Tests and API smokes

Install `backend/requirements.txt` and `backend/requirements-dev.txt`. Use an isolated PostgreSQL 17 test
server with a superuser/CREATEDB login. Pytest creates its own database, applies migrations and resets touched
tables between tests; it drops the database on completion. PostgreSQL tests skip locally without
`TEST_DATABASE_URL` and fail in CI if it is absent. From the source checkout root:

```bash
cd backend
python -m pytest -q
python scripts/character_session_smoke.py
python scripts/character_ingest_smoke.py
python scripts/creation_catalog_smoke.py
python scripts/rpc_player_meta_smoke.py
python scripts/skins_e2e_smoke.py
python scripts/lore_items_smoke.py
```

Each standalone smoke requires `TEST_DATABASE_URL`, creates a random disposable database and temporary asset
directories, and cleans them up on exit. It overrides `DATABASE_URL` for that test run. These API smokes
exercise code/session, upload and plugin flows; renderer and live bot/Minecraft integration checks remain
separate.
