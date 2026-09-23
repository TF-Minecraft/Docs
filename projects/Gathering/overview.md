# Behaviour, configuration, and operations

[Gathering documentation](README.md) · [All projects](../../README.md)

## System model

Gathering places invisible spots on existing surface blocks. A spot records its
world, block position, spot type, surface material, and the RPCharacters
characters that have discovered it. Each chunk holds at most one active spot.
Spots do not expire; a spot stays in place until someone gathers it.

Every `spawn-interval-minutes`, the scheduler makes up to
`spawn-attempts-per-tick` attempts in each configured world. Each attempt picks a
random spot type that is below its `max-active` limit and outside its
`cooldown-minutes` spawn cooldown. It then picks a random chunk within that
world's bounds and skips it if the chunk already holds a spot, is on cooldown, or
is excluded. Otherwise, the chunk is loaded and up to `probe-column-attempts`
random columns are scanned from the top down. The first block that is solid, has
two air blocks above it, and matches the type's surface block, altitude, and
biome filters becomes the spot. This can be below the open surface, such as on
a cave floor. If no column matches, the chunk is excluded for every spot type.

## Configuration files

The plugin copies its defaults into `plugins/Gathering/` on first start.

| File | Purpose |
| --- | --- |
| `config.yml` | Spawn interval, attempts, column probes, chunk cooldown, per-world chunk bounds (`worlds.<world>.chunk-x-min` and so on), passive discovery, attribute and profession weights, particle ring, and gather effects. |
| `categories.yml` | Named drop categories. Each is a `drops` list (or a bare list) of `<item-path> <min>-<max> <weight>` lines. |
| `spot-types.yml` | Spot types with optional `biome` list, `altitude-min`, `altitude-max`, `spawn-block`, and `particle-dust`, plus `max-active`, `cooldown-minutes`, `profession-id`, and weighted `categories` entries (`id`, `weight`, and `drops` as `N` or `min-max` rolls). |

Item paths are resolved through TLibs, so they use the prefixes understood by
TLibs and the installed item providers. Biomes use Minecraft biome keys, and
blocks use Bukkit material names. Unknown biomes, materials, and malformed drop
lines are logged and skipped. Category references are not checked at load time.

Run `/gathering reload` after editing these files. Reloading re-reads all three
files but does not restart the scheduled tasks, so changes to
`spawn-interval-minutes`, `passive-discovery.interval-seconds`, and
`particles.interval-ticks` only apply after a restart. Existing spots keep their
spot type identifier.

## Discovery and gathering

Only players with an active RPCharacters character take part. When
`passive-discovery.enabled` is true, every `interval-seconds` the plugin rolls
once for each undiscovered spot within `radius` blocks of each such player. The
chance is `base-chance` plus wisdom × `wisdom-weight`, intelligence ×
`intelligence-weight`, and, when `profession.enabled` is true and MMOCore is
enabled, the profession level × `level-weight`. The chance is capped at 100%. The
profession is the spot type's `profession-id`, or `profession.id` when that is
not set. On success, the character is recorded against the spot and receives the
configured message.

Discovered spots within 32 blocks (or `radius`, if larger) show a two-particle
ring coloured by `particle-dust` or the surface block. Right-clicking the spot's
block with the main hand gathers it. The plugin chooses one weighted category,
rolls the configured number of drops from it, and pops the items out of the spot.
Harvesting a spot removes it and puts its chunk on cooldown for
`chunk-cooldown-minutes`. If nothing can be rolled, the player sees "Nothing to
gather here." and the spot remains. Interactions already cancelled by another
plugin are ignored.

## Commands and permissions

All subcommands require `gathering.admin`, which defaults to operators.

| Command | Effect |
| --- | --- |
| `/gathering reload` | Reload `config.yml`, `categories.yml`, and `spot-types.yml`. |
| `/gathering status` | Show active spots, excluded chunks, and chunks on cooldown. |
| `/gathering clearcache [world]` | Clear excluded chunks for one world, or for all worlds. |
| `/gathering forcespawn <spotType> [chunkX chunkZ]` | Probe the player's current chunk, or the given chunk in the player's world, for the type. This ignores world bounds, `max-active`, and cooldowns. A failed probe excludes the chunk. |
| `/gathering adminmode [on\|off]` | Toggle or set admin mode. Admin mode shows every nearby spot with an extra marker and allows gathering without a discovery or character. |

Admin mode is held in memory and ends when the player leaves or the server stops.

## Persistence and shutdown

- Active spots and their character discoveries are stored in
  `plugins/Gathering/Data/spots.json`.
- Chunk cooldowns and excluded chunks, with reasons, are stored in
  `plugins/Gathering/Data/chunk-cache.json`.

Changed state is written every 60 seconds and again on a normal plugin disable.
The per-type spawn cooldown is held in memory only and resets on restart. Back up
the complete `plugins/Gathering/` directory before renaming spot types or
migrating configuration, and stop the server cleanly before copying live state.

## Validation

For a server-side change, verify the following on Paper 1.21.10 with the pinned
dependency set:

1. Start with both an empty data directory and a copy of representative existing
   spot and chunk-cache data.
2. Confirm all definitions load without unknown biome, material, drop-line, or
   item-path warnings.
3. Force-spawn each spot type, and confirm scheduled spawning respects world
   bounds, `max-active`, type cooldowns, and chunk cooldowns.
4. Discover a spot with a character, with and without MMOCore, and confirm only
   that character sees the particle ring.
5. Gather the spot, and check drops, the chunk cooldown, and `/gathering status`.
6. Exercise `adminmode`, `clearcache`, and `reload`.
7. Restart cleanly and confirm spots, discoveries, cooldowns, and excluded chunks
   are restored.
