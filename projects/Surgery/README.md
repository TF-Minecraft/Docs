# Surgery

[Source repository](https://github.com/TF-Minecraft/Surgery) · [All projects](../../README.md)

Technical documentation is maintained here. Run commands from the source checkout unless a guide says otherwise.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

Build with Java 21 and pinned TLibs **2.3.0** / RPCharacters **2.16.0** release
artifacts. The shared dependency installer prepares them before `mvn clean
verify`. Runtime requires those versions or newer; see the installation and
lifecycle guidance below.

- [Project overview](overview.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
