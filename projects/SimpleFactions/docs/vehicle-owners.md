# Vehicle owners

SimpleFactions decides who may change a VehicleFramework vehicle's owner and who
pays for it. VehicleFramework 2.13 stores owners as characters (`char_<id>`);
SimpleFactions moves the old account-name owners across once, keeps faction
vehicles stamped for their leader, and keeps the payer registry in step. The
[VehicleFramework guides](../../VehicleFramework/README.md) describe the owner
values, the whitelist and the staff commands.

## Startup

Factions start without waiting for VehicleFramework. Vehicle work runs in a
separate stage once factions have started and VehicleFramework is enabled,
whichever happens last: SimpleFactions tries straight after it starts, and again
when VehicleFramework enables. The stage runs once per server start, on the main
thread, in this order:

1. the stage-5 payer migration (`identity/vehicle-payers.json`, once);
2. the owner migration (`vehicles/owner-migration.json`, once);
3. the leader reconcile, which stamps every faction vehicle for its leader;
4. the upkeep reconcile, which also caches the account on older personal rows;
5. the vehicle listeners;
6. the `VehicleOwnershipAuthority` service.

A failure in steps 1 or 2 disables SimpleFactions, as any other unfinished
financial state does; the next start resumes from the plan files. A failure in
steps 3 or 4 is logged and the stage stops there, so no listener or authority is
registered and VehicleFramework refuses every player ownership change until a
restart. `SimpleFactionsReadyEvent` says nothing about vehicles.

If VehicleFramework never enables, factions run without vehicles and the log
says so once. If it is older than 2.13, or `ownership-identity` is not
`characters`, only step 1 and the listeners run: claims are refused for
non-staff, faction stamps are not written, and upkeep is still charged from the
personal registry rows.

## Owner migration

The first start in characters mode records a plan before it changes anything.
For each vehicle (stored rows except tombstones, plus loaded vehicles) it keeps
the original owner, whitelist and ticket fields and the decided new values:

| Vehicle | New owner |
| --- | --- |
| Pool or installation row | The paying faction's leader character, else `char_none` |
| Personal row | The row's character, when the old name still belongs to that account (`player_<name>` resolves through DenarEconomy and Bukkit returns the same name) and the account plays that character |
| No row | The reviewed heir of the account the name round-trips to |
| `none`, `char_*` | Unchanged |

Anything else is quarantined: it keeps its old `player_` value, which nobody
matches, and is listed by `/vf admin quarantine`. Whitelist entries move to the
named account's heir when the name round-trips and otherwise stay, greyed out.

Before the first write the plan is synced to disk, then two fixed-name backups
are taken in `plugins/SimpleFactions/vehicles/`: `vehicles-6a-premigration.db`
(a `VACUUM INTO` copy of VehicleFramework's database, checked with
`quick_check`) and `vehicles_registry-6a-premigration.json`. They sit outside
VehicleFramework's rotating backups and are never retaken once the plan says
`backedUp`.

Each vehicle is then written only if it still holds its planned original
values; one that already holds the new values is marked done, one that holds
anything else (for example a staff takeover since the plan) is quarantined, and
one that no longer exists is counted as gone. Afterwards every vehicle's stored
and loaded copies are read separately; copies that disagree fail the stage. The
plan is then marked `completed` and never runs again.

## Ownership changes

VehicleFramework asks SimpleFactions about every player change through
`VehicleOwnershipChangeEvent` and reports the result through
`VehicleOwnershipChangedEvent`, both carrying one operation ID:

- Staff (`vf.admin`) are not refused, and their takeovers pay nothing; each
  staff claim, takeover and clear is logged as `[vehicle audit]`.
- Any other change to a pool or installation vehicle is refused, including the
  whitelist and ticket switches. The leader stamp only opens the ownership menu
  and the seats.
- A claim needs the claimer's current character, ready vehicle payments and a
  free personal slot, then pays the transfer fee when someone else owned the
  vehicle last. The first click shows the fee and the second pays it under the
  operation ID.
- After a successful claim or takeover the payer row names the new character
  and caches its account. A failed claim refunds its fee. Clearing ownership
  drops the payer row but keeps the last owner, so a friend who claims the
  released vehicle still pays the transfer fee.

SimpleFactions' own writes (construction, berthing, the pool, releases,
handovers, installation transfers and leader stamps) go through VehicleFramework's
`setOwnership`. The payer row is written first and put back if the owner write
fails. A constructed vehicle is stamped for the character that paid its
registration fee; if VFBuilders recorded a different constructor (or, for older
stations, the account's heir is someone else) it is stamped `char_none` and
listed for staff.

Gift, berth and pool requests capture both characters when they are offered and
refuse acceptance from any other character.

## Leader stamps

A faction leader change restamps that faction's vehicles at once, stored or
loaded, keeping their whitelists. Deleting a faction stamps its remaining rows
`char_none`; annexed and untangled vehicles have already moved with their
installations. Leaders without a character (no leader, a staff `dummy_N`) stamp
`char_none`. A click on a faction vehicle whose stamp is stale is refused once
while the stamp is fixed on the next tick, and the ownership menu is hidden
until then.

## Upkeep reconcile

At startup and every 24 hours SimpleFactions compares VehicleFramework's owners
with the payer registry. A character-owned vehicle without a row gets a personal
row for that character. Everything else that disagrees is listed for staff in
`/vf admin quarantine` and left alone: a vehicle owned by a current faction
leader with no row, a personal row whose vehicle names someone else, a stale
faction stamp, a row without a vehicle, and a personal row whose account cannot
be worked out.

## Slot limits

Personal limits count personal registry rows per account. Rows cache the account
when they are written, and the vehicle stage fills it in on older rows from the
character, or from the account the owner or payer migration matched. A row with
no knowable account counts against every claimer until staff resolve it, and a
lookup error refuses the claim.

## Rollback

Roll back the whole stage 6a set together with the server stopped. For
vehicles, run the rollback tool from the server folder, first without `--apply`
to see what it would do:

```sh
java -cp "plugins/SimpleFactions-<version>.jar:libraries/com/google/code/gson/gson/<version>/gson-<version>.jar:libraries/org/xerial/sqlite-jdbc/<version>/sqlite-jdbc-<version>.jar" \
  net.tfminecraft.simplefactions.vehicles.owners.VehicleOwnerRollback . --apply
```

It reads `vehicles/owner-migration.json` and, for each migrated vehicle whose
SQLite row still holds exactly the migration's owner, whitelist and whitelist
switch, puts the original values back in the `owner` column and the payload's
`owner`, `whitelisted` and `whitelist` keys, in one transaction. Position,
health, fuel, cargo and tickets are never touched. Changed and missing vehicles
are listed and left alone. With `--apply` it also moves the plan aside
(`owner-migration.json.rolled-back-<time>`) so a later upgrade plans afresh, and
writes `vehicles/refunds-<time>.json`: every claim, build and handover fee paid
after the migration and not refunded, with the paying character and account.
The `VACUUM INTO` copy is for disaster recovery only.

Under old jars, ownership changes made after the migration are lost and
character-owned vehicles left unrestored match nobody, so they are frozen rather
than stolen.

## Files

Paths are relative to `plugins/SimpleFactions/`:

| Path | Purpose |
| --- | --- |
| `vehicles/owner-migration.json` | The owner migration plan, its quarantine and its completion |
| `vehicles/vehicles-6a-premigration.db` | VehicleFramework database before the migration |
| `vehicles/vehicles_registry-6a-premigration.json` | Payer registry before the migration |
| `vehicles/quarantine.json` | Constructed vehicles held back for staff |
| `vehicles/refunds-<time>.json` | Fees to refund after a rollback |
