# Cooking

[Source repository](https://github.com/TF-Minecraft/Cooking) · [All projects](../../README.md)

Food composition, cooking stations, crop quality and animal husbandry.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

See the [shared API versions](../../PLATFORM.md#shared-api-versions) for the matching provider dependency set.

## Build and dependencies

Run Maven from the source checkout. The current [POM](https://github.com/TF-Minecraft/Cooking/blob/main/pom.xml) declares Java **release 21** and **paper-api 1.21.10-R0.1-SNAPSHOT**; [plugin.yml](https://github.com/TF-Minecraft/Cooking/blob/main/src/main/resources/plugin.yml) declares `api-version: 1.21.10`. The build and loader metadata target the shared runtime. Gameplay validation remains separate from build verification.

Use JDK 21, install the matching TLibs Maven artifact (`me.plugins:tlibs`, version from `tlibs.version`), install the other TFMC Maven dependencies listed in the POM, and populate `libs/` using the pinned private dependency preparation script. Run `mvn clean verify`; the artifact stays in `target/`. Optional runtime integrations can still be required at compile time.

## Runtime and configuration

The plugin registers food item paths with TLibs and integrates furniture stations, TLibs inventory scanning, crops and husbandry. The manifest requires TLibs and InteractibleFurniture, and the POM pins TLibs 2.1.0; RPCharacters, MMOCore, CustomCrops, SimpleFactions and CustomFishing enable additional integrations. `/cooking` requires `cooking.admin` (op by default). The guides below define crop and husbandry behavior and their configuration boundaries.

## Guides

- [docs/crops.md](docs/crops.md)
- [docs/husbandry.md](docs/husbandry.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.

## Shared feature ownership

See [shared feature ownership](../TFMCCore/ownership.md) for scanner, focus and letter APIs, configuration, and verification.
