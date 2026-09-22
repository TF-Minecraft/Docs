# AdvancedResearch

[Source repository](https://github.com/TF-Minecraft/AdvancedResearch) · [All projects](../../README.md)

Research stations, research notes and player research progress.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

**Archived repository:** GitHub currently makes this repository read-only. The Java 21 / Minecraft 1.21.10 migration below was built and validated on the local `build/java21-mc1.21.10` branch; it has not been pushed or merged into the archived source repository.

Run Maven with **JDK 21** from the source checkout. The POM sets `maven.compiler.release=21` and resolves `org.spigotmc:spigot-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope from Spigot snapshots. The plugin descriptor declares `api-version: 1.21.10`.

Populate `libs/` with the exact files and hashes listed in `.github/dependencies.sha256`. `.github/scripts/prepare-release.sh` downloads those pinned private assets when supplied with the approved dependency token.

Run `mvn clean verify` to build and run the available tests; use `mvn clean install` when another plugin needs the result as a Maven dependency. The plugin JAR is written under `target/`. Gameplay and web integration checks on the Minecraft 1.21.10 server remain separate from build verification.

## Runtime and configuration

Required plugins declared by the manifest: MMOItems, MythicLib, ItemsAdder.

`ResearchMain` loads stations and online player records, registers research and persistence listeners, and replenishes mental points on a scheduled task. `Database` reads/writes JSON under `plugins/AdvancedResearch/Data` and `PlayerData`. Preserve those directories across upgrades. No commands or default `config.yml` are bundled; setup requires the existing research configuration and item definitions.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
