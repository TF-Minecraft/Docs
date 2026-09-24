# AdvancedCrafting

[Source repository](https://github.com/TF-Minecraft/AdvancedCrafting) · [All projects](../../README.md)

AdvancedCrafting supplies ingredient conversion, station crafting, smithing hits,
alloy discovery and MMOItems stat/provenance updates. The imported source is by
Drefvelin.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

See the [shared API versions](../../PLATFORM.md#shared-api-versions) for the matching provider dependency set.

- [Setup, builds and releases](setup.md)
- [Configuration and commands](configuration.md)
- [Architecture, data and integrations](architecture.md)
- [Verification and operations](verification.md)
- [Organisation pipeline guide](../../PIPELINES.md)

## Source references

- [Source README and build commands](https://github.com/TF-Minecraft/AdvancedCrafting/blob/main/README.md)
- [Maven dependencies and packaging](https://github.com/TF-Minecraft/AdvancedCrafting/blob/main/pom.xml)
- [Descriptor and default configuration](https://github.com/TF-Minecraft/AdvancedCrafting/tree/main/src/main/resources)

Build with JDK 21 and `mvn clean verify` after preparing private dependencies and
installing the pinned TLibs.
