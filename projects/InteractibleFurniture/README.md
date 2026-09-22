# InteractibleFurniture

[Source repository](https://github.com/TF-Minecraft/InteractibleFurniture) · [All projects](../../README.md)

Configurable furniture interactions and persistence, with integrations used by Magic and Thievery.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

See the [shared API versions](../../PLATFORM.md#shared-api-versions) for the matching provider dependency set.

## Build and dependencies

Use JDK 21 and `mvn clean verify` from `main`. Install the TLibs version
declared in `pom.xml` with the [shared installer](../TLibs/README.md) in pinned
mode. Prepare the private inputs in `libs/` with
`.github/scripts/prepare-release.sh` and verify `.github/dependencies.sha256`.
The POM uses the Paper 1.21.10 API and writes the JAR under `target/` using
its declared version. Validate server behavior against the intended dependencies.

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
