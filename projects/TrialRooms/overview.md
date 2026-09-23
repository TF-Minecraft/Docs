# Behaviour, configuration, and operations

[TrialRooms documentation](README.md) · [All projects](../../README.md)

## System model

TrialRooms builds combat rooms from in-world parts placed with the edit tool.
An **entrance** is a lodestone with a key item, a destination, and an optional
exit lodestone. A **spawner** is a block matching a `spawners.yml` definition,
with its own MythicMobs mob, amount, level, radii, cooldown, loot tables, and
**door blocks** that are present only while its encounter runs. **Loot chests**
open with keys and are either bound to a spawner or independent. Spawners cycle
through Idle, Active, Unlocking, and Cooldown. Text-display holograms label
spawners, chests, entrances, and exits while a player is within 96 blocks.

## Configuration files

The plugin copies missing defaults into `plugins/TrialRooms/` on start and never
overwrites existing files. There is no reload command; restart after editing.

| File | Purpose |
| --- | --- |
| `config.yml` | Edit tool, key items, loot size, level scaling, key rarity model, mob-key chances, and Denar conversions. |
| `spawners.yml` | Spawner definitions: each top-level key sets a TLibs `block` path (default `v(spawner)`). |
| `loot-tables.yml` | Named loot tables used by spawner and mob keys. |

Settings read from `config.yml`, with the defaults used when a key is absent:

| Key | Default | Effect |
| --- | --- | --- |
| `edit-tool` | `v.blaze_rod` | TLibs item path of the administrator edit tool. |
| `spawner-key`, `mob-key` | `v.tripwire_hook` | Base items for spawner keys and mob keys. |
| `max-loot` | `24` | Maximum distinct loot entries recorded on a key. |
| `health-per-level`, `damage-per-level` | `10.0`, `0.5` | Extra mob health and extra damage to players per spawner level. |
| `mob-key-base-chance`, `mob-key-chance-per-level`, `mob-key-max-chance` | `0.02`, `0.0015`, `0.25` | Mob-key drop chance per spawner mob death. |
| `common-chance` … `legendary-chance` | `70`, `20`, `7`, `2.8`, `0.2` | Base key rarity weights. |
| `rarity-weight-model` | `EXP` | `LINEAR`, `EXP`, or `LOGISTIC` level scaling of rarity weights. |
| `rarity-*`, `jitter-max` | see [source](https://github.com/TF-Minecraft/TrialRooms/blob/main/src/main/java/net/tfminecraft/trialrooms/loader/ConfigLoader.java) | Model tuning; `rarity-bias-per-level` also sets loot-table level bias. |
| `conversions` | none | Lines of `<item-path> <denar-per-item>`. |
| `debug` | `false` | Broadcasts a 10,000-key rarity simulation instead of dropping spawner keys. |

The shipped `config.yml` contains `bias-per-level`, which is not read.

A loot table is either a list of `<item-path> <min>-<max> <weight> [tier]` lines,
or a section with that list under `drops` and `amounts` lines of
`<key-rarity> <min>-<max>`. Tiers are `bad`, `common` (the default), `uncommon`,
`rare`, `epic`, and `legendary`. `amounts` sets how many items a key of each
rarity releases; without it a key releases 2–4. The default `artifact_test` table
uses `magic.` paths, which need Magic installed.

## Building a room

Hold the edit tool and right-click a block matching a spawner definition to
create or reopen its editor, a lodestone to register or reopen an entrance, or
an unregistered chest to register an independent loot chest. New entrances must
be at least 4 blocks from other entrances, exits, and destinations.

The spawner editor sets the MythicMobs internal mob name (not validated), amount,
level, cooldown in seconds, spawn and activation radii, loot table, mob loot
table, bound chest, and door blocks. New spawners start with `rpg_skeleton`, 1
mob, level 1, radii of 5, and a 10-second cooldown. Values are typed in chat and
`cancel` aborts. Binding a chest requires a loot table. Door blocks must be
within 32 blocks and not a chest; typing `remove` drops the latest one. The
entrance editor sets the key item path and, within 32 blocks of the entrance, a
destination block and an exit lodestone.

Breaking a spawner or registered chest requires the edit tool. Breaking an
entrance lodestone removes the entrance, and breaking an exit or destination
block clears it, with or without the tool. Edit-tool actions are not
permission-checked, so choose an item ordinary players cannot obtain.

## Encounters and keys

Right-clicking within 1.5 blocks of an entrance with its key item in the main
hand consumes one and teleports the player to the destination; stepping within
1.5 blocks of the exit returns them. An idle spawner activates when a survival
or adventure player is within its activation radius and 2 blocks vertically. It
spawns its mobs 1–3 seconds apart on spots within the spawn radius with 3×3×3
clear air over a solid 3×3 floor. If no player remains within 50 blocks, or the
chunk unloads, the mobs are removed and the spawner enters cooldown without a
key.

When every mob is dead, the spawner unlocks for about 2.5 seconds, drops a
spawner key, and enters cooldown. Bound chests appear one second into cooldown
and hide when it ends. If a mob loot table is set, each spawner mob death may
also drop a mob key.

Key rarity is rolled from the base weights and the spawner level. The key then
records up to `max-loot` distinct entries from its table, weighted by level,
tier, and key rarity, with higher tiers capped by rarity; its lore lists them
with their chances. Right-clicking a visible registered chest with any key
consumes it and releases the rolled number of distinct entries. Bound chests
stay hidden until the next cooldown; independent chests return after 5 seconds.

## Dungeon rules and conversions

Players count as inside after using an entrance, being in range when a spawner
activates, or taking damage from a spawner mob. Inside players do not regenerate
health from saturation and cannot damage each other. Leaving through the exit,
dying, or disconnecting clears the flag.

Items matching a `conversions` line gain "converts on exit" lore when picked up.
Leaving through the exit removes them and credits their Denar value through
DenarEconomy. When any player dies, convertible items are removed from their
drops and inventory.

## Commands and permissions

| Command | Permission | Effect |
| --- | --- | --- |
| `/tr resetcooldowns` | `trialrooms.admin` | Set every cooling-down spawner to one second remaining. |

`/tr` is player-only and has no tab completion. `plugin.yml` declares no
permissions, so `trialrooms.admin` falls back to the operator default.

## Persistence and shutdown

- Spawners, including state, cooldown, and doors:
  `plugins/TrialRooms/data/spawners/<uuid>.json`.
- Loot chests: `plugins/TrialRooms/data/chests/<uuid>.json`.
- Entrances: `plugins/TrialRooms/data/entrances/entrance_<world>_<x>_<y>_<z>.json`.

Spawners and chests are written only on a normal plugin disable. Entrances are
autosaved within 10 seconds of being registered and are written on disable.
Records that cannot be read, reference an unloaded world, or name a missing
`spawners.yml` definition are skipped at start, and saving deletes their files.
Active or unlocking spawners resume in a full cooldown; chests whose spawner is
missing load as independent.

Back up the complete `plugins/TrialRooms/` directory before renaming spawner
definitions or worlds, and stop the server cleanly before copying live state.

## Validation

For a server-side change, verify the following on Paper 1.21.10 with the pinned
dependency set:

1. Start with both an empty data directory and a copy of representative existing
   room data.
2. Confirm spawner definitions, loot tables, key items, and MythicMobs mob names
   resolve without warnings.
3. Build an entrance, exit, spawner, door blocks, bound chest, and independent
   chest with the edit tool.
4. Enter with the key item, clear the encounter, and confirm doors, level
   scaling, keys, chest opening, cooldown, healing suppression, blocked PvP,
   exit conversions, and death removal of convertible items.
5. Restart cleanly and confirm entrances, spawner settings, cooldowns, doors,
   and chests are restored.
