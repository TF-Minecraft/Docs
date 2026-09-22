# BarterShops

[Source repository](https://github.com/TF-Minecraft/BarterShops) · [All projects](../../README.md)

Sign-based item shops with barter, DenarEconomy payments and faction embargo checks.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Run Maven with **JDK 21** from the source checkout. The POM sets `maven.compiler.release=21` and resolves `org.spigotmc:spigot-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope from Spigot snapshots. The plugin descriptor declares `api-version: 1.21.10`.

Install these matching Java 21 TFMC artifacts into local Maven before building: `net.tfminecraft:denareconomy:0.2.0`, `net.tfminecraft:simplefactions:3.0.0`. Their source repositories use `mvn clean install`; CI uses the pinned dependency setup actions.

Populate `libs/` with the exact files and hashes listed in `.github/dependencies.sha256`. `.github/scripts/prepare-release.sh` downloads those pinned private assets when supplied with the approved dependency token.

Run `mvn clean verify` to build and run the available tests; use `mvn clean install` when another plugin needs the result as a Maven dependency. The plugin JAR is written under `target/`. Gameplay and web integration checks on the Minecraft 1.21.10 server remain separate from build verification.

## Runtime and configuration

Required plugins declared by the manifest: MMOItems, MythicLib.

`ShopEvents` handles sign interactions and calls DenarEconomy directly for currency trades; install DenarEconomy even though the current manifest omits it. `ShopEmbargo` provides the SimpleFactions integration. Shop JSON lives under `plugins/BarterShops/Data`; preserve it across upgrades. The manifest declares no commands.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
