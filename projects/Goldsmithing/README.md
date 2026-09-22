# Goldsmithing

[Source repository](https://github.com/TF-Minecraft/Goldsmithing) · [All projects](../../README.md)

Standalone jewelry smithing plugin. GemInfusion also contains a goldsmithing system; treat these as separate implementations when selecting a deployment.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

**Archived:** The source on `main` targets Java 21 / Minecraft 1.21.10.

Run Maven with **JDK 21** from the source checkout. The POM sets `maven.compiler.release=21` and resolves `org.spigotmc:spigot-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope from Spigot snapshots. The plugin descriptor declares `api-version: 1.21.10`.

Populate `libs/` with the exact files and hashes listed in `.github/dependencies.sha256`. `.github/scripts/prepare-release.sh` downloads those pinned private assets when supplied with the approved dependency token.

Run `mvn clean verify` to build and run the available tests; use `mvn clean install` when another plugin needs the result as a Maven dependency. The plugin JAR is written under `target/`. Gameplay and web integration checks on the Minecraft 1.21.10 server remain separate from build verification.

## Runtime and configuration

Required plugins declared by the manifest: MMOItems, MythicLib.

`Goldsmithing` loads jewelry/material definitions with `ConfigLoader` and registers `SmithingEvents`. The repository does not bundle a default `config.yml`; supply existing definitions for `smithing_block`, tools, `materials` and `jewelry`. The manifest declares no commands. Compare the [GemInfusion implementation](../GemInfusion/README.md) before enabling overlapping smithing mechanics.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
