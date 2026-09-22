# AACommandsFiller

[Source repository](https://github.com/TF-Minecraft/AACommandsFiller) · [All projects](../../README.md)

Configurable command trees and permission-filtered tab completion.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Run Maven from the source checkout. The current [POM](https://github.com/TF-Minecraft/AACommandsFiller/blob/main/pom.xml) declares Java **release 21** and **paper-api 1.21.10-R0.1-SNAPSHOT**; [plugin.yml](https://github.com/TF-Minecraft/AACommandsFiller/blob/main/src/main/resources/plugin.yml) declares `api-version: 1.21.10`. The build and loader metadata target the shared runtime. Gameplay validation remains separate from build verification.

Build with `mvn clean verify`; Paper API resolves from Maven. Packaging writes the jar to `target/`.

## Guides

- [Behavior and operations](overview.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
