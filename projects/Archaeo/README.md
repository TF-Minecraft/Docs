# Archaeo

[Source repository](https://github.com/TF-Minecraft/Archaeo) · [All projects](../../README.md)

Archaeo provides archaeology, hidden ruins, excavation, and fragile finds for TFMC Minecraft servers. It is actively used.

## Build and configuration

Use the shared [Java 21 / Minecraft 1.21.10 platform baseline](../../PLATFORM.md).
From the source checkout, run `mvn clean verify`. The JAR is written to
`target/archaeo-<version>.jar`.

- [Plugin commands and permissions](https://github.com/TF-Minecraft/Archaeo/blob/main/src/main/resources/plugin.yml)
- [Default configuration and catalogs](https://github.com/TF-Minecraft/Archaeo/tree/main/src/main/resources)
- [Configuration ownership and TFMC installation](docs/configuration.md)
- [Optional custom pack and installation](docs/pack-installation.md)
- [Gameplay guide and default tools](docs/gameplay.md)
- [Custom-pack player guide](docs/pack-gameplay.md)
- [Lore catalog editing](docs/lore-catalogs.md)
- [Original design reference (Spanish)](docs/concepto.md) — includes proposals;
  it does not establish implemented behavior.

Technical guides live here. Plugin code, bundled YAML defaults, and optional
pack assets stay in [Archaeo](https://github.com/TF-Minecraft/Archaeo). TFMC-specific
settings and lore catalogs live in private
[ServerAssets](https://github.com/TF-Minecraft/ServerAssets/tree/main/configs/Archaeo).

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md). Pull requests and pushes to `main` build dated development JARs; matching numeric `v*` tags create draft releases with checksums.
