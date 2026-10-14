# ConditionalEvents

[Source repository](https://github.com/TF-Minecraft/ConditionalEvents) · [All projects](../../README.md)

TFMC's copy of [Ajneb97/ConditionalEvents](https://github.com/Ajneb97/ConditionalEvents): configured actions for Minecraft events, with once-only and cooldown data per character by default, or per account.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Run Maven with **JDK 21** from the source checkout. The POM sets `maven.compiler.release=21` and resolves `io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope. The plugin descriptor declares `api-version: 1.21.10`. exp4j is shaded under `net.tfminecraft.conditionalevents.libs.exp4j`.

ItemsAdder's public API artifact is no longer published, so the build uses the pinned ItemsAdder 4.0.18 jar from ServerAssets. Install `me.plugins:tlibs:2.6.1` with the [shared installer](../TLibs/README.md), prepare the private input, then build:

```bash
python3 path/to/TLibs/tools/install-plugins.py --pom pom.xml --mode pinned &&
  (read -rsp 'ServerAssets token: ' GH_TOKEN && echo && export GH_TOKEN &&
    bash .github/scripts/prepare-release.sh) &&
  mvn clean verify
```

JaCoCo requires 100% line coverage of `net.tfminecraft.conditionalevents.character`, the TFMC character code. Upstream code has no tests.

## Runtime and configuration

The manifest requires TLibs. RPCharacters provides character sessions; it is not a load dependency, because SimpleFactions loads after ConditionalEvents and RPCharacters after SimpleFactions. Event types, conditions, actions and variables are configured as in upstream ConditionalEvents; see the [upstream wiki](https://ajneb97.gitbook.io/conditionalevents). This copy has no update checker or bStats reporting, and an old `Config.update_notification` key is ignored.

## Guides

- [Behaviour and operations](overview.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
