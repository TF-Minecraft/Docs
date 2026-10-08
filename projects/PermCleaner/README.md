# PermCleaner

[Source repository](https://github.com/TF-Minecraft/PermCleaner) · [All projects](../../README.md)

Removes obsolete player permissions through LuckPerms while preserving configured permissions and tracking completed cleanups.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Run Maven with **JDK 21** from the source checkout. The POM sets `maven.compiler.release=21` and resolves `io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope from the PaperMC Maven repository. The plugin descriptor declares `api-version: 1.21.10`.

Install the pinned `me.plugins:tlibs:2.0.0` artifact into local Maven with the [shared installer](../../PIPELINES.md#build-dependencies). LuckPerms API `5.4` resolves from Maven; the running server requires both TLibs and LuckPerms. CI uses the shared dependency setup action.

No private `libs/` JARs are required by this POM.

Run `mvn clean verify` to build and run the tests; use `mvn clean install` when another plugin needs the result as a Maven dependency. The plugin JAR is written under `target/`. Live LuckPerms cleanup and storage checks on the Minecraft 1.21.10 server remain separate from build verification.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
