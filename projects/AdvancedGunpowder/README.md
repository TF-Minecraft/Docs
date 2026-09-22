# AdvancedGunpowder

[Source repository](https://github.com/TF-Minecraft/AdvancedGunpowder) · [All projects](../../README.md)

Musket firing, ammunition, reload timing and armour interactions backed by MMOItems and MMOCore.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

**Temporarily reopened:** The verified Java 21 / Minecraft 1.21.10 migration is pushed in [PR #4](https://github.com/TF-Minecraft/AdvancedGunpowder/pull/4) and awaits the required independent review. Restore the repository’s archived state after the migration is merged; it has not been deployed.

Run Maven with **JDK 21** from the source checkout. The POM sets `maven.compiler.release=21` and resolves `org.spigotmc:spigot-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope from Spigot snapshots. The plugin descriptor declares `api-version: 1.21.10`.

Populate `libs/` with the exact files and hashes listed in `.github/dependencies.sha256`. `.github/scripts/prepare-release.sh` downloads those pinned private assets when supplied with the approved dependency token.

Run `mvn clean verify` to build and run the available tests; use `mvn clean install` when another plugin needs the result as a Maven dependency. The plugin JAR is written under `target/`. Gameplay and web integration checks on the Minecraft 1.21.10 server remain separate from build verification.

## Runtime and configuration

Required plugins declared by the manifest: MMOCore, MMOItems, MythicLib.

`GunpowderMain` loads weapon definitions through `ConfigLoader` and registers `GunpowderEvents` and `/agp`. The source does not bundle a `config.yml`: supply the existing server configuration, including `handweapons`, before enabling it. See [GunsAndGadgets](../GunsAndGadgets/README.md) for the replacement project; this page does not establish that AdvancedGunpowder is currently deployed.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
