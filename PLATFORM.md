# Shared platform and build baseline

TFMC plugins target **Java 21 / Minecraft 1.21.10**, using
`io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope.
Plugin descriptors declare API 1.21.10.

## Runtime and toolchain

| Component | Baseline |
| --- | --- |
| Minecraft | 1.21.10 |
| Server | Paper 1.21.10 |
| Build JDK and server JVM | Java 21 |
| Plugin build tool | Maven |
| Web/backend | Follow [ProvinceSystem](projects/ProvinceSystem/docs/README.md) |

Build from `main` using the committed POM and dependency pins. CoreProtect uses
`master`. Tagged releases record a specific version of that source.

## Build conventions

### Java package layout

Plugin-owned Java sources use `src/main/java/net/tfminecraft/<plugin>/`,
with lowercase package segments throughout. Derive `<plugin>` from the repository
name by lowercasing it and removing hyphens: for example, `VFBuilders` becomes
`vfbuilders`, `activity-tf` becomes `activitytf`, and `geiger-counters` becomes
`geigercounters`. CoreProtect uses `net.tfminecraft.coreprotect` in this fork.
Use `enums` and `interfaces` as package names; their singular forms are Java
keywords. Java class names retain normal Java capitalization.

Mirror packages under `src/test/java`, except deliberate external API fixtures.
Keep package declarations, imports, reflection strings, `plugin.yml` entry points,
and shaded-library destinations aligned with the source folders. Maven artifact
coordinates, plugin names, and data-directory names are separate identifiers
from Java packages.

Build consumers against matching provider jars and release the dependent plugin
set together. CoreProtect integrations use this fork's
`net.tfminecraft.coreprotect` API.

### Build inputs

Follow the [XML and Maven POM conventions](POM-CONVENTIONS.md). Run builds from
the plugin source repository with Java 21:

```sh
java -version
mvn -version
python3 ../tlibs/tools/install-plugins.py --pom pom.xml --mode pinned
mvn clean verify
```

The compiler's `release=21` setting controls bytecode and available Java APIs.
Paper API resolves from the [PaperMC Maven repository](https://repo.papermc.io/repository/maven-public/)
and is not bundled into plugin jars. Prepare private third-party dependencies with the
repository's `.github/scripts/prepare-release.sh`; it verifies
`.github/dependencies.sha256` where present, then installs those exact JARs
under hash-qualified Maven versions with `provided` scope. See
[local dependency preparation](PIPELINES.md#build-dependencies).

Shared plugin dependencies use the exact versions declared in each consumer POM.
The [shared installer](PIPELINES.md#build-dependencies) verifies the public
artifacts and installs them into Maven. For source builds involving circular
plugin dependencies, provide the matching API artifacts before compiling the
consumer set. Source builds must pass clean verification before publication.

## Plugin build targets

| Project | Java release | API | API version |
| --- | --- | --- | --- |
| [AACommandsFiller](projects/AACommandsFiller/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [ActivityTF](projects/ActivityTF/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [AdvancedCrafting](projects/AdvancedCrafting/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [AdvancedGunpowder](projects/AdvancedGunpowder/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [AdvancedResearch](projects/AdvancedResearch/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Archaeo](projects/Archaeo/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [ArmourShop](projects/ArmourShop/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [BarterShops](projects/BarterShops/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [BirdMessenger](projects/BirdMessenger/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Cooking](projects/Cooking/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [CoreProtect](projects/CoreProtect/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [DenarEconomy](projects/DenarEconomy/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [DrinkBuilder](projects/DrinkBuilder/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Dowsing](projects/Dowsing/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Games](projects/Games/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [GeigerCounters](projects/GeigerCounters/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [GemInfusion](projects/GemInfusion/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Goldsmithing](projects/Goldsmithing/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [GunsAndGadgets](projects/GunsAndGadgets/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [InteractibleFurniture](projects/InteractibleFurniture/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Magic](projects/Magic/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [MarketBlock](projects/MarketBlock/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [MusicalInstruments](projects/MusicalInstruments/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Nutrition](projects/Nutrition/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [PermCleaner](projects/PermCleaner/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [PointShop](projects/PointShop/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Recycler](projects/Recycler/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [RPCharacters](projects/RPCharacters/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [SimpleFactions](projects/SimpleFactions/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Surgery](projects/Surgery/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [TFMCCore](projects/TFMCCore/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [TFMCWeb](projects/TFMCWeb/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Thievery](projects/Thievery/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [TLibs](projects/TLibs/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [VehicleFramework](projects/VehicleFramework/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [VFBuilders](projects/VFBuilders/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Woodworking](projects/Woodworking/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [WorldBorder](projects/WorldBorder/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |

ProvinceSystem is a web/backend project. ServerAssets contains configurations,
models, resource packs, and private build inputs. Neither produces a plugin jar.

## Shared API versions

These source versions provide the `net.tfminecraft.<plugin>` Java APIs used by
the corresponding consumer dependency pins. Maven coordinates remain separate
from Java package names.

| Project | Version |
| --- | --- |
| [AdvancedCrafting](https://github.com/TF-Minecraft/AdvancedCrafting) | `2.0.0` |
| [cooking](https://github.com/TF-Minecraft/Cooking) | `0.2.1` |
| [CoreProtect](https://github.com/TF-Minecraft/CoreProtect) | `25.0.0` |
| [denareconomy](https://github.com/TF-Minecraft/DenarEconomy) | `0.2.0` |
| [games](https://github.com/TF-Minecraft/Games) | `0.2.0` |
| [geiger-counters](https://github.com/TF-Minecraft/GeigerCounters) | `2.0.0` |
| [gunsandgadgets](https://github.com/TF-Minecraft/GunsAndGadgets) | `2.0.0` |
| [interactiblefurniture](https://github.com/TF-Minecraft/InteractibleFurniture) | `0.2.0` |
| [magic](https://github.com/TF-Minecraft/Magic) | `0.2.0` |
| [Marketblock](https://github.com/TF-Minecraft/MarketBlock) | `0.1.0` |
| [musical-instruments](https://github.com/TF-Minecraft/MusicalInstruments) | `3.0.0` |
| [rpcharacters](https://github.com/TF-Minecraft/RPCharacters) | `2.0.0` |
| [simplefactions](https://github.com/TF-Minecraft/SimpleFactions) | `3.0.0` |
| [tfmccore](https://github.com/TF-Minecraft/TFMCCore) | `2.0.0` |
| [tlibs](https://github.com/TF-Minecraft/TLibs) | `2.0.0` |
| [vehicleframework](https://github.com/TF-Minecraft/VehicleFramework) | `2.0.0` |
| [vfbuilders](https://github.com/TF-Minecraft/VFBuilders) | `2.0.0` |

## Dependencies and validation

Record source commits, dependency checksums, the JDK, Maven commands, test
results, and artifact checksums for release builds. Check packaged entry points,
plugin versions, and API versions as well as source settings.

Compilation and unit tests do not exercise a live Minecraft server. Runtime
validation should record the Paper build, plugin set, configuration, exercised
commands, gameplay, and persistence across restarts. Publishing artifacts does
not deploy them to a server.

## Documentation conventions

Each [project index](README.md#projects) links here. Keep current setup guidance
aligned with the declared platform and dependency versions. Link to the source
repository for code and use relative links between Docs guides. See
[Maintaining the documentation](MAINTAINING.md).
