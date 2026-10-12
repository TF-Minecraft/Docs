# Magic

[Source repository](https://github.com/TF-Minecraft/Magic) · [All projects](../../README.md)

Technical documentation is maintained here. Run commands from the source checkout unless a guide says otherwise.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

- [Mage gear](docs/MAGE_GEAR.md)
- [docs/SYSTEM.md](docs/SYSTEM.md)
- [docs/TEST_MATRIX.md](docs/TEST_MATRIX.md)

## Build and dependencies

Build from `main` with Java 21. Install the TLibs, RPCharacters, and
InteractibleFurniture releases pinned in the
[POM](https://github.com/TF-Minecraft/Magic/blob/main/pom.xml) using the
[shared dependency installer](../../PIPELINES.md#build-dependencies), then run
`bash .github/scripts/prepare-release.sh` with ServerAssets access to install
the checksum-verified private inputs. Run `mvn clean verify`; the output is
`target/magic-<version>.jar`.

The plugin descriptor requires TLibs, ItemsAdder, RPCharacters, and
InteractibleFurniture. MMOItems, MythicLib, and MMOCore are optional integrations
in the descriptor; the corresponding gear and casting features need their
providers. The build compiles against Paper API `1.21.10-R0.1-SNAPSHOT`.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.

## Shared feature ownership

See [shared feature ownership](../TFMCCore/ownership.md) for scanner, focus and letter APIs, configuration, and verification.
