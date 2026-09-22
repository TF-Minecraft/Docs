# Archaeo

[Source repository](https://github.com/TF-Minecraft/Archaeo) · [All projects](../../README.md)

Archaeo provides archaeology, hidden ruins, excavation, and fragile finds for TFMC Minecraft servers. It is actively used.

## Build and configuration

From the source checkout, use Java 21 and run `mvn clean verify`. The JAR is written to `target/Archaeo-<version>.jar`.

- [Plugin commands and permissions](https://github.com/TF-Minecraft/Archaeo/blob/main/src/main/resources/plugin.yml)
- [Default configuration and catalogs](https://github.com/TF-Minecraft/Archaeo/tree/main/src/main/resources)
- [Optional custom pack and installation](https://github.com/TF-Minecraft/Archaeo/blob/main/pack/README.md)
- [Gameplay loop](https://github.com/TF-Minecraft/Archaeo/blob/main/pack/GAMEPLAY.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md). Pull requests and pushes to `main` build dated development JARs; matching numeric `v*` tags create draft releases with checksums.
