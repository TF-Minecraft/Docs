# Vehicle ownership

A vehicle has one owner value, a whitelist, a whitelist switch and ticket settings. VehicleFramework stores them in the vehicle's SQLite row (the `owner` column and the `payload_json` keys `owner`, `whitelist`, `whitelisted`, `ticketsEnabled` and `ticketId`). The [player guide](playing.md) covers the menus; this page covers identity, migration and the API other plugins use.

## Identity mode

`ownership-identity` in `config.yml` decides who owns vehicles. It is read once at startup; `/vf reload` logs a warning if the value changed and keeps the old mode until a restart.

| Value | Owners and whitelist entries |
| --- | --- |
| `characters` | The RPCharacters character being played. A different character on the same account is a stranger. |
| `names` | Account names, as on a server without RPCharacters. |

If the key is missing while RPCharacters is installed (whether or not it has finished starting), ownership is turned off and the console shows a block of severe lines: nobody can claim, change whitelists, take over or use the ownership API, and an owned vehicle with its whitelist on admits only ticket holders. Without RPCharacters a missing key means `names`. An unknown value also turns ownership off. VehicleFramework does not soft-depend on RPCharacters.

In `characters` mode every check asks TLibs for the player's current character session. Without RPCharacters' provider, or without a current session, the player owns nothing and cannot claim, edit or take over (staff included).

## Owner values

| Value | Meaning |
| --- | --- |
| `char_<characterId>` | Owned by that character. |
| `none` | Unowned. The next player to use it claims it. |
| `char_none` | A faction vehicle whose faction has no leader character. It matches nobody and can never be claimed. |
| `player_<name>` | Legacy account owner. Used in `names` mode; inert in `characters` mode. |

Character whitelist entries are stored as `char_<characterId>;<accountId>;<name>`, where the name is the one captured when the entry was added. In `characters` mode `player_<name>` and bare-name entries grant nothing. The whitelist menu shows them greyed out as "Old entry" so the owner can remove them. Staff (`vf.admin`) also see each entry's account, and the menu shows the owner's character name (with the account for staff).

VehicleFramework never migrates owners itself. SimpleFactions converts legacy values through `setOwnership(..., MIGRATE)` and records what it could not convert; `/vf admin quarantine` lists those vehicles.

## Whitelist in characters mode

"Add to Whitelist" opens a picker of players who have a current character and are within 16 blocks of the vehicle or aboard it, leaving out the owner and anyone already listed. Each head shows the name other players see; that name and the character are stored when it is clicked, and the click is refused if the player has since switched character.

"Type a Name" takes a character's real name in chat. Exactly one living character must have that name; no match and several matches give the same refusal. It needs TLibs 2.5.0 (`Characters.findByName`), which VehicleFramework checks once at startup; with an older TLibs the button is hidden and the picker still works.

## Claims, changes and takeovers

Characters mode clears the whitelist and turns it off when a vehicle is claimed, cleared or taken over, so a new owner never inherits the previous crew. `names` mode keeps the whitelist on claim and takeover and only turns it off when ownership is dropped.

Every change saves the vehicle at once. If the save fails, the vehicle keeps its previous values and the player is told nothing changed.

`/vf takeover` gives the next vehicle you right-click to your current character; `/vf takeover <name>` gives it to the single living character with that real name. Taking over an unowned vehicle counts as a claim; taking over an owned one is a takeover. Both fire the ownership events, and the click is checked again for `vf.admin` and an unchanged character session.

While SimpleFactions is installed (even if it failed to enable), a player without `vf.admin` can change ownership only once SimpleFactions has registered its `VehicleOwnershipAuthority`.

## Plugin API

The API is in `net.tfminecraft.vehicleframework.api` and the events in `net.tfminecraft.vehicleframework.events`. Call everything on the main thread.

`VehicleFrameworkApi`:

| Method | Returns |
| --- | --- |
| `ownershipIdentity()` | `CHARACTERS`, `NAMES` or `DISABLED`. |
| `listOwnershipMeta()` | Every stored row except tombstones, plus loaded vehicles without a row. Each `OwnershipMeta` keeps the stored owner column, the stored payload values and the live values apart, so a verifier can compare them. Throws if SQLite is closed. |
| `readOwnershipMeta(UUID)` | The same for one vehicle. |
| `setOwnership(UUID, OwnerChange, SystemReason)` | `OK`, `NOT_FOUND`, `SAVE_FAILED` or `REFUSED_MODE` (not in characters mode). |

`setOwnership` writes a loaded vehicle and saves it, putting the old values back if the save fails; it never falls back to the stored row. An unloaded vehicle has its owner column and payload rewritten in one SQLite transaction. Tickets never change. `OwnerChange` accepts `none`, `char_none` and `char_<characterId>`; only `MIGRATE` may carry whitelist entries (`OwnerChange.seeded`). The reason decides the whitelist:

| Reason | Entries | Switch |
| --- | --- | --- |
| `RESTAMP` | kept | kept |
| `MIGRATE` | the seeded entries, or kept when none are given | kept |
| `CONSTRUCT` | emptied | on if `allow-whitelist` and `whitelisted-by-default` |
| `RELEASE`, `HANDOVER` | emptied | off |
| `TRANSFER` | emptied | kept |

`VehicleOwners` builds and parses owner values and whitelist entries.

Events:

| Event | When |
| --- | --- |
| `VehicleOwnershipEditCheckEvent` | Before an ownership-menu button is shown and again on every click. A pure check: `deny()` hides or refuses the control. An empty reason means opening the menu. |
| `VehicleOwnershipChangeEvent` | Before a player's change is written. Cancellable. Carries the vehicle actually changed (the locomotive for tickets), the reason (`CLAIM`, `CLEAR`, `TAKEOVER`, `WHITELIST_ADD`, `WHITELIST_REMOVE`, `WHITELIST_TOGGLE`, `TICKETS_TOGGLE`), an operation ID, the acting character, a staff flag, and the target character or raw whitelist entry. |
| `VehicleOwnerClaimedEvent` | After the change event, for claims only. Still cancellable; kept for older listeners. |
| `VehicleOwnershipChangedEvent` | After the write, with the same operation ID, the outcome and the values before and after. For a player change it always fires once the change event has fired, including when the change was cancelled or the save failed. For `setOwnership` it fires only on `OK`. |

Services, looked up on every call:

- `VehicleOwnershipAuthority`: SimpleFactions registers it once it handles the change events. `ready()` returning false counts as missing.
- `VehicleQuarantineSource`: lists `QuarantinedVehicle` rows for `/vf admin quarantine`. Every registration is listed.
