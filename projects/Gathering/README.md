# Gathering

[Source repository](https://github.com/TF-Minecraft/Gathering) · [All projects](../../README.md)

An active gathering activity: characters spend Mental Points to search their surroundings for spots that they harvest for weighted drops.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Gathering builds with Java **21** against
`io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT`. Install the pinned TLibs
`2.3.0`, RPCharacters `2.16.0`, and SimpleFactions `4.7.0` release artifacts with
the shared dependency installer. The tests also need checksum-verified MMOCore
`1.13.1-SNAPSHOT` and MythicLib `1.7.1-SNAPSHOT` from the private ServerAssets
repository, because RPCharacters classes reference them; they are test-scoped and
not used by Gathering at runtime.

At runtime, `plugin.yml` requires TLibs and RPCharacters. Character identity comes
from the [shared TLibs session API](../TLibs/character-identity.md). Gathering mode
spends RPCharacters Mental Points (focus), and the spawn chance uses wisdom and
intelligence from the RPCharacters character sheet. SimpleFactions is a soft
dependency: it supplies the province map for spot types limited to provinces.

## Guides

- [Behaviour, configuration, and operations](overview.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts,
release tags, private dependency access, and release verification.
