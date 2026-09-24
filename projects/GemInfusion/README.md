# GemInfusion

[Source repository](https://github.com/TF-Minecraft/GemInfusion) · [All projects](../../README.md)

Gem infusion, socket rarity preservation and the integrated goldsmithing project system.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Run `mvn clean verify` with JDK 21 from the source checkout. The POM
uses **release 21**, resolves **Paper API 1.21.10-R0.1-SNAPSHOT** from Maven,
and declares `api-version: 1.21.10` in the plugin manifest.

Install the TLibs version declared in `pom.xml` using the
[shared installer](../TLibs/README.md) in pinned mode; CI uses the shared setup action.
Prepare the authorized private jars in `libs/` with
`.github/scripts/prepare-release.sh` and verify `.github/dependencies.sha256`.
These supply Gson, MMOCore, MMOItems and MythicLib; TLibs and the server API
are Maven dependencies. Output is `target/geminfusion-<version>.jar`.

Gameplay validation remains separate from compilation; follow the
[shared baseline](../../PLATFORM.md) for build and validation requirements.

## Runtime and configuration

Required plugins declared by the manifest: TLibs, MMOItems, MythicLib.

`InfusionMain` loads `config.yml`, `goldsmithing.yml` and the `goldsmithing/` definitions for hits, materials, tiers, qualities and projects. It loads persisted stations, flushes them periodically and on shutdown, and registers socket/unsocket listeners. `/geminfusion reload` reloads definitions and stations; `/geminfusion select <projectId>` selects a project. Admin access uses `geminfusion.admin`; goldsmithing gameplay uses `professions.goldsmith` (false by default).

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
