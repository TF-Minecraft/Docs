> Canonical documentation: [TF-Minecraft/docs](https://github.com/TF-Minecraft/docs). [Source snapshot](https://github.com/TF-Minecraft/rpcharacters/blob/9e2d9f0d7ca9e7080f0748a654eab535c2c9c663/docs/graves-system/01-config-and-tracker.md). Commands and plain-text code/config paths refer to the source repository unless stated otherwise.

# Batch 1 - Config and last-solid tracker

## Files

- `rpcharacters/src/main/resources/graves.yml` (default resource)
- `grave/GraveLoader.java` - read YAML into static fields (or `Cache` graves section)
- `grave/LastSolidTracker.java` - runnable 20 ticks (config)
- `RPCharacters.createConfigs()` add `"graves.yml"`
- `loadConfigs()` + `onEnable` start tracker; `onDisable` stop

## Tracker

Map `UUID -> Location` (block location of last solid). Update only when the candidate is solid. Clear on quit optional (keep last for death after crash in same session only; persist not required).

Used only when the death column is empty (air/void with no solid and no water below). Ground deaths place on the ground at the death column. Water deaths replace the water at the death block. Last-solid is the void fallback.

## Done when

Config loads; walking dirt then falling into void still has a last solid location in memory.
