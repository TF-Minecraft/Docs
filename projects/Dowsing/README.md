# Dowsing

[Source repository](https://github.com/TF-Minecraft/Dowsing) · [All projects](../../README.md)

Resource discovery and configurable production nodes tied to SimpleFactions guilds.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Dowsing builds with Java **21** against
`io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT`. Install the pinned TLibs
`2.0.0`, SimpleFactions `3.0.0`, and Magic `0.2.0` release artifacts with
the shared dependency installer. The build also prepares checksum-verified
ItemsAdder, MMOItems, MythicLib, and json-simple inputs from the private
ServerAssets repository.

At runtime, `plugin.yml` requires TLibs, SimpleFactions, MMOItems, MythicLib,
and ItemsAdder. Magic is optional; configured Magic artifact paths are only
resolved when that plugin is present.

## Guides

- [Behavior, configuration, and operations](overview.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts,
release tags, private dependency access, and release verification.
