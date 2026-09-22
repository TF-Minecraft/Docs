# DrinkBuilder

[Source repository](https://github.com/TF-Minecraft/DrinkBuilder) · [All projects](../../README.md)

Synchronizes drink ingredients and approved drink packs between Minecraft and the web service.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Run Maven with **JDK 21** from the source checkout. The POM sets `maven.compiler.release=21` and resolves `org.spigotmc:spigot-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope from Spigot snapshots. The plugin descriptor declares `api-version: 1.21.10`.

Install these matching Java 21 TFMC artifacts into local Maven before building: `me.plugins:tlibs:1.1.1`. Use the [shared installer](../TLibs/README.md) for published dependencies, or `mvn clean install` from matching source versions. CI uses the shared dependency setup actions.

Populate `libs/` with the exact files and hashes listed in `.github/dependencies.sha256`. `.github/scripts/prepare-release.sh` downloads those pinned private assets when supplied with the approved dependency token.

Run `mvn clean verify` to build and run the available tests; use `mvn clean install` when another plugin needs the result as a Maven dependency. The plugin JAR is written under `target/`. Gameplay and web integration checks on the Minecraft 1.21.10 server remain separate from build verification.

## Runtime and configuration

Startup loads `config.yml`, `ingredients.yml`, `effects-blacklist.yml`, `categories.yml` and `permission-groups.yml`, then uploads the catalog and texture assets and starts pack polling. `/drinkbuilder` requires `drinkbuilder.admin` (op by default). TLibs and TFMCWeb are required; ItemsAdder is declared optional and supplies the custom pack integration. See the drinks workflow for service configuration.

## Guides

- [Drink texture assets](src/main/resources/assets/README.md)
- [Drinks workflow and integration](../ProvinceSystem/docs/cosmetics/drinks.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
