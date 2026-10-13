# Table ownership and estates

Private table authority follows a recorded character. Account UUIDs still route players, inventory and the existing placement limits; they do not grant another character on that account the recorded owner's rights. Wagers retain their separate captured identities and money recovery rules in [WAGER_ENGINE.md](WAGER_ENGINE.md).

## Classification and authority

| Stored mode | Owner authority | Property inheritance |
|---|---|---|
| Nonblank `ownerGuildId`, including a guild table with `staffMint` enabled | Existing guild membership/leadership, captured guild incarnation and staff override | Outside private property |
| No guild, `staffMint: true` | Existing staff permission and funding rules | Outside private property |
| No guild, `staffMint: false` | Recorded `ownerPlayer` plus `ownerCharacterId`, with a current live character session; existing staff override | Private table property |

`autoDealer` and expansion-slot counting do not change this classification. The owner record is separate from guild and staff funding. Editing a table's mode preserves its recorded owner; turning off staff mint does not adopt the editor as the private owner. New placements, including saved settings used as a template, capture the new placer's current character.

Explicit stored `staffMint` values take precedence even when `autoDealer` is null. Legacy missing/null mint fields retain the loader's old default: a missing/null automatic-dealer field uses that game's layout default, while an explicit automatic-dealer field defaults missing mint to false. Migration freezes the effective mint value in the same durable raw plan before property candidates are planned, including unloaded tables. Later layout changes do not reclassify that frozen record or recapture its owner.

Owner editing, pickup and private dealing/hosting require the full recorded identity. Guild tables retain their guild rules. The character provider must confirm that a session belongs to the connected account, that its character is alive, and that the session is still current. Menus, placement arms and queued chat capture that session. Applying settings also checks the table's original owner and its runtime ownership generation, including staff edits; an old menu cannot restore an owner changed by an estate.

Character session end clears placement, prompts, hands and dealer state through the existing disconnect cleanup. Cleanup uses the departing account even after its token stops being current. Money operations still require their original captured wager identity; cleanup cannot deliver that obligation to the next character. Missed lifecycle events do not authorize old menu or chat callbacks.

## Storage and migration

All paths below are relative to the Games plugin data directory, usually `plugins/Games/`.

Placed tables remain JSON files beneath `Data/tables/`. `ownerIdentityVersion: 2` adds nullable `ownerCharacterId` beside the existing `ownerPlayer`. Missing or version-1 identity metadata expands through the reviewed legacy-heir service, never the account's current, last-played or newest character. A missing reviewed heir leaves a null character slot; a later reviewed mapping can resolve it without erasing intervening table settings. A recorded dead character remains the owner until the estate decision changes property.

Each migration archives exact original bytes under `migrations/table-ownership/<SHA256-of-filename>/<original-SHA256>.original` and stores a frozen `.json` plan beside them. Archive and plan are forced before publication. Plans distinguish owner-envelope changes from legacy-mode freezing; a mode-only plan preserves an existing owner unchanged. A restart uses that original mapping/mode, checks both digests and the exact permitted output, and refuses changed sources or damaged archives. Raw files are inventoried before world/card-set filtering, so unloaded tables participate too.

Duplicate JSON fields, duplicate table IDs, unsupported or nonintegral identity versions, malformed owner/float/guild UUIDs and ambiguous guild-incarnation metadata remain untouched for review. Duplicate table IDs are checked across readable source files before owner or guild migration publishes anything. An unreadable inventory defers legacy mapping rather than guessing its missing rows; independently coherent, already resolved files can remain usable. Deferred loads retry every five seconds.

Ordinary saves overlay known gameplay fields onto the original raw document. Unknown fields, explicit nulls, nested ledger metadata and unrecognized wager references survive saves and restarts. Consumed, valid wager bindings can be removed normally. Unexpected file deletion, replacement or content changes hold the affected table rather than recreating or overwriting the source. A reviewed repair requires a fresh load/restart; guards do not silently accept an external writer as a new baseline.

## Estate settlement

Games registers the `games` estate participant when the guarded estate API is present. Only the decision's **property** recipient can receive private tables. Guild and staff-mode tables remain outside this transfer. Money, loot, house floats, guild banks, stakes and captured payout identities are never inherited with the table.

Settlement first requires reviewed legacy ownership and the exact current death, testator and decision revision. Unresolved private owner slots for the testator block settlement before an empty receipt can be written. `WAITING` and `FROZEN` property remain in place, with durable completions recording the full decision, retained table IDs/owner references and cumulative completed moves. Unsupported account/sender property routes and a self-recipient block rather than recording fictitious transfers.

A completion refuses changed same-revision decisions or newly appearing/resolved testator ownership at that revision, including an empty completion. A genuinely newer guarded revision can consider new untouched property and the previously retained pool. Persisted future-revision evidence blocks decision rollback before any effects. Previously moved table IDs can never move again for that death: every later revision detects a restored source. Historical retained completions bind their cumulative IDs to earlier completed character snapshots, and reports count each moved table once.

Plans under `estates/tables/<death-id>-<revision>.json` capture candidate table IDs durably before waiting for activity to finish. Pending transfers prevent new sessions, dealer claims, stakes and free draws. Existing captured games, payouts and card recycling can finish under their existing identity and money guards. Live work returns `RETRY`; retained wager intents, unresolved money, floats, stakes or ambiguous saved activity return `BLOCKED` with the table ID. Ownership settlement does not replay or remove a wager intent.

Once every candidate is idle, Games checkpoints loaded tables and freezes complete raw before/after documents. Publication changes only the owner account, owner character and identity version. It checks the guard again before each write, preserves unrelated raw fields and records exact completed IDs before releasing pending authority. Filesystem failures retry against the same plan, including a write whose bytes published before durability acknowledgement failed. Conflicting, stale or partial plans remain held. Historical receipts validate their death, full source/recipient, integral revision, filename, snapshots and moved IDs before contributing cumulative results.

Startup, estate/revival wake-ups and periodic reconciliation recover pending intents. Provider-confirmed revival or a different death can obsolete an untouched intent and release its pending tables. Missing providers are not cancellation evidence. A partially published transfer remains held for review; revival does not reverse completed property.

## Conservative rollback

Use the source checkout's `tools/ownership-rollback.py` for a single migration whose table has no later progress or estate history. Keep a complete stopped-data backup and preserve all migration and wager journals. The helper defaults to preview:

```sh
python3 tools/ownership-rollback.py /path/to/plugins/Games imported-table.json ORIGINAL_SHA256
```

Use the full original SHA256 from that table's migration plan. The helper verifies the immutable original, frozen account/character mapping and exact current migrated bytes. It refuses altered settings, ownership changes, damaged evidence or any estate intent/receipt naming that table. A compatible binary and dependencies must accompany any rollback.

After stopping Games cleanly, repeat with `--apply`. The plugin's `ownership-active` marker must be absent; it remains after an interrupted run or a shutdown with held ownership/money. Do not delete the marker to bypass recovery. Successful apply preserves the migrated file as `<table-filename>.pre-ownership-rollback` and restores the exact original bytes with atomic, forced writes. Previewing an already restored source is harmless.

This helper is deliberately unable to undo ordinary gameplay or estate transfers. Review those against the stopped backup and complete receipts, preserving obligations; restoring an old owner after a completed estate is detected and held.

## Compatibility and verification

The build pins TLibs **2.6.0**. Without the required identity capability or reviewed provider, private migration and current owner authority defer; no account fallback grants ownership. Older TLibs may expose character sessions while lacking guarded estates, so those capabilities are probed separately. Presentation-name fallback is independent of owner authority.

Run `tfmc-mvn -o -B clean verify` with Java 21. Automated scenarios cover account A-to-B switches and renewed sessions, missed lifecycle callbacks, staff stale snapshots, duplicate/malformed raw sources, null preservation, migration interruption, idle-only estates, receipt corruption, restored sources, revival and write acknowledgement failure. JaCoCo reports every production class and has no enforced threshold.

`integration-tests/LegacyApiCheck.java` can run with the full test dependency classpath, compiled Games classes and an actual older TLibs jar. Its arguments are the Games classes/JAR, old TLibs JAR, expected character-capability boolean and an empty isolated fixture directory. It tests capability separation, missing provider authority and byte-preserving deferred private migration. This compatibility probe and the automated suite do not verify client packet rendering; retain the [manual matrix](TEST_MATRIX.md) for server/client behavior.
