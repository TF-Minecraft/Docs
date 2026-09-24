# TrialRooms

[Source repository](https://github.com/TF-Minecraft/TrialRooms) · [All projects](../../README.md)

Keyed dungeon entrances, levelled MythicMobs spawner encounters, and key-opened loot chests.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

TrialRooms builds with Java **21** against
`io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT`. Install the pinned TLibs
`2.0.1` and DenarEconomy `0.2.1` release artifacts with the shared dependency
installer. The build also prepares a checksum-verified MythicMobs
`5.13.1-SNAPSHOT` input from the private ServerAssets repository.

At runtime, `plugin.yml` requires MythicMobs, TLibs, and DenarEconomy. Magic is
not declared; `magic.` item paths in loot tables only resolve when Magic is
installed.

## Guides

- [Behaviour, configuration, and operations](overview.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts,
release tags, private dependency access, and release verification.
