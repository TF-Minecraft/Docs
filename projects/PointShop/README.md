# PointShop

[Source repository](https://github.com/TF-Minecraft/PointShop) · [All projects](../../README.md)

Provides configurable point currencies and item trades through `/pointshop`.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

**Temporarily reopened:** The verified Java 21 / Minecraft 1.21.10 migration is pushed in [PR #6](https://github.com/TF-Minecraft/PointShop/pull/6) and awaits the required independent review. Restore the repository’s archived state after the migration is merged; it has not been deployed.

Run Maven with **JDK 21** from the source checkout. The POM sets `maven.compiler.release=21` and resolves `org.spigotmc:spigot-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope from Spigot snapshots. The plugin descriptor declares `api-version: 1.21.10`.

Use the Java 21 replacement `me.plugins:tlibs:1.1.1`. The shared installer in
`--mode latest` selects the published replacement and updates the consumer
version property; an explicitly pinned build must set `tlibs.version=1.1.1`. See the
[replacement release status](../../PLATFORM.md#java-21-dependency-replacements).

Populate `libs/` with the exact files and hashes listed in `.github/dependencies.sha256`. `.github/scripts/prepare-release.sh` downloads those pinned private assets when supplied with the approved dependency token.

Run `mvn clean verify` to build and run the available tests; use `mvn clean install` when another plugin needs the result as a Maven dependency. The plugin JAR is written under `target/`. Gameplay and web integration checks on the Minecraft 1.21.10 server remain separate from build verification.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
