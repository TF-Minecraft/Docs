# BarterShops

[Source repository](https://github.com/TF-Minecraft/BarterShops) · [All projects](../../README.md)

Sign-based item shops with DenarEconomy payments and faction embargo checks.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Run Maven with **JDK 21** from the source checkout. The POM sets `maven.compiler.release=21` and resolves `io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope from the PaperMC Maven repository. The plugin descriptor declares `api-version: 1.21.10`.

Install these matching Java 21 TFMC artifacts into local Maven before building: `net.tfminecraft:denareconomy:0.2.0`, `net.tfminecraft:simplefactions:3.0.1`. Their source repositories use `mvn clean install`; CI uses the pinned dependency setup actions.

Populate `libs/` with the exact files and hashes listed in `.github/dependencies.sha256`. `.github/scripts/prepare-release.sh` downloads those pinned private assets when supplied with the approved dependency token.

Install the pinned shared plugin dependencies, download the private build
inputs, then run the build with Java 21. In Bash:

```bash
python3 path/to/TLibs/tools/install-plugins.py --pom pom.xml --mode pinned &&
  (read -rsp 'ServerAssets token: ' GH_TOKEN && echo && export GH_TOKEN &&
    bash .github/scripts/prepare-release.sh) &&
  mvn clean verify
```

The installer comes from a separate TLibs checkout
(`git clone https://github.com/TF-Minecraft/TLibs.git`); point `path/to/TLibs` at it. The token needs Contents read access
to TF-Minecraft/ServerAssets. The prompt keeps it out of shell history, the
subshell keeps it out of your session and Maven, and Maven only runs if both
preparation steps succeed. CI supplies it from `DEPS_TOKEN`.

Use `mvn clean install` when another plugin needs the result as a Maven dependency. The plugin JAR is written under `target/`. Gameplay and web integration checks on the Minecraft 1.21.10 server remain separate from build verification.

## Runtime and configuration

Required plugins declared by the manifest: MMOItems, MythicLib.

`ShopEvents` handles sign interactions and calls DenarEconomy directly for currency trades; install DenarEconomy even though the current manifest omits it. `ShopEmbargo` provides the SimpleFactions integration. Shop JSON lives under `plugins/BarterShops/Data`; preserve it across upgrades. The manifest declares no commands.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
