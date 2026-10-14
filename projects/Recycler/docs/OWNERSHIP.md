# Character returns and recovery

[Recycler](../README.md) · [Source](https://github.com/TF-Minecraft/Recycler)

A living current character owns each deposited stack. Menus retain the initiating
session and reject later sessions, including a later session of the same
character. A switch or departure closes the outgoing menu and queues its item
for that recorded character. Joining Minecraft alone cannot deliver another
character's returns. Matching character start, normal close/take-out or
`/recycler escrow return <online player>` can deliver that living character's
pending queue.

Refunds use free storage slots and split oversized stacks into batches up to the
material's stack size. Full inventory leaves the remainder queued; refunds do
not drop overflow into the world. New deposits use exact Paper item bytes,
including names, enchantments and persistent metadata. Providers, recovery rates,
permissions and existing account policies keep their existing behavior.

## Storage and effects

Paths are relative to `plugins/Recycler/data/`:

- `character-returns/<character UUID>/<operation UUID>.json`: full account and
  character owner, stable operation ID, item bytes or retained legacy item map,
  remaining amount and effect evidence. Unknown nested properties and explicit
  nulls survive state changes and restart.
- `ownership/migration/<operation UUID>.json`: fixed reviewed legacy recipient,
  source/destination paths, exact original/output bytes and hashes, phase.
- `ownership/estates/<death UUID>.json`: full testator/recipient references, exact
  decisions/revisions, source/output expectations and cumulative move receipts.
- `ownership/backups/<SHA-256>.bin`: immutable original documents.
- `ownership/unassigned/`: retained evidence for unrecognized legacy filenames.
- `escrow/` and `pending_returns/`: retained legacy sources, inert for this
  version. Older JARs deliver directly from these account filenames.

Inventory intent is written and synced before an effect. `depositing` records the
input slot, exact stack and initiating session before removal. Only successful
removal and a Paper inventory save request allow the row to become `escrow`.
A GUI refund becomes `pending`. Each free-slot delivery first becomes
`delivering` with its slot, batch, session and planned remainder. After the
inventory effect and save request, its acknowledged remainder is `pending` or
its receipt is `delivered`. Confirmed input becomes `consumed`, retaining planned
output bytes. A cancelled pre-effect deposit keeps an inert `cancelled` receipt.

On restart, committed `escrow` becomes `pending`. `depositing` and `delivering`
remain ambiguous and never automatically replay. A synchronous failure before
intent publication preserves inventory; a failure after an effect retains its
intent. Each interrupted refund effect addresses at most one free-slot batch,
while unattempted remainder stays in the same queue record.

Paper player data, queue files and world entities are separate stores. A returned
`saveData()` call is not a transaction or a filesystem durability proof for all
of them. These procedures do **not** promise arbitrary-crash exactly-once item
delivery. Inspect ambiguous records against the character's body/inventory and
record a staff recovery decision before changing their state or restoring items.
Do not delete evidence or mark an intent pending merely because the menu closed.

Confirmed recycling keeps the existing staggered world-output behavior. Input
is consumed before all scheduled drops finish. A crash can lose unspawned
outputs; dropped entities and player pickup also have their own persistence.
The consumed receipt retains the planned outputs for inspection, and startup
never blindly respawns them. This ownership migration does not solve that
existing world-output crash boundary.

## Reviewed legacy migration

Migration waits for `Characters.legacyHeirsReady` and uses only
`Characters.legacyHeir(account)`. It never chooses the current, last-played or a
living replacement character. A dead reviewed heir first receives its queue;
its estate then controls subsequent inheritance. A missing heir leaves the
original file unmapped. Existing fixed plans retain their separately recorded full recipient reference
on restart.

Each legacy file gets its own deterministic operation ID. Multiple pending files
for an account remain separate holdings. Valid legacy pending maps become queued
returns with their unknown fields intact. Legacy escrow becomes `held`: its old
format contains no intent proving inventory removal completed. Malformed item
maps retain raw bytes in a held, character-owned envelope. Unrecognized account
filenames stay unassigned with source evidence. Changed/corrupt plans and UUID
conflicts refuse publication instead of overwriting data.

TLibs 2.6.0 is the pinned build API. Isolated probes make older installations fail
ownership closed, without resolving legacy property through an active account.
CI and compatibility tests also load the actual TLibs 2.3.0 release separately.

## Estates

The `recycler` participant reports durable queued operation IDs, including
unloadable item payloads. It moves queued ownership only, without giving items.
Source and recipient sessions must be idle; inheritance has no acquisition cap.
WAITING/FROZEN rows stay with their testator, and earlier moved IDs remain
cumulative receipts. Ambiguous inventory effects block settlement for staff.

Each plan records full from/to references, death, an integral revision and the
exact decision. Completed receipts validate their captured decision envelope
independently of newer revisions. A moved operation that reappears at its old
owner blocks every revision, including WAITING/FROZEN; preserve both copies and
receipts for staff reconciliation. Current
estate guards are checked before each destination publication and source
removal. A newer decision can replace an untouched plan. A stale partially
published transfer stays BLOCKED for recovery; completed rows are receipts and
are never automatically redirected. Affected owners cannot edit a pending
transfer. Disk failures return RETRY; conflicting state returns BLOCKED.

## Inspection and offline rollback

`/recycler escrow list` shows character/account references, operation IDs, states,
held documents and retained legacy paths. Account-name return affects only the
online player's current living character and leaves full-inventory/held rows
queued. For a complete disk report, run from the source checkout:

```sh
python3 tools/recycler-ownership.py --data /path/to/plugins/Recycler/data --kind estates
python3 tools/recycler-ownership.py --data /path/to/plugins/Recycler/data --kind migration
```

Coordinate a separate deployment owner and stop Paper cleanly before apply.
Archive the entire current Recycler data directory and matching character/body
records first. Roll back estates before migration, using a new recovery folder
for each apply:

```sh
python3 tools/recycler-ownership.py --data /path/to/plugins/Recycler/data --kind estates --apply --backup /path/to/new-estate-recovery
python3 tools/recycler-ownership.py --data /path/to/plugins/Recycler/data --kind migration --apply --backup /path/to/new-migration-recovery
```

Chained estates can require more than one estates pass. Repeat with a new recovery
folder while another pass archives further journals; if no progress is possible,
preserve the remaining evidence for manual reconciliation before migration.

The tool preflights every record in a journal before restoring any of its rows.
It checks paths, full references, captured decisions and planned hashes. It preserves current
bytes, restores exact original documents only if planned copies remain unchanged,
and archives fully restored journals under `ownership/rolled-back/`. Changed or
missing previously published copies remain conflicts. An untouched `planned`
migration with its original legacy source intact can roll back without a
character copy. A migration referenced by a live estate journal remains a
conflict until that estate is safely rolled back; unreadable estate evidence
also blocks migration rollback. New character queues and inventory effects
need manual reconciliation: an old JAR cannot read the character namespace, and
restoring a whole old snapshot would discard later progress. Do not restore a
queued item that has already been delivered or consumed. Retain all recovery
images and receipts; never make old and new queues authoritative together.

If a live migration journal's retained legacy file is missing, deposits,
refunds, deliveries and restart recovery are held, and the tool refuses
migration rollback. Estate settlement and other legacy migrations can continue;
follow the operation ID through estate receipts to its current character copy.
After confirming that no older JAR delivered it, restore its exact bytes from
`ownership/backups/<before-hash>.bin`. If an older JAR did deliver it, stop Paper,
archive the current copy and its receipts, record that delivery and set any
undelivered character copy to `cancelled` with a reason before restoring the
legacy bytes. Reconcile already delivered copies manually. The restored legacy
file is inert in this version and must stay outside the old queue on downgrade.
The backup alone cannot prove that another delivery is safe.

If apply fails after restoring some records, the report's `applied` paths name
the completed actions alongside the original error. Preserve the backup and
live journal for reconciliation; a partial apply does not prove rollback completed.

Before starting any older Recycler JAR, move every `escrow/` and
`pending_returns/` file whose migration journal was not archived under
`ownership/rolled-back/migration/` out of `data/` into a separate legacy holding
folder outside `data/`. Keep it separate from the tool's verified backup, which
holds current copies only for restored records, and from the complete pre-apply
archive. A conflicting journal's tool backup may contain only its journal.
Match each journal's `source` path to its legacy file; a missing or conflicting
journal does not prove rollback succeeded. Older JARs move escrow into the old
pending queue, then deliver and delete those files when the account joins. Leaving
retained sources there can duplicate items already delivered, consumed or
inherited. Restore a legacy file to the old queue only after confirming its
character return was never delivered or consumed, and its migration and any
estate moves were safely rolled back. Keep unresolved files outside both
authoritative queues for manual review.

Before starting this version again after a partial rollback, return each held
legacy file unchanged to its journal's `source` path.

## Verification

Prepare pinned providers through the shared plugin installer, including the
isolated `.github/compatibility/tlibs-2.3.xml` fixture with its separate lock.
Then run from the source checkout:

```sh
tfmc-mvn -o -B clean verify
python3 -m unittest discover -s tools -p 'test_*.py'
```

Tests exercise character/session isolation, outgoing cleanup, exact item metadata,
unknown/null preservation after normal writes/restart, full inventory and batch
remainders, unavailable/dead identity, reviewed mappings, corruption and fixed
recipients, interrupted fanout, exact estate guards, inventory intent failure
cuts and guarded rollback. Paper `saveData` is an explicit mocked boundary in
unit fixtures because MockBukkit does not implement it; runtime player/world
persistence remains the separate boundary described above.
