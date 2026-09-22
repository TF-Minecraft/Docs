# PermCleaner

[Source repository](https://github.com/TF-Minecraft/PermCleaner) · [All projects](../../README.md)

Removes obsolete player permissions through LuckPerms while preserving configured permissions and tracking completed cleanups.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Run Maven with **JDK 21** from the source checkout. The POM sets `maven.compiler.release=21` and resolves `org.spigotmc:spigot-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope from Spigot snapshots. The plugin descriptor declares `api-version: 1.21.10`.

Install these matching Java 21 TFMC artifacts into local Maven before building: `me.plugins:tlibs:1.1.1`. Use the [shared installer](../TLibs/README.md) for published dependencies, or `mvn clean install` from matching source versions. CI uses the shared dependency setup actions.

No private `libs/` JARs are required by this POM.

Run `mvn clean verify` to build and run the available tests; use `mvn clean install` when another plugin needs the result as a Maven dependency. The plugin JAR is written under `target/`. Gameplay and web integration checks on the Minecraft 1.21.10 server remain separate from build verification.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
