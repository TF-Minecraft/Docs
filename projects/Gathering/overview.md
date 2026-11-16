# Behaviour, configuration, and operations

[Gathering documentation](README.md) · [All projects](../../README.md)

## System model

Gathering is something a player chooses to do. `/gather` turns on **gathering
mode**, which costs Mental Points while it is on. Spots appear around players in
the mode, and every player in the mode can see and harvest them. A spot records
its world, block position, spot type, surface material, spawn time, and when a
gatherer was last nearby. Each chunk holds at most one active spot.

Spots exist only in memory. The only saved state is each chunk's **depletion**,
which makes worked-over ground spawn less until it recovers.

## Gathering mode

`/gather` toggles the mode; `/gather on` and `/gather off` set it. It needs
`gathering.use`, which defaults to everyone, and a ready session from the
[shared character API](../TLibs/character-identity.md).

- Entering charges `mode.drain-amount` Mental Points (RPCharacters focus) at
  once, then again every `mode.drain-interval-seconds`. A drain amount of 0 makes
  the mode free.
- Mental Points belong to the character. If the player switches character, the
  mode stays on and later charges go to the new character.
- The mode ends only when the player turns it off or a charge fails. Logging out
  or a plugin disable also clears it, without a refund. `/gathering reload` keeps
  players in the mode.
- While the mode is on, a boss bar shows `mode.status-bar` (`{mp}` is the
  current Mental Points), filled to the share of the focus maximum. An empty
  value turns it off. An action bar is not used because the MMOCore HUD
  overwrites it.

## Spawning

Every `spawn.interval-seconds`, each player in the mode, in random order, may get
one spot:

1. **Cap.** Count active spots within `spawn.max-radius` of the player. The cap is
   `spawn.cap-base`, plus `spawn.cap-per-extra-gatherer` for each other gatherer
   within `spawn.max-radius`, never more than `spawn.cap-max`.
2. **Chance.** `spawn.base-chance` + wisdom × `spawn.wisdom-weight` + intelligence
   × `spawn.intelligence-weight`, capped at `spawn.max-chance`. Wisdom and
   intelligence come from the character sheet's creation-layer attributes.
3. **Location.** Up to `spawn.location-attempts` random points between
   `spawn.min-radius` and `spawn.max-radius` blocks away. A point is rejected if
   its chunk is outside the world's `worlds.<world>` chunk bounds, is not already
   loaded (the plugin never loads chunks), already holds a spot, or fails the
   freshness roll. The column is then scanned from `spawn.max-vertical` blocks
   above the player down to the same distance below. The first block that is
   solid, has two air blocks above it, and that at least one spot type accepts
   becomes the spot, unless another spot is within `spawn.min-spacing` blocks.
4. **Type.** One accepted type is picked by `spawn-weight`.

Worlds without a `worlds` entry never spawn spots naturally. TFMC's map world is
`TFMC_Map`, 6400 × 6400 blocks, so chunks 0–399.

## Chunk freshness

Each harvest adds `freshness.per-harvest` depletion to the spot's chunk, and each
spawn adds `freshness.per-spawn`. Depletion halves every
`freshness.half-life-hours`; it is computed when read, so no task decays it. A
chunk passes the freshness roll with probability
`1 / (1 + depletion × freshness.strength)`: one recent harvest gives 50%, three
give 25%, and three harvests two days ago give about 57%.

## Spot lifetime and visibility

- Players in gathering mode, and staff in admin mode, see a two-particle ring on
  spots within `spot.keepalive-radius`, coloured by `particle-dust` or the
  surface block. Other players see nothing.
- A spot disappears when it is older than `spot.lifetime-minutes`, when no player
  in the mode has been within `spot.keepalive-radius` for
  `spot.orphan-grace-seconds`, when its chunk unloads, or on reload and shutdown.
  When nobody on the server is gathering, every spot is gone within about a
  minute.

Right-clicking a spot's block with the main hand while in gathering mode (or
admin mode) gathers it. The plugin chooses one weighted category, rolls the
configured number of drops from it, and pops the items out of the spot. The first
player to click gets the drops. Harvesting removes the spot and depletes its
chunk. If nothing can be rolled, the player sees "Nothing to gather here." and
the spot remains. Interactions already cancelled by another plugin are ignored.

## Configuration files

The plugin copies its defaults into `plugins/Gathering/` on first start.

| File | Purpose |
| --- | --- |
| `config.yml` | Per-world chunk bounds (`worlds.<world>.chunk-x-min` and so on), `mode` (drain, status bar, messages), `spawn`, `spot`, `freshness`, the particle ring, and gather effects. |
| `categories.yml` | Named drop categories. Each is a `drops` list (or a bare list) of `<item-path> <min>-<max> <weight>` lines. |
| `spot-types.yml` | Spot types with optional `biome` list, `altitude-min`, `altitude-max`, `spawn-block`, `particle-dust`, `spawn-weight` (default 1; 0 never spawns naturally), `provinces`, and weighted `categories` entries (`id`, `weight`, and `drops` as `N` or `min-max` rolls). |

`provinces` is a list of SimpleFactions province ids. A type with the list only
spawns where the province map returns one of those ids, on top of its other
rules. If SimpleFactions or its province map is unavailable, those types never
spawn and the plugin logs one warning at load. A list with no valid ids means the
type never spawns.

Item paths are resolved through TLibs, so they use the prefixes understood by
TLibs and the installed item providers. Biomes use Minecraft biome keys, and
blocks use Bukkit material names. Unknown biomes, materials, province ids, and
malformed drop lines are logged and skipped. Category references are not checked
at load time.

Settings from before gathering mode (`spawn-interval-minutes`,
`chunk-cooldown-minutes`, `spawn-attempts-per-tick`, `probe-column-attempts`,
`passive-discovery`, `attributes`, `profession`, and the per-type `profession-id`,
`max-active`, and `cooldown-minutes`) are ignored, with one warning per file.

Run `/gathering reload` after editing these files. Reloading re-reads all three
files, clears active spots, and restarts the timers with the new intervals.

## Commands and permissions

`/gather` needs `gathering.use` (default: everyone). All `/gathering`
subcommands require `gathering.admin`, which defaults to operators.

| Command | Effect |
| --- | --- |
| `/gather [on\|off]` | Toggle or set gathering mode. |
| `/gathering reload` | Reload the three files, clear active spots, and restart the timers. |
| `/gathering status` | Show active spots, players gathering, tracked chunks, and how many are below 50% freshness. |
| `/gathering forcespawn [spotType]` | Spawn a spot near the player, skipping the chance, cap, freshness, and world-bound checks. Surface and province rules still apply. |
| `/gathering freshness` | Show the depletion and freshness of the player's current chunk. |
| `/gathering clearcache [world]` | Reset chunk depletion for one world, or for all worlds. |
| `/gathering adminmode [on\|off]` | Toggle or set admin mode, which shows every nearby spot with an extra marker and allows gathering outside gathering mode. |

Admin mode is held in memory and ends when the player leaves or the server stops.

## Persistence and shutdown

- Chunk depletion is stored in `plugins/Gathering/Data/chunk-cache.json` as a
  value and last-update time per chunk. Entries that have decayed below 0.05 are
  dropped when saving. Changed state is written every 60 seconds and on a normal
  plugin disable; a failed write is retried.
- Spots and gathering mode are not saved. Files from older versions are handled
  on start: `Data/spots.json` is renamed to `spots.json.old` once, and the old
  `cooldowns` and `excluded` sections of `chunk-cache.json` are ignored and dropped
  on the next save.

## Validation

For a server-side change, verify the following on Paper 1.21.10 with the pinned
dependency set:

1. Start with both an empty data directory and data from an older version, and
   confirm the migration messages and that all definitions load without
   warnings.
2. With two characters, turn on gathering mode and confirm the Mental Point
   charges, the boss bar, and that running out ends the mode.
3. Confirm spots spawn near gatherers up to the cap, that both gatherers see the
   same spots, and that a player outside the mode sees none.
4. Gather a spot and check the drops, `/gathering freshness`, and
   `/gathering status`.
5. Force-spawn a province-limited type inside and outside its provinces.
6. Turn the mode off and confirm the spots disappear after the grace period.
7. Exercise `adminmode`, `clearcache`, and `reload`.
