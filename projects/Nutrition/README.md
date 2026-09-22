# Nutrition

[Source repository](https://github.com/TF-Minecraft/Nutrition) · [All projects](../../README.md)

Tracks player nutrition and diet variety using configured food groups and nutrition levels.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

**Archived:** The source on `main` targets Java 21 / Minecraft 1.21.10.

Run Maven with **JDK 21** from the source checkout. The POM sets `maven.compiler.release=21` and resolves `org.spigotmc:spigot-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope from Spigot snapshots. The plugin descriptor declares `api-version: 1.21.10`.

Install the TLibs version declared in `pom.xml` using the
[shared installer](../TLibs/README.md) with `--mode pinned`. See the
[shared API versions](../../PLATFORM.md#shared-api-versions).

Populate `libs/` with the exact files and hashes listed in `.github/dependencies.sha256`. `.github/scripts/prepare-release.sh` downloads those pinned private assets when supplied with the approved dependency token.

Run `mvn clean verify` to build and run the available tests; use `mvn clean install` when another plugin needs the result as a Maven dependency. The plugin JAR is written under `target/`. Gameplay and web integration checks on the Minecraft 1.21.10 server remain separate from build verification.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
