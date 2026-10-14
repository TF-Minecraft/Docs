# Estates

When a character dies, RPCharacters decides who receives what it owned after 24
hours (its estate). SimpleFactions takes part in four ways. It tells
RPCharacters which guild the character died in, it hands the dead character's
personal vehicles to the estate's recipient, it stops its own death cleanup
from acting on a character who was revived or died again, and it pauses upkeep
while vehicles wait for an estate.

Estates need TLibs 2.6.0 or newer. SimpleFactions checks for the estate API
once. On an older TLibs it enables as usual and takes no part in estates.
The bridge isolates estate API probing, calls and registration from financial
failures. An unavailable API disables estate integration; registration errors
are logged. A failed vehicle registry write during an estate move still follows
the ordinary financial fail-closed path and disables SimpleFactions.

See [Character membership and migration](characters.md) for death cleanup and
[Vehicle owners](vehicle-owners.md) for the vehicle stores.

## Death guild

Each death journal (`deaths/<deathId>.json`) records the guild a character
died in as `lockGuildIncarnation`. It also records that guild's realm as
`lockGuildRealm`. A realm is identified by its ruling guild's incarnation,
whose treasury is the realm treasury. Both use the same lookup at death,
including the civil-war rule: a member moved into a rebel main guild is
recorded in their origin guild, in the host realm.

SimpleFactions registers TLibs' `EstateFallback` service once factions have
started, before `SimpleFactionsReadyEvent` fires. It reads only journals and
loaded guilds. It never creates a guild and never re-reads a realm snapshot.

| Call | Answer |
|---|---|
| `deathGuild(character, deathId)` | **UNAVAILABLE** while SimpleFactions is not ready, when the journal cannot be read or names another character, and when there is no journal yet but a realm or warband still names the character (the startup reconcile writes it). **NONE** for a guildless death, or a character SimpleFactions never knew. Otherwise the **guild**: its incarnation, whether it still exists, its current leader and the realm at death. |
| `guild(incarnation)` | UNAVAILABLE while not ready, GONE, or the live guild with its name, current realm, leader and treasury account `guild:<incarnation>`. |
| `guildByName(name)` | As `guild`, matched by name, ignoring case. A guild incarnation is accepted in place of the name. Two live guilds with the same name answer UNAVAILABLE, so use the incarnation. |

The leader is `Guild.getLeader()`, so a ruling guild's leader is the realm's.
It is given only while the guild exists and the seat is filled, and it may be a
dead character. RPCharacters checks.

Journals written before 4.2.0 have no `lockGuildRealm`. For those, the realm is
the one realm whose saved rights plan lists the guild. If no plan or several
plans list it, the realm is unknown, and RPCharacters treats it as gone.
SimpleFactions 4.1.0 drops `lockGuildRealm` when it rewrites a journal, and a
payment rewrite can also drop the audit-only `closedBy` field. The stored-plan
realm fallback still applies after upgrading again; closed cleanup steps remain
unreplayed.

## Revived and re-dead characters

Before an unfinished journal is replayed, the character is checked:

| Character now | Journal |
|---|---|
| DEAD with this journal's death ID | Replayed as before. |
| ALIVE (revived), or DEAD with a later death ID | Closed: the remaining steps are marked done without running, the journal is marked complete, and `closedBy` records `revive` or `redeath`. |
| Unreadable (quarantined account, or no death ID) | Skipped until it can be read. |
| MISSING | Skipped: staff decide what happens to a missing character. |

Closing also cancels every claim whose cleanup step never ran, in the same
write, by marking it paid in full. That cleanup step would have cleared the
character's wage bucket and dividend eligibility. Those still pay the character
directly, so paying the claim as well would pay twice. Claims whose cleanup did
run stay payable to the character's bank.

`closedBy` is for audit only. SimpleFactions 4.1.0 reads a closed journal as
complete and its cancelled claims as paid, so rolling the jar back does not
replay closed journals.

A succession step never removes a living character from a seat. If the seat is
blank when the step replays, it is still filled.

## Vehicles

The `simplefactions-vehicles` estate participant registers at the end of the
vehicle stage. It needs VehicleFramework 2.13 in characters mode, as owner
changes do. It moves personal vehicles to the estate's property recipient once
the estate is decided. Vehicles stay with the dead owner while the property is
waiting or frozen for staff. Faction vehicles are never estate property, even
when they carry the dead leader's stamp.

A vehicle belongs to the estate when its personal payer row names the dead
character, or when VehicleFramework's owner is `char_<dead character>`. Before
a vehicle moves, a gate checks four things:

- its type is known;
- it is not a faction vehicle;
- no vehicle payment for it awaits recovery or staff;
- it is not held back in `/vf admin quarantine`.

A vehicle that fails the gate makes the participant answer RETRY. Unlike a
player handover there is no fee, no slot check and no battle lock. An inherited
vehicle may take the recipient's account over its slot limit. That blocks
further claims and builds until the account is back under the limit.

Each vehicle moves in three durable steps, recorded in
`vehicles/estates/<deathId>.json`. The plan is written before anything changes:

1. the payer row becomes the recipient's character and account;
2. VehicleFramework's owner becomes the recipient, with a HANDOVER write that
   empties the whitelist and turns it off;
3. the recipient is saved as the vehicle's last owner.

A replay after a crash looks at the row and owner as they are now:

| Row | Owner | Action |
|---|---|---|
| any | neither the dead character nor the recipient | The vehicle was handed on since; the entry is closed and the vehicle left alone. |
| not the recipient | any | Step 1 again. |
| the recipient | the dead character | Step 2 again. |
| the recipient | the recipient | Step 3, if not yet done. |

If the owner write fails for any reason other than a missing vehicle, the
previous row is put back and the participant retries. If the vehicle is
missing or cannot be read on three checks at least an hour apart, it is listed
for staff (BLOCKED). This also covers a vehicle destroyed after an earlier failed
step, when both its owner metadata and registry row are gone. The row is not put
back, so upkeep never falls on the dead owner. The participant's own hourly run
leaves a listed vehicle alone. Staff fix
the vehicle and run `/estate retry <deathId> simplefactions-vehicles`, which
reads it once more, or handle it by hand and waive it. A vehicle planned for a
recipient other than the decision's is also listed, never reported as moved.

The participant answers "nothing to move" for property that is waiting or
frozen even while the vehicle stage is not running, so it never holds back a
revive for that reason.

A finished settle reports the number of vehicles moved and every vehicle ID.
The participant also runs over every decided estate shortly after the vehicle
stage starts and then every hour. That catches a vehicle that appears later,
such as a build that finishes for the dead payer. It reports only changed
outcomes.

To undo a move by hand, each plan entry keeps `previousRow`. Restore only
entries whose row and owner still name the recipient.

## Upkeep while waiting

While a vehicle's payer is dead and its latest estate is open, held or decided,
the vehicle has not moved yet. Settlement marks no new unpaid day for it, and
the hourly upkeep does not damage it. An unpaid day marked before the death
stays until the recipient pays. Storage is free while property waits or is
frozen. The pause also lasts while the vehicles participant is not registered
(VehicleFramework older than 2.13 or not in characters mode). For decided character
property, the pause ends when registration and infrastructure recover and the
vehicle moves, or when staff revert or cancel the estate, or the payer is revived.
Staff cannot reassign character property. If staff revert an estate, the vehicle
stays with the dead owner and upkeep applies as before, even if its property was
frozen.

## Files

Paths are relative to `plugins/SimpleFactions/`:

| Path | Purpose |
| --- | --- |
| `deaths/<deathId>.json` | Death journal, with `lockGuildIncarnation`, `lockGuildRealm` and `closedBy` |
| `vehicles/estates/<deathId>.json` | One estate's vehicle moves: vehicle, from, to, previous row, step and attempts |
