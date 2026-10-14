# Mage gear

Magic owns mage-weapon assembly, enchanted charges, station orb runs, weapon
resonance requirements, Rift and revision refresh. The implementation is in
[the gear package](https://github.com/TF-Minecraft/Magic/tree/main/src/main/java/net/tfminecraft/magic/gear).

## Configuration

| File | Purpose |
| --- | --- |
| `charges.yml` | Charge item paths and aura caps by item tier |
| `gear/archetypes.yml` | Weapon templates, melee behavior and socket groups |
| `gear/part-types.yml` | Part categories |
| `gear/parts.yml` | Part compatibility, costs and socket contributions |
| `gear/socket-colours.yml` | Socket colour prefixes by resonance band |
| `gear/orbs.yml` | Hitscan, orbit, capture, Rift and difficulty settings |
| `skills.yml` | Skill-to-element bindings used for cast checks |
| `config.yml` | Station and alignment settings |

Archetypes include staff, wand and sword. Selected parts determine socket count,
clamped to four. MMOItems supplies templates, gemstones and skill combinations;
TLibs supplies socket groups.

## Charges and station use

Charges implement the shared aura-vessel interface. They gather aura through
eligible shrine, sacrifice and admin-fill paths, and display element tier bands.
They are excluded from meditation and artifact care/muffle handling.

1. Right-click an empty station and select an archetype and its parts.
2. Confirm assembly. Materials are consumed and the prepared weapon stays on the
   station, with its provenance and state persisted.
3. Apply a filled charge. Blank charges and concurrent runs are refused. A charge
   above the player's resonance band requires confirmation.
4. Hit the station's good orbs and avoid bad ones. The charge is consumed when
   the run begins; the captured result is written when the run ends.
5. Right-click with an empty hand to eject the weapon. Ejection is blocked
   while a run is active.

To recharge an existing mage weapon, right-click an empty station while holding
it without sneaking. One weapon moves from the hand onto the station and retains
its state. Apply a charge as above, or take it back with an empty-hand click.

The station does not need to be at a shrine. Difficulty uses the charge item's
tier, not its displayed aura band. A character switch, permanent death, disconnect
or shutdown finishes the outgoing character's runs with their captured result. The
charge stays spent and the weapon remains on its station. The incoming character
cannot hit the old orbs, and the station's part choices and any pending over-tier
confirmation are cleared, so it must choose and confirm again. A player without an
active character is told so and cannot start a run.

Deposited weapons belong to the full account and character that prepared or
rested them. Abort and material-refund actions require that character or
`magic.admin`. Charging and empty-hand ejection remain public to active living
characters. An ownerless legacy station retains public charging and ejection;
its active run records the initiating character. Abort returns require the
station's full character owner, including when staff act. Ownerless or unresolved
property stays on the station for review.

Menus, over-tier confirmations and runs capture their initiating session. A late
callback checks the occupancy ID, original item and full owner before writing.
Ending an outgoing session can finish its already-paid run, including after the
session becomes noncurrent, without changing a replacement station or a newer
session's menu.

## Property storage and inheritance

`data/gear-stations.yml` remains authoritative. Original row keys, root metadata,
unknown fields, explicit nulls, unloaded worlds and unsupported item records
survive saves and restarts. Character-owned rows add an `occupancy-id`, explicit
`ownership` envelope and `effect-state`; new or updated weapons use exact Paper
`item-bytes`. The original legacy item map and account attribution remain raw.
Unresolved ownership or unreadable data is held for review.
A row with an unparseable location retains its raw data without blocking deposits
at unrelated valid coordinates. Known held coordinates remain reserved; duplicate
occupancy IDs or valid occupied coordinates still hold the inventory.

Legacy account owners migrate only after the reviewed heir directory is ready,
using its exact account-matching character reference. Plans fix that recipient;
a changed heir mapping never redirects a retry. Missing or malformed owners are
kept separately from legitimately ownerless stations. TLibs 2.6.0 supplies the
character ownership and estate APIs. On an older API, character gear actions and
migration remain unavailable until the supported APIs are installed.
Participant startup failures with present APIs log the underlying cause at
`SEVERE`, separately from the missing-API warning.

Estate participant `magic-gear` transfers deposited gear and queued returns.
It waits for every orb run touching the testator's gear, including public runs
started by someone else. It checks the current estate decision before each
publication and records exact death, source, recipient, revision and decision.
Newer decisions move only untouched property; a partial older publication is
blocked for recovery. Immutable source archives and independent receipts retain
cumulative moved IDs through waiting or frozen decisions. Restoring a completed
source, losing receipt IDs or altering a captured envelope blocks further moves.
Every completed revision, including zero-item outcomes, also has independent
full-decision evidence and its remaining source IDs. The same revision cannot
absorb newly discovered property; a newer estate decision is required. Globally
duplicate return operation IDs are held, including delivered or interrupted
evidence. An exact pair belonging to one unfinished fixed publication can resume
only that captured plan.
Inheritance does not apply acquisition limits.

Magic profiles, focus, resonance and progression never participate in this
transfer. Crafting costs, bypass permissions and other account policies retain
their existing behavior.

## Interrupted effects and queued refunds

Deposits, charges and releases persist intent before changing inventory or
spawning world output. Abort refunds are queued under
`data/gear-returns/<character UUID>/<operation UUID>.json`. Rested weapons return
as the original item; fresh crafts refund their recorded materials. Delivery
always targets the deposited character, even after a staff abort. Immediate
delivery uses only that recipient's captured session; staff aborts for another
character queue the property for its owner. Delivery uses empty storage slots,
retains any remainder and retries for the owning
character when its next valid session starts. A full inventory does not discard
the queued remainder or hand it to an incoming character.

A fresh craft with a missing, malformed or overflowing recorded material payment
cannot automatically refund today's recipe. Its weapon and raw record stay on
the station for staff review; it can still be charged and publicly ejected after
attunement. An explicit empty cost map remains a known material bypass.

An interrupted deposit, charge, world release or inventory delivery is held with
its evidence for staff review. Restart does not blindly repeat or discard it.
Runtime scans preserve regular `magic-*.tmp` staging files without treating them
as committed records. Temporary-looking directories or symlinks and malformed
committed records still hold operations for review.
Paper inventory/player saves, world item storage and Magic files are separate
durability domains: this is not an arbitrary-crash exactly-once guarantee.
Public ejection and missing-furniture cleanup still drop the weapon into the
world; a crash between that effect and its acknowledgment requires staff to
compare the held record, player/world data and recovery evidence.

## Offline ownership recovery

Stop Paper before using
[`tools/gear-ownership.py`](https://github.com/TF-Minecraft/Magic/blob/main/tools/gear-ownership.py).
Python 3 and PyYAML are required for this offline tool; plugin dependencies are
unchanged. Preview legacy migration or estate journals:

```sh
python3 tools/gear-ownership.py --data /path/to/plugins/Magic/data --kind migration
python3 tools/gear-ownership.py --data /path/to/plugins/Magic/data --kind estates
```

Apply only one previewed run/death UUID, with a new backup directory outside
Magic's data folder:

```sh
python3 tools/gear-ownership.py --data /path/to/plugins/Magic/data --kind estates \
  --journal <death-UUID> --apply --backup /path/to/new-gear-recovery
```

The tool preflights the whole selected journal, full references, captured
decisions, raw payload semantics, original archives, receipts and current rows.
It rejects conflicting, progressed or ambiguous effects before restoring
ownership. It saves and verifies gear-only recovery bytes first, preserves
unrelated station rows and archives rolled-back journals and receipts. Untouched
planned records are no-ops. Restore errors require preserving the backup and
keeping Paper stopped for manual recovery. The tool never replays physical
effects or changes profiles/focus. Do not downgrade a progressed station to an
older JAR: the retained legacy item map may precede its newer authoritative item
bytes.

## Staff weapon commands

`/magic weapon give <player> <staff|wand|sword> <element> <aura> <part> [part...]`

Gives one completed mage weapon to an online player. Use part IDs from
`gear/parts.yml` and an enabled attunement element from the loaded configuration.
Supply exactly one part for each required category, respecting the core's part
limit. Aura is a finite positive raw attunement amount and must reach a configured
tier band. The command applies attunement, finalizes sockets, and records no
material cost. It does not change the recipient's resonance. The recipient needs
an empty inventory slot.

`give-permission` in `config.yml` defaults to `magic.weapon.give` (operators).
Set it to the chosen staff permission; a blank value disables giving. This
permission is independent of `magic.admin`. Reload configuration with
`/magic reload`. Tab completion suggests recipients, archetypes, elements, and
enabled part IDs.

## Orb results and weapon state

Capture is clamped to 0–1 from good hits divided by the tier's `good_target`,
minus missed-good-orb penalties. Bad hits add Rift up to its configured cap.
A later recharge can reduce existing Rift once per completed run.

Weapon requirements are stored per element. Applying captured aura uses the
higher of the existing and incoming requirement; values do not add. A new element
adds its own requirement. The first charge selects socket colours from the
captured band. Requirements display as tier bands.

## Cast checks

Checks use held mage gear, preferring the main hand and otherwise the offhand.
For a skill bound to an element:

- Missing weapon requirement or insufficient player resonance refuses the cast
  before mana and cooldown are spent.
- After that check, a cast wears the weapon. Rift rolls a flat fumble chance;
  holding more than one staff forces an overload fumble. A fumble spends mana
  and cooldown and cancels the spell.
- Alignment is a configurable bonus derived from the weapon's band. It is
  synchronized when held gear or the relevant resonance changes.

Armor does not gate spells. Skills cast without mage gear retain their normal
behavior. Refusal and alignment derive from live session and weapon state.

## Refresh and recycling

Provenance records parts and revisions. Refresh reconciles socket layouts while
preserving applied runes. A rune that no longer fits marks the weapon broken;
its data is retained for reclamation. Disable configured IDs instead of deleting
them from persisted item definitions. Refresh and socket rewrites keep an
ArmourShop skin the weapon is wearing; the part model scheme only applies to
unskinned weapons.

The Recycler provider returns configured part materials and discards weapon
resonance. Check refresh and reclamation after changing parts or archetypes.

## Validation

Use the exact source and dependency set intended for release. Check station
persistence, material consumption, blank/over-tier charge handling, ejection
locks, perfect and missed orb runs, multi-element highest-only merging, Rift
at 0 and 100, refusal without cost, alignment resync, rune preservation and
recycling. Record results with the run or PR.
