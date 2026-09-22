# ArmourShop

[Source repository](https://github.com/TF-Minecraft/ArmourShop) · [All projects](../../README.md)

Applies cosmetic skins and synchronizes approved skin packs with the web service.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Run Maven with **JDK 21** from the source checkout. The POM sets `maven.compiler.release=21` and resolves `io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope from the PaperMC Maven repository. The plugin descriptor declares `api-version: 1.21.10`.

Install these matching Java 21 TFMC artifacts into local Maven before building: `me.plugins:tlibs:2.0.0`, `net.tfminecraft:gunsandgadgets:2.0.0`. Use the [shared installer](../TLibs/README.md) for published dependencies, or `mvn clean install` from matching source versions. CI uses the shared dependency setup actions.

Populate `libs/` with the exact files and hashes listed in `.github/dependencies.sha256`. `.github/scripts/prepare-release.sh` downloads those pinned private assets when supplied with the approved dependency token.

Run `mvn clean verify` to build and run the available tests; use `mvn clean install` when another plugin needs the result as a Maven dependency. The plugin JAR is written under `target/`. Gameplay and web integration checks on the Minecraft 1.21.10 server remain separate from build verification.

## Runtime and configuration

Required plugins declared by the manifest: TLibs, ItemsAdder, TFMCWeb.

Startup loads `config.yml`, `categories.yml`, `base-sets.yml`, `permission-groups.yml` and `Categories/`, then starts pack pulling and catalog sync. `/armourshop` provides the shop and admin subcommands. `armourshop.admin` defaults to false, so grant it explicitly to administrators. Follow the integration guides below for the gateway, approval and ItemsAdder pack workflow.

## Guides

- [Web integration and pack generation](../ProvinceSystem/docs/integrations/armourshop.md)
- [Skins workflow](../ProvinceSystem/docs/cosmetics/skins.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
