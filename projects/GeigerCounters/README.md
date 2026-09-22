# GeigerCounters

[Source repository](https://github.com/TF-Minecraft/GeigerCounters) · [All projects](../../README.md)

Particle and sound tracking for hidden sources, weighted loot and per-player collection limits.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Run Maven from the source checkout. The current [POM](https://github.com/TF-Minecraft/geiger-counters/blob/main/pom.xml) declares Java **release 21** and **paper-api 1.21.10-R0.1-SNAPSHOT**; [plugin.yml](https://github.com/TF-Minecraft/geiger-counters/blob/main/src/main/resources/plugin.yml) declares `api-version: 1.21.10`. The build and loader metadata target the shared runtime. Gameplay validation remains separate from build verification.

Install the approved Maven artifact `me.plugins:tlibs:2.0.0` using the shared dependency workflow, then run `mvn clean verify` with JDK 21. Paper API, WorldGuard API and bStats resolve from Maven. Packaging writes the jar to `target/`. MMOItems is an optional runtime item source, not a direct build dependency.

## Guides

- [Behavior and operations](overview.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
