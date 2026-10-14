# Character projects and recovery

[Project index](README.md) · [Source](https://github.com/TF-Minecraft/MusicalInstruments)

The recording studio requires an active character. Each character has its own
project library, selected project, pending takes and editing authority. Switching
characters or leaving finishes the outgoing take using its captured character,
stops private previews and closes studio menus. Delayed menu/dialog responses
check the initiating session; a response from an earlier session cannot edit the
incoming character's project or consume its disc.

The original song author and author account remain on the project. Inheriting a
project grants editing authority without changing that attribution. Published
editions, their content IDs and existing disc metadata remain unchanged, so old
discs keep playing. Ordinary instruments and jukebox playback remain available
without a character provider; creating, editing and recording projects fail
closed when that provider is unavailable.

Publication timestamps in `studio/editions/<account UUID>.log` and the short
publication cooldown remain account-wide. Switching characters or inheriting
another author's project does not reset them. An inherited library may exceed
36 projects; every inherited project remains available, and creating another
project waits until the character has fewer than 36. The library menu shows only
the first 36. Use `/music projects` to list all project IDs and
`/music open <project-id>` to open a project beyond those menu slots.

## Requirements and storage

Build with Java 21 for Paper 1.21.10 and the pinned TLibs 2.6.0 API. The build and
release workflows prepare this dependency through the shared plugin installer.
They also install the actual TLibs 2.3.0 release as an isolated compatibility test
fixture; it is not packaged into the runtime jar.
TLibs/RPCharacters are optional load-order dependencies: capability probes isolate
new calls from older installations. Without the estate API, holdings stay with
their character until that integration becomes available.

Paths below are relative to `plugins/MusicalInstruments/`:

- `studio/projects/<account UUID>/` contains retained legacy source projects,
  their selected pointer and optional library cache. The new runtime does not
  edit or use this account namespace.
- `studio/character-projects/<character UUID>/<project UUID>.yml` contains editable
  projects with separate `owner-account` and `owner-character` authority fields.
  `selected` holds the chosen project ID and `library.index` is a rebuildable cache.
- `studio/songs/<edition UUID>.yml` contains immutable published recordings.
- `studio/ownership/migration/<account UUID>.xml` records the reviewed recipient,
  source/target hashes, original payloads, completion and held records.
- `studio/ownership/estates/<death UUID>.xml` records exact estate decisions,
  full source/recipient references, expected payloads and cumulative move receipts.
- `studio/ownership/backups/<SHA-256>.yml` contains immutable original documents.

Unknown project properties—including nested maps and explicit null values—survive
migration and later saves. Extension metadata from a removed track or discarded
pending take stays in retained metadata without becoming playable music.
Unreadable files remain available for staff recovery; absence from the playable
library does not mean the file was deleted.

## Legacy migration

Migration runs after stores are ready, on ownership operations and at the hourly
reconciliation. It waits until RPCharacters reports reviewed legacy heirs ready.
Each account's legacy projects go to exactly its reviewed heir, even if that heir
is dead. The character's estate then determines any subsequent inheritance.
There is no active-character, last-played or username fallback.

A journal inventories the account library and selected pointer before publishing
its character copies. Immutable backups, checked writes and stable IDs allow
interrupted runs to resume the same planned recipient. Original account files
remain retained and inert. A recipient with a selected project keeps that
selection; migration supplies the legacy selection only when none is present.
Unsupported, corrupt or identity-mismatched records are held. A conflicting
recipient project is not overwritten.

Inspect journals and unassigned legacy paths from the source checkout:

```sh
python3 tools/studio-ownership.py \
  --studio /path/to/plugins/MusicalInstruments/studio --kind migration
```

The JSON report lists held files, publication states, conflicts and character
projects created after the plan. `unassigned_legacy` lists legacy paths with no
migration journal yet; incomplete journals appear under `journals`.
Do not edit a source archive to choose an heir; fix the reviewed mapping before
its first plan, or recover a previously planned transfer by hand.

## Estate transfers

The `studio` participant reports editable project IDs and counts through the
existing estate screens. It moves property to the estate's character recipient;
WAITING/FROZEN property stays with the testator. Death, owner reference, exact
revision and current decision are checked before publication and source removal.
The source and recipient must finish pending studio saves before transfer starts.

A planned destination is written and acknowledged before removing the source.
Repeated settlement reports the same cumulative moved IDs. Completed projects
are receipts and are not redirected automatically when staff later change a
recipient. A newer decision can replace an untouched plan. If any output was
published under an older decision, that partial transfer stays BLOCKED for staff
recovery. Affected libraries refuse conflicting edits while an intent is pending.
Every entry, including historical completed receipts, validates its captured
death, full source/recipient references and integral revision. A previously
transferred project that reappears at its source blocks every revision, including
WAITING/FROZEN, while preserving both files and receipts for staff review.
Before/after YAML may differ only in the project authority fields: titles, tracks,
authorship and unknown nullable metadata remain unchanged even when a modified
plan carries recomputed hashes. Transient disk failures return RETRY; conflicting
contents return BLOCKED.

Inspect an estate's files before staff retry or waive a blocked participant:

```sh
python3 tools/studio-ownership.py \
  --studio /path/to/plugins/MusicalInstruments/studio --kind estates
```

Use the existing `/estate show`, `/estate retry` and `/estate waive` procedures
only after the reported cause is understood. Do not delete a journal to force
retry: it contains the original ownership and transfer receipts.

## Offline rollback

Coordinate with the server deployment owner and stop Paper cleanly before apply.
Archive the current studio directory first; this retains new projects and edits
that restoring an old snapshot would otherwise discard. Preview estates first,
then legacy migration, with the inspection commands above.

The offline tool requires Python 3 and PyYAML (`python3-yaml` on Ubuntu). Its safe
loader rejects duplicate YAML fields, and duplicate XML keys are also rejected.
It preflights every entry in a journal before restoring any project, checking
full references, captured decisions, paths, hashes and the authority-only
before/after transformation. Current source/destination contents must still
match their planned hashes. Apply requires a new recovery directory:

```sh
python3 tools/studio-ownership.py \
  --studio /path/to/plugins/MusicalInstruments/studio --kind estates --apply --backup /path/to/new-estate-recovery
python3 tools/studio-ownership.py \
  --studio /path/to/plugins/MusicalInstruments/studio --kind migration --apply --backup /path/to/new-migration-recovery
```

It preserves the current journal and every current project copy in the new
recovery directory before the first restore or removal. It restores exact
original source bytes, removes only the unchanged planned copy, and archives
fully restored journals under `ownership/rolled-back/`.
Changed or missing copies produce conflicts and remain preserved for staff.
Projects created after migration are listed and retained; an older jar cannot
read their character namespace, so staff must reconcile them separately.
Published editions and account quota logs are never rolled back by this tool.

After reconciling conflicts, restore the matching old jar. Re-upgrading runs a
new reviewed plan for journals that were fully rolled back. Keep archived
current data and old receipts; never make both legacy and character namespaces
simultaneously authoritative.

## Verification and limits

Prepare both pinned dependency manifests using the
[shared plugin installer](../TLibs/README.md#builds-and-releases), then run
from the source checkout. The fixture manifest is
`.github/compatibility/tlibs-2.3.xml` and should use a separate
`.build/legacy-plugin-dependencies.json` lock file.

```sh
tfmc-mvn -o -B clean verify
python3 -m unittest discover -s tools -p 'test_*.py'
```

Tests cover two characters on one account; noncurrent outgoing-session cleanup;
late save routing; publication quota isolation; exact published bytes; unknown
fields through migration, editing and restart; inherited overflow; repeated
migration/estate settlement; unavailable identity; and failures before/after
destination publication and source removal. Stale revisions hold partially
published files instead of completing an obsolete handover.

Ownership transfers operate only on durable project files. Publishing or copying
a physical disc still crosses Paper inventory/world persistence boundaries;
these tests do not establish arbitrary-crash exactly-once item delivery. A source
archive and journal must be preserved for staff recovery when a disk failure
leaves an ambiguous publication.
