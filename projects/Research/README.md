# Research

[Source repository](https://github.com/TF-Minecraft/Research) · [All projects](../../README.md)

Lectern research stations where characters run item experiments to uncover hidden aspects and research results.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Research builds with Java **21** against
`io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT`. Install the pinned TLibs
`2.0.1` and RPCharacters `2.1.0` release artifacts with the shared dependency
installer. The build also prepares checksum-verified MMOCore `1.13.1` and
MythicLib `1.7` inputs from the private ServerAssets repository.

At runtime, `plugin.yml` requires MMOItems, MythicLib, ItemsAdder, TLibs, and
RPCharacters. The code reaches MMOItems and ItemsAdder only through TLibs item
paths. MMOCore is declared as a soft dependency, but the discovery attribute
lookup calls MMOCore classes directly, so install MMOCore wherever Research
runs.

## Guides

- [Behaviour, configuration, and operations](overview.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts,
release tags, private dependency access, and release verification.

## Shared feature ownership

See [feature ownership and migration](../TFMCCore/ownership-migration.md) for scanner, focus and letter APIs, coordinated upgrades, and rollback.
