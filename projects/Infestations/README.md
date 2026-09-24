# Infestations

[Source repository](https://github.com/TF-Minecraft/Infestations) · [All projects](../../README.md)

Province-scale MythicMobs infestations with ambient spawning, lure raids, and optional spread between SimpleFactions provinces.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Infestations builds with Java **21** against
`io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT`. Install the pinned TLibs
`2.0.1`, SimpleFactions `3.0.2`, and InteractibleFurniture `0.2.1` release
artifacts with the shared dependency installer. The build also prepares a
checksum-verified MythicMobs `5.13.1-SNAPSHOT` input from the private
ServerAssets repository.

At runtime, `plugin.yml` requires TLibs, SimpleFactions, MythicMobs,
ItemsAdder, and InteractibleFurniture. The plugin code does not call ItemsAdder
directly; the default lure is an ItemsAdder item (`ia.tfmc:lure`) placed as
InteractibleFurniture.

## Guides

- [Behaviour, configuration, and operations](overview.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts,
release tags, private dependency access, and release verification.
