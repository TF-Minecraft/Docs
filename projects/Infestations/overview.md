# Behaviour, configuration, and operations

[Infestations documentation](README.md) · [All projects](../../README.md)

## System model

An infestation belongs to one SimpleFactions province and has a mob group from
`groups.yml` and a severity: `mild`, `worrying`, `severe`, or `extreme`. Each
province holds at most one infestation. Only land provinces can be infested:
provinces with a terrain listed in `skip-terrains` are refused, and a group
with a `terrains` list is limited to those terrains.

```mermaid
stateDiagram-v2
  [*] --> Idle: set or spread
  Idle --> Joining: lure placed
  Joining --> Active: join window ends
  Joining --> Idle: no committed players remain
  Active --> Idle: party lost
  Active --> [*]: remaining reaches zero
  Idle --> [*]: admin clear
```

**Idle.** Every `ambient-interval-ticks`, each player in Survival or Adventure
inside an idle infested province triggers one spawn attempt, as long as the
province's tagged ambient mobs are below `ambient-cap`. Spots lie in a ring
between `ambient-ring-min` and `ambient-ring-max` blocks from the player, within
two blocks of the player's height, inside the same province, and at or above
the group's `min-y`. Each spot needs a clear 3×3×3 space over a solid 3×3
floor in loaded chunks. No spot may be within `min-player-distance` of any
player other than spectators, checked again when the delayed spawn fires; the
ring minimum is raised to that distance and the ring maximum to at least eight
blocks beyond it. The search tries a capped number of random points, so a
failed search logs `no-spot` without loading chunks. `night-only` groups spawn
only while world time is 13000–22999. Mobs are picked from the group's weighted
MythicMobs list and tagged with the province and kind. Mobs that a dying
tagged mob summons, such as parasitic worms, take its tags. Killing ambient
mobs never clears an infestation, and the plugin does not remove spawned mobs.
The loaded ambient count is recounted at most every five seconds after tagged
mobs load or unload. A delayed ambient spawn requires the original connection
and, when character identity is available, the original character session.
Switching away and back, reconnecting, or losing that session cancels the
attempt. A provider that is present but has no ready character schedules no
attempt; a standalone attempt is cancelled if a provider appears before it fires.

**Lure.** Placing InteractibleFurniture whose item path equals `lure-item`
starts a lure. Placement is cancelled unless the province is infested land with
no lure; placing the lure item as an ordinary block is always cancelled. The
placer joins automatically and other players in the province are notified.
With character identity, placing or joining a lure requires a ready character.
Characters still loading receive no nonjoiner damage.
During the `join-seconds` window, players in the province see an action-bar
countdown and join by right-clicking the lure. Ambient spawning stops for the
duration of the lure; existing ambient mobs stay.

When the window ends, the province's loaded ambient mobs become lure mobs and
count toward `lure-count`. The remaining count starts at `lure-count`, or at
the number of mobs taken over if that is larger. It is the number of mobs left
to kill: any death of a lure-tagged mob reduces it, and each mob summoned by a
dying lure mob (for example the parasitic worms a bug zombie leaves) is tagged
and adds one to it. The lure spawns mobs until everything left to kill is in
the field, paced evenly across `lure-duration-seconds`. The pace counts
introductions against the clock, and mobs already sent wait for the next share.
A tally that has run ahead of both the clock and the mobs actually in the field
cannot stop the lure while enemies remain: the field is brought back up to the
share the clock has reached. After the duration, anything still owed is
released. The first mob is sent as soon as the lure is active. Spots lie
between `min-player-distance` (at least 4) and `lure-spawn-radius` blocks from
the lure and stay that far from players when such a spot exists. If the ring
has nowhere to put an owed mob, the search loosens to a single column of air
on a taller band, and any mobs still unplaced spawn at the lure. A delayed
spawn that a player has walked up to is moved to the lure instead of being
cancelled. The duration paces spawning; it is not a time limit. Every five
seconds the lure recounts its loaded mobs, takes over ambient mobs that loaded
since, and replaces mobs that were lost without being killed. A floating text display above the lure shows
the countdown or the remaining count to players within `hologram-view-range`. Right-clicking an active lure makes the remaining lure mobs
glow for 10 seconds and commits a player who has not yet joined. Uncommitted
Survival and Adventure players in the province take `deserter-damage` every
second until they leave.

- **Victory:** two seconds after the remaining count reaches zero, if it is
  still zero, the lure is removed and the infestation is cleared. The delay lets
  death summons join the count.
- **Failure:** the lure is removed and the infestation returns to idle at the
  same severity when no committed player is alive and online, within the
  logout grace period, or owed a death on login. A death held without a
  character, described below, does not count. A committed player who leaves
  the province stays in the lure and takes `deserter-damage` every second, in
  Survival or Adventure, until `/lure leave` drops them out. Coming back into
  the province stops that damage without dropping them. `/lure leave` fails
  the lure when nobody committed remains.
- **Departure:** switching character, quitting, or shutting down starts
  `logout-grace-seconds` for the outgoing character, which remains committed.
  Only that character's ready return ends its grace. After the grace expires,
  it is killed when it next becomes ready. A directory record belonging to
  the same account with status `DEAD` or `MISSING` settles the pending death
  without damaging the current character. Unknown records do not settle it.
  A committed character's death removes its own commitment.
- **Other characters:** another character on the same account takes no
  deserter damage for the waiting commitment, and its death or `/lure leave`
  does not touch it. Further departures preserve the first character and
  deadline. Character UUIDs are compared without case sensitivity; saved
  strings are not rewritten.
- **Deaths without a character:** when character identity is in use, a death
  saved without a character is held. A console warning names the player and
  province on enable, reload, and grace expiry. That debt brings no outside
  warnings or deserter damage and does not keep the lure alive. It clears
  when the lure ends or a ready character on that account dies or leaves.
- **Provider unavailable:** once the running manager has seen character
  identity or loaded a saved character tag, losing the provider holds
  commitments and penalties until a character is ready. It never converts a
  tagged penalty into an account penalty. This mode survives a config reload;
  saved character tags also restore it after restart. Invalid or unknown tags
  remain held.
- **Standalone:** with no provider seen and no saved character tags, the
  account owns the commitment. Quitting starts its grace and returning ends
  it or applies its pending death. Old records without character tags cannot
  distinguish a standalone penalty from a character-era penalty after a
  restart with no provider.

Players cannot break the lure, and explosions and pistons cannot move it. Lure
furniture that does not match saved lure state is removed on enable, reload,
chunk load, or when a player touches it.

**Spread.** When `spread` is `true`, every `spread-interval-seconds` each idle
infestation rolls `worsen-chance` to rise one severity (up to `extreme`). It
then considers uninfested land neighbours its group may occupy, plus such land
on the far side of one adjacent `water` or `sea` province. Two-province hops are
not considered. Each candidate uses its easiest route (land, then water, then
sea); one candidate is chosen, weighted by route chance, and a single roll
against `spread-chance-<route>` for the source severity decides whether it
becomes a new `mild` infestation of the same group. Infestations with a lure
neither worsen nor spread.

## Configuration files

The plugin copies its defaults into `plugins/Infestations/` on first start.

| File | Purpose |
| --- | --- |
| `config.yml` | Debug and spawn-log switches, spread switch, interval and chances, lure item, join window, lure spawn radius, minimum spawn distance from players, logout grace, deserter damage, hologram range, and `skip-terrains`. |
| `groups.yml` | Mob groups: `display` name, `night-only`, optional `min-y`, optional SimpleFactions `terrains`, weighted MythicMobs `mobs`, and per-severity `ambient-cap`, `ambient-interval-ticks`, `ambient-ring-min`, `ambient-ring-max`, `lure-count`, and `lure-duration-seconds`. |
| `messages.yml` | Chat, action-bar, and hologram text. `{prefix}` inserts the `prefix` entry; hex colours are formatted through TLibs. |

Chances are values from 0 to 1. Groups without `mobs` are skipped with a
warning, unknown terrain names are reported but kept, and omitted severity rows
use built-in defaults. The default `swamp_mobs` group spawns `SwampGhoul` at
night in `bog` provinces.

## Commands and permissions

Admin commands use `/infestation` (alias `/infestations`). Province arguments
take a numeric SimpleFactions province ID or `here` for the player's province.
`/lure leave` is available to every player.

| Command | Permission | Effect |
| --- | --- | --- |
| `/infestation set <province\|here> <group> <severity>` | `infestations.admin` | Infest an uninfested land province that the group's terrain rules allow. |
| `/infestation clear <province\|here>` | `infestations.admin` | Remove an infestation and any lure it has. |
| `/infestation list` | `infestations.admin` | List infestations by province, group, and severity, marking those with a lure. |
| `/infestation reload` | `infestations.admin.reload` | Reload all three files, then reload saved state from disk. |
| `/lure leave` | none | Drop the player out of every lure they have joined. |

Both permissions default to operators, and `infestations.admin` grants
`infestations.admin.reload`. Because `plugin.yml` also requires
`infestations.admin` for the command itself, the reload permission alone is not
enough. Reloading re-reads `Data/infestations.json`, removes stray lure
furniture and text displays, recounts loaded ambient mobs, and re-exports the
map data.

## Integrations

- **SimpleFactions** supplies province lookups, terrain, neighbours, and the
  province enter and leave events that govern lure commitment.
- **MythicMobs** spawns every ambient and lure mob. Unknown mob IDs are logged
  and skipped.
- **InteractibleFurniture** hosts the lure; placement, interaction, and break
  events drive the lure lifecycle. TLibs item paths identify the lure item.
- **TLibs character identity** provides ready sessions, end events, and
  owner-checked directory snapshots. RPCharacters 2.16.0+ is the optional
  provider. Infestations captures the outgoing identity even though its
  session is already invalid at end, and applies pending work only to a
  current ready session. It rechecks the session between penalties because
  damage listeners can switch characters synchronously.
- **Map export:** on start and whenever infestations are set, spread, cleared,
  or reloaded, the plugin writes each province's ID, severity, group, and
  display name to `MapAPI/infestation_data.json` and uploads it through the
  SimpleFactions REST server as `infestation_data`.

## Persistence and shutdown

- Infestations and lure state, including committed players, logout grace, the
  character each committed player logged out as, and lure counters, are stored
  in `plugins/Infestations/Data/infestations.json`.
- The latest map export is `plugins/Infestations/MapAPI/infestation_data.json`.
- When `logging` is true, spawn decisions are appended to
  `plugins/Infestations/logs/spawn.log`; `wipe-log` deletes it on each start
  and reload.

State is saved after each change and every five seconds. On a normal disable,
the plugin records departures for ready committed characters, removes lure
text displays, and saves state. Existing grace deadlines and penalties are
preserved, and the JSON field layout is unchanged. Lure timers use
wall-clock time, so a join window that expired during downtime activates immediately.
Stop the server before editing the data file, since periodic saves overwrite
manual changes.

## Validation

For a server-side change, verify the following on Paper 1.21.10 with the pinned
dependency set:

1. Start with both an empty data directory and a copy of representative
   infestation data, and confirm the configs load without group or terrain
   warnings and every configured MythicMobs ID exists.
2. Set, list, and clear infestations with both a province ID and `here`, and
   confirm refusals for water or sea, disallowed terrain, and provinces that
   are already infested.
3. Confirm ambient mobs spawn in the configured ring inside the province, never
   within `min-player-distance` of a player, stop at the cap, and honour
   `night-only` and `min-y`.
4. Place lures with and without an infestation, then exercise joining, the
   countdown, activation, paced spawning, highlighting, and deserter damage.
   Confirm a lure that still owes mobs spawns them even when the ring has no
   clear spot away from players, using the lure itself as a last resort.
   Confirm roaming ambient mobs count toward the lure when it activates, and
   that killing a mob that summons parasitic worms raises the remaining count.
5. Exercise victory, a committed player leaving the province (damage until
   `/lure leave`), losing the whole party, and a logout both within and beyond
   the grace period, including a return on another character after it. Switch
   Alice → Bob → Alice and confirm only Alice settles her saved penalty.
   Test provider loss while debts are pending, startup with tagged saved data
   but no provider, and standalone play with no tags. Confirm an old ambient
   callback cannot follow a reconnect or character switch.
6. On a test server, enable `spread` with a short interval and confirm
   worsening, land spread, single water and sea hops, and group terrain limits.
7. Confirm `MapAPI/infestation_data.json` is written and uploaded.
8. Reload and restart cleanly during a lure, and confirm infestations, the lure,
   its text display, and its counters are restored without duplicates.
