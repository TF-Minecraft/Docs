# TFMCCore

[Source repository](https://github.com/TF-Minecraft/TFMCCore) · [All projects](../../README.md)

Technical documentation is maintained here. Run commands from the source checkout unless a guide says otherwise.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

- [Overview](overview.md)
- [Shared feature ownership](ownership.md)
- [Three-part resource-pack delivery](resource-pack.md)
- [Statistics architecture](src/main/java/net/tfminecraft/tfmccore/stats/ARCHITECTURE.md)
- [Statistics configuration and commands](src/main/java/net/tfminecraft/tfmccore/stats/STATS.md)
- [Player commands](src/main/java/net/tfminecraft/tfmccore/tfmc/TFMC.md)

The POM pins TLibs **2.4.1** and SimpleFactions **4.0.0**. Battle participation
remains an account UUID integration; the character migration preserves that
event contract.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
