# ActivityTF

[Source repository](https://github.com/TF-Minecraft/ActivityTF) · [All projects](../../README.md)

ActivityTF tracks daily tasks and weekly activity rewards through gameplay event hooks. Its source repository is public; the plugin name in `plugin.yml` is `activity`. Run build commands from the `activity-tf` source checkout.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Commands

Staff target completion includes known previously played players whose names are
still in Bukkit's cache, as well as online players. Joins refresh renamed
accounts. Each root action follows its own permission, including an explicit
`activity.check` denial for an administrator. Suggestions match the current prefix.

## Build and integration

Build with JDK 21 and `mvn clean verify`. The POM uses compiler release 21 and Paper API `1.21.10-R0.1-SNAPSHOT`; the loader API is `1.21.10`.

Install the shared Maven plugin dependencies selected by the POM, then supply the four private `libs/` dependencies (VotingPlugin, MMOCore, MMOItems and MythicLib). `.github/scripts/prepare-release.sh` retrieves pinned ServerAssets files and checks `.github/dependencies.sha256`; it needs read access through `GH_TOKEN` (the CI `DEPS_TOKEN` secret). Output is `target/activity-<version>.jar`; pull request builds publish a dated development version.

Optional runtime integrations are declared as `softdepend` in `src/main/resources/plugin.yml`; those declarations do not remove their compile-time JAR requirements. `ActivityPlugin` registers hooks for installed plugins, `ActivityManager` owns task progress and rewards, and `/activity` opens the GUI or runs permitted admin actions.

- [Reward pools and operator checks](REWARD-POOLS.md)
- [Activity descriptions, placeholders and config updates](ACTIVITY-LORE.md)

The POM pins TLibs **2.4.1** and SimpleFactions **4.0.0**. Battle participation
remains an account UUID integration; the character migration preserves that
event contract.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
