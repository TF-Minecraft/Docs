# DenarEconomy

[Source repository](https://github.com/TF-Minecraft/DenarEconomy) · [All projects](../../README.md)

Shared currency plugin for player bank and pouch accounts, coins and money drops.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Run Maven from the source checkout. The current [POM](https://github.com/TF-Minecraft/denareconomy/blob/main/pom.xml) declares Java **release 21** and **paper-api 1.21.10-R0.1-SNAPSHOT**; [plugin.yml](https://github.com/TF-Minecraft/denareconomy/blob/main/src/main/resources/plugin.yml) declares `api-version: 1.21.10`. The build and loader metadata target the shared runtime. Gameplay validation remains separate from build verification.

Build with JDK 21. Install the matching TLibs Maven release and populate `libs/` using `.github/scripts/prepare-release.sh`, then verify `.github/dependencies.sha256` and run `mvn clean verify`. The primary output is `target/denareconomy-0.1.9.jar`. The current CI workflow records the exact dependency setup.

## Runtime and configuration

Required plugins declared by the manifest: MMOItems, MythicLib, TLibs.

Startup loads `coins.yml`, `drops.yml` and `messages.yml`, registers money/player listeners and starts the player manager. `/deco` and `/pouch` are the entry commands; config reload uses `denareconomy.reload` (op by default). Preserve the plugin data directory, including `Data` and `PlayerData`, when changing builds. Consumers should use the existing money/player manager API rather than maintain a second balance store.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, dependency selection and rollback.
