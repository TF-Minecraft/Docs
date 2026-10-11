# Gathering

[Source repository](https://github.com/TF-Minecraft/Gathering) · [All projects](../../README.md)

Hidden world gathering spots that roleplay characters discover and harvest for weighted drops.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Gathering builds with Java **21** against
`io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT`. Install the pinned TLibs
`2.3.0` and RPCharacters `2.16.0` release artifacts with the shared dependency
installer. The build also prepares checksum-verified MMOCore `1.13.1-SNAPSHOT` and
MythicLib `1.7.1-SNAPSHOT` inputs from the private ServerAssets repository.

At runtime, `plugin.yml` requires TLibs and RPCharacters. Character identity comes
from the [shared TLibs session API](../TLibs/character-identity.md). The direct
RPCharacters dependency remains for creation-layer wisdom and intelligence;
MMOCore totals would change discovery odds. MMOCore is optional;
the profession bonus to discovery chance is only applied when that plugin is
enabled. MythicLib is a compile input only and is not declared in `plugin.yml`.

## Guides

- [Behaviour, configuration, and operations](overview.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts,
release tags, private dependency access, and release verification.
