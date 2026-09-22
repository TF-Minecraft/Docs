# AdvancedCrafting

[Source repository](https://github.com/TF-Minecraft/AdvancedCrafting) · [All projects](../../README.md)

AdvancedCrafting supplies ingredient conversion, station crafting, smithing hits,
alloy discovery and MMOItems stat/provenance updates. The imported source is by
Drefvelin. The first public source release is 1.2.2; the archive's Maven version
was 1.2.1 while its descriptor reported 1.0.2. Release packaging now keeps those
versions aligned without changing Java gameplay source.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

Published Java 21 replacement: [1.2.3](https://github.com/TF-Minecraft/AdvancedCrafting/releases/tag/v1.2.3), verified locally. See the [replacement release status](../../PLATFORM.md#java-21-dependency-replacements) for provenance, verification and source-review boundaries.

- [Setup, builds and releases](setup.md)
- [Configuration and commands](configuration.md)
- [Architecture, data and integrations](architecture.md)
- [Verification and operations](verification.md)
- [Organisation pipeline guide](../../PIPELINES.md)

## Source references

- [Source README and build commands](https://github.com/TF-Minecraft/AdvancedCrafting/blob/main/README.md)
- [Maven dependencies and packaging](https://github.com/TF-Minecraft/AdvancedCrafting/blob/main/pom.xml)
- [Descriptor and default configuration](https://github.com/TF-Minecraft/AdvancedCrafting/tree/main/src/main/resources)
- [Source import provenance](https://github.com/TF-Minecraft/AdvancedCrafting/blob/main/SOURCE.md)

Build with JDK 21 and `mvn clean verify` after preparing private dependencies and
installing the coordinated Java 21 TLibs build. See the shared baseline for the
published replacement versions and source-review status.
