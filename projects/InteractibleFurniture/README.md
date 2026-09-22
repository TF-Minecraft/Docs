# InteractibleFurniture

[Source repository](https://github.com/TF-Minecraft/InteractibleFurniture) · [All projects](../../README.md)

Configurable furniture interactions and persistence, with integrations used by Magic and Thievery.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

Published Java 21 replacement: [0.1.4-BETA](https://github.com/TF-Minecraft/InteractibleFurniture/releases/tag/v0.1.4-BETA), verified locally. See the [replacement release status](../../PLATFORM.md#java-21-dependency-replacements) for provenance, verification and deployment status.

## Build and dependencies

Use JDK 21 and `mvn clean verify` from the source checkout. Install the compatible
TLibs 1.1.1 build in local Maven; prepare the authorized private inputs in `libs/`
with `.github/scripts/prepare-release.sh` and verify `.github/dependencies.sha256`.
The replacement release source at `v0.1.4-BETA` uses the Maven Spigot 1.21.10
API and produces `target/interactiblefurniture-0.1.4-BETA.jar`. Its clean Java 21 build passes;
server behavior still needs validation against the intended dependencies.

The plugin manifest requires TLibs and MythicMobs. ProtocolLib is also a build
input; resolve the exact runtime integration versions with the shared baseline.

## Configuration and operations

The entrypoint seeds `furniture/example.yml`, `furniture/magic.yml`,
`furniture/cooking.yml`, `furniture/shelf.yml` and `sounds.yml` in the plugin data
folder. It loads all YAML files directly under `furniture/`, starts the furniture
manager and restores furniture from already loaded chunks. Shutdown removes
carried furniture and saves loaded chunks.

`/if reload` reloads furniture and sounds with `interactiblefurniture.reload`.
`/if debug <on|off>` controls interaction debug particles with
`interactiblefurniture.debug`. Both permissions default to operators. The command
also exposes `/if nested attach` and `/if nested detach` for nested furniture.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
