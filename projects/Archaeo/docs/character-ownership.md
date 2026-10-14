# Character ownership and recovery

[Project index](../README.md)

Archaeo requires TLibs. Its build pins TLibs 2.6.0 alongside the shared Java 21 /
Paper 1.21.10 baseline. RPCharacters supplies character identity, reviewed legacy
heirs and estate decisions. Without a current identity, character actions fail
closed. Capability probes isolate legacy-heir and estate integrations: older
TLibs can load core character handling, while unavailable migration or estate
capabilities leave unresolved property held.

## Authority and sessions

Site directors, excavator rosters, worker pages, prospect samples and confirmations
use character UUIDs with full account/character references. Bukkit account UUIDs
route online players; a matching account alone grants no site rights. `created-by`,
find recovery attribution and interpretation authors remain account audit records.
Existing prospect/tool warning cooldowns and the shared workday budget retain
their existing scope.

The default one-open-excavation limit follows the directing character. Held
possibly owned camps count conservatively until reviewed. Inherited camps remain
even if they exceed the limit; new establishment waits until capacity is available.
The configured staff roster capacity is unchanged.

Menus capture their opening session. Invite, rename, close, relocation, sampling,
mining, brushing, lab and sketch callbacks retain their initiating session and
check it before acting. A switch ends outgoing work using its captured session,
even though it is already noncurrent. Sketch cleanup saves the outgoing drawing
before the body is captured. A late callback cannot finish another character's
work or close a newer menu. Worker invitations accept an unambiguous character
name or UUID; an online account name resolves only its current character.

## Raw dossier migration

All paths below are beneath `plugins/Archaeo/`.

| Path | Meaning |
| --- | --- |
| `sites/<site UUID>.yml` | Current dossier; schema 2 and `actors-version: 1` discriminate character actor fields. |
| `ownership/source/<site UUID>.yml` | Immutable original dossier bytes, including comments and line endings. |
| `ownership/plans/<site UUID>.yml` | Version 1 fixed legacy account-to-character mapping and original source text. |
| `ownership/journals/<operation ID>.yml` | Version 1 migration or estate intent with exact before/after snapshots and durable completion. |
| `ownership/superseded/<operation ID>.yml` | Exact obsolete estate intent, archived only while the source still equals its before snapshot. |
| `ownership/completions/<death UUID>/<revision>.yml` | Full decision acknowledgement, cumulative moved IDs/count and retained source ownership. |
| `ownership/placements/<operation UUID>.yml` | Camp occupancy, kit and world-effect evidence; retained after completion. |
| `ownership/conflicts/<operation UUID>.yml` | Held or stale runtime progress, last checked source and current disk evidence; manual recovery only. |
| `ownership/reconciled-conflicts/<operation UUID>.yml` | Unchanged conflict evidence archived after explicit offline reconciliation; retained for review and excluded from automatic rollback. |

Startup inventories every raw dossier before publishing any migration. IDs must
match filenames and be unique across the complete inventory. Duplicate/nontext
YAML keys, recursive containers, unsupported or fractional versions, conflicting
refs and malformed gameplay actors are held. Legitimate ownerless hidden ruins
remain distinguishable from unresolved ownership.

Every historical director, excavator, worker and prospect actor must resolve via
`Characters.legacyHeir` after `legacyHeirsReady`. Missing historical worker or
sample identity can hold the entire dossier, even when its director is known.
The fixed mapping records unresolved entries; no later active character replaces
them automatically. Never delete a held site or treat it as absent property.
Held locations block overlapping creation; unlocatable held dossiers conservatively
block new occupancy until reviewed.

To resolve a missing heir in an existing fixed plan:

1. Stop Paper cleanly and back up the complete `plugins/Archaeo/` directory.
2. Inspect `ownership/plans/<site UUID>.yml`. Proceed only if this plan has never
   produced a journal: if any live or archived journal names the dossier in its
   `file` field, leave the plan unchanged for manual recovery. The current legacy
   dossier must exactly match both the plan's `source` text and
   `ownership/source/<site UUID>.yml`.
3. Verify each missing account's
   [reviewed RPCharacters heir](../../RPCharacters/docs/character-bodies.md).
   Replace only that account's null `legacy-map` value with its full reference,
   using canonical UUIDs. For example, this mapping entry has the format:

   ```yaml
   legacy-map:
     11111111-1111-4111-8111-111111111111:
       account: 11111111-1111-4111-8111-111111111111
       character: 22222222-2222-4222-8222-222222222222
   ```

   The `account` must match its legacy key, and the reviewed character must belong
   to that account. Keep `version: 1`, `source`, every other mapping entry and the
   exact historical actor key set unchanged. Never edit the immutable original,
   current dossier or a journal to choose an heir. Without a reviewed heir, leave
   the null entry and dossier held.
4. Restart after checking the YAML. Archaeo validates the fixed mapping and writes
   a migration journal before publishing the character dossier. Any unresolved
   actor or conflicting evidence keeps the dossier held for staff recovery.

Unknown maps, row fields, typed binary scalars and explicit nulls survive migration
and routine saves/restarts. A recognized field that the runtime cannot preserve
holds the dossier for reviewed recovery. Such a dossier remains in the raw
inventory and estate holdings even if it cannot enter the runtime cache. Gameplay
writes compare the current file with the exact loaded source; conflicting external
edits are retained. An unreadable dossier at its own save boundary becomes a
held conflict, preserving dirty progress and the actual read error in a snapshot.
Known transient write failures permit only a checked retry; restore storage and
flush that progress successfully before shutdown.

Unexpected runtime additions, edits, removals or individual unreadable files hold
the affected names and refuse new-dossier creation and estate inventory operations
until re-inventoried. Checked healthy existing sites can still save their progress.
A failed directory listing keeps the whole inventory unavailable. Hourly retry,
`/archaeo reload` and restart re-run the full preflight: an individually unreadable
file then makes the whole inventory unavailable until it is readable and a
complete retry succeeds. Healthy dirty progress is flushed before that preflight;
restore readability promptly.
Reload retains unchanged live site instances and promptly loads a released site.
Sampling cancels if its captured site has been replaced.

A refused first save with no checked source and no published file drops only that
unpublished creation from the cache and flush queue; it creates no conflict
snapshot or phantom holding. A file already published before failure remains
protected. Any validated active conflict whose current dossier is verifiably
absent stays held and reserves its recorded chunks, regardless of whether its
snapshot recorded present bytes, absence or a read error. It does not count as
another inventory mutation on every retry. Unrelated creation and estates can proceed when the
remaining inventory and possible ownership permit it. An unknown read-error frame
still protects every character, including after deletion. Reappearance or another unexpected change
still requires re-inventory.

Before removing held dirty progress from the flush queue, Archaeo writes an
immutable conflict snapshot containing the captured runtime, raw overlay, last
checked source and current disk bytes (or its read error). It never overwrites
the conflicting source or replays that progress automatically. Snapshot-associated
dossiers stay held across reload/restart, including their possible ownership,
camp limits and occupied chunks. Estate settlement blocks before any transfer or
completion for a held possible owner, including FROZEN/WAITING decisions; an
unreadable or unidentified conflict frame conservatively protects every character.
Failed snapshot
writes retain the captured object in memory and refuse site reload; staff must
restore storage and obtain durable evidence before shutting down. `/archaeo reload`
reports this refusal instead of claiming that sites reloaded. Staff deletion
checks and removes the dossier before purging camp blocks or tagged items; a
held, changed, missing or undeletable dossier refuses those effects.

Resolve a runtime conflict only while Paper is stopped and after a complete
backup. Inspect every snapshot whose `file` names the dossier: `source` is the
last checked text, `runtime` is the captured model, `captured` retains its raw
overlay, and `current`/`current-error` record disk evidence. Compare these with
the current dossier, world and affected inventories. Reconcile legitimate progress
and effects into the current dossier without dropping unknown fields or changing
character references contrary to reviewed estate decisions; never copy the
captured overlay over newer data wholesale. Record the staff decision and the
before/after hashes with the backup. Only after validating that reconciliation,
move each original snapshot unchanged from `ownership/conflicts/` to
`ownership/reconciled-conflicts/`, retaining the same UUID filename. Do not edit
or delete evidence merely to resume play. Next startup validates the archive and
dossier; any remaining active conflict snapshot keeps the site held. Transient
estate holds without runtime-conflict evidence can still release normally.

If the current dossier is missing and `source` contains a previously checked
record, restore a reviewed dossier from the complete backup or that checked
source, then reconcile captured progress, world/items and current estate authority
before archiving evidence. Preserve all unknown fields and newer valid changes;
restoring an old source blindly is not reconciliation. If an older snapshot has
both `source: null` and `current: null`, establish from backups, logs, world and
inventories that no dossier was published and no effects occurred before recording
that decision and archiving it unchanged. Inconclusive cases remain held.
`current-error` means the file could not be read, not that it was absent. Current
absence needs a separate filesystem check. Restore a reviewed dossier and
readability, then inspect its actual contents and reconcile progress/effects;
deletion alone never resolves or discards the read-error evidence.

## Estate handover

The participant is `archaeo-sites`. Boot and hourly reconciliation report outcomes
for the current decision revision. An estate transfers only the director reference
and registers the exact recipient ref. Worker tallies, original roster slots,
prospect progress, finds and unrelated fields remain intact. The recipient's
existing progress is preserved. The current director alone displays the Director
role; an old worker page can retain its historical role without granting authority.

A character recipient must differ from the testator.

Each transfer binds death, testator, recipient, full decision, revision and exact
before/after dossier. The guard is rechecked before publication and completion.
Interrupted matching plans recover idempotently. A newer decision can supersede
an obsolete intent only when the actual source still exactly matches its before
snapshot; the original intent is archived without inventing a moved ID. Published,
partial or conflicting obsolete intents block for staff review. Completed receipts
are validated before their moved IDs are reused. Frozen/waiting revisions retain cumulative receipts. A restored already
moved site cannot be transferred twice for the same death.

Relevant semantic receipts and all revision completions are preflighted before
any pending publication, supersession or source transfer, including at startup.
Corruption in a later receipt or older completion blocks the entire operation
before source/journal effects.
Every live or archived intent for one death/revision must agree on the full
decision, and the historical completion must match that revision's intents.

Each completed decision revision has a durable completion record, including a
zero-site outcome. It binds the full decision, cumulative completed receipt IDs
and count, and retained canonical site UUID filenames/director refs. The same revision cannot
absorb a newly discovered or newly resolved source; staff must issue a new
revision. New revisions move only untouched still-testator sites. Frozen/waiting
repeats retain their recorded ownership, allowing ordinary care/history changes
without opening the completed decision to new ownership.

## Camp placement boundary

Establishment and relocation write a durable captured intent before kit/world
effects. It contains the actor/session, exact prior and desired dossier, kit YAML
payload, world, and unique block coordinates with before/after block-data strings.
Checked dossier publication precedes block changes and kit consumption. A known
intent or dossier write failure leaves the kit and world untouched.

An interrupted or ambiguous effect holds the dossier on restart. The plugin never
replays kit debits or world placement automatically. Staff must compare the intent,
current dossier, player inventory and world while offline before resolving it.
File durability and inventory/world persistence are separate; this mechanism does
not promise exactly-once effects across an arbitrary crash. Both completed and
pending placement evidence remain excluded from automatic rollback.

## Offline recovery

Use a source checkout containing `tools/site-ownership.py`. Python 3 and PyYAML
are required (`python3 -m pip install PyYAML` in an isolated environment if absent).
The deployment owner must stop Paper cleanly before recovery. Preview first:

```sh
python3 tools/site-ownership.py --data /path/to/plugins/Archaeo
```

The report inventories raw dossiers, live and superseded journals, completion
records, placements and runtime conflicts. Apply restores only
an unchanged, completed migration whose exact current bytes match its captured
before/after snapshot and which has no estate or placement history. Superseded intents and revision
completion records remain manual estate evidence. It preserves
new, deleted, changed, held and incomplete records for manual review. A dossier
with runtime conflict evidence also remains manual, even if its current bytes
match a completed migration. Invalid journal/completion/placement/conflict metadata
or duplicate/unreadable inventory blocks all changes.

Use a new backup directory outside the plugin data folder:

```sh
python3 tools/site-ownership.py --data /path/to/plugins/Archaeo \
  --apply --backup /path/to/new/archaeo-recovery
```

The tool copies the complete current plugin tree, verifies SHA-256 hashes and
forces the backup before restoring any original bytes. It archives completed
migration journals under `ownership/rolled-back/journals/` using no-clobber links.
The immutable source and fixed plans remain. Review the JSON report and backup
before restarting; starting this build again can reapply reviewed migration plans.

Archaeo 2.0.7 and earlier can read a schema-2 dossier as legacy data and drop its
character references on the first save. Do not start those versions while any
schema-2 dossier remains, including new, changed or held sites that the selective
recovery tool preserves. A successful selective rollback does not establish
downgrade compatibility. Fix forward, or restore a coherent reviewed pre-upgrade
backup of the JAR and plugin data after assessing the progress and property that
would be lost; retain current dossiers and all recovery evidence separately.

Any restore/archive I/O interruption requires staying offline and reviewing the
full backup plus surviving intent/archive. There is no automatic estate,
progression, kit or world undo. Do not restore only selected old files over newer
worker/sample/find progress. Keep all originals, current data and receipts until
that reconciliation is complete.
