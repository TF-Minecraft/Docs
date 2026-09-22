# Shared platform and build baseline

TFMC runs **Minecraft 1.21.10 on Java 21**. All maintained plugin builds target
Java 21 bytecode and the Minecraft **1.21.10** Paper or Spigot API. Plugin
`api-version` metadata is **1.21.10** throughout.

## Runtime and toolchain

| Component | Baseline |
| --- | --- |
| Minecraft client/server | 1.21.10 |
| Server implementation | Paper; the recorded lab used build 130 (`8043efd`) |
| Plugin build JDK and server JVM | Java 21 |
| Build tool | Maven; use each repository's CI workflow and pinned dependencies |
| Web/backend | Follow [ProvinceSystem](projects/ProvinceSystem/docs/README.md); its Node/Python runtimes are independent |

Paper's [Java version table](https://docs.papermc.io/paper/getting-started/#requirements)
recommends Java 21 for the 1.20–1.21.11 series. TFMC's plugin migration uses Java 21
for both compilation and the runtime target. Old Java 25 TFMC jars must be
replaced together with their rebuilt dependencies; changing the server JVM alone
is insufficient.

The earlier [vehicle lab](projects/ServerAssets/docs/LAB.md) used Java 25 and
records historical evidence. It is not a Java 21 runtime certification. Its
restored-vehicle failure remains unresolved by this build migration.

## Build conventions

Run commands from the **source repository**, not this Docs checkout:

```sh
java -version
mvn -version
mvn clean verify
```

Both version commands should identify JDK 21. The POM uses
`maven.compiler.release=21` to restrict emitted bytecode and Java platform APIs.
Paper/Spigot APIs resolve from their Maven repositories with `provided` scope;
they are not bundled into plugin jars or read from an ambiguously named local
`spigot-api.jar`.

Supply the authorized private dependency jars using each repository's
`.github/scripts/prepare-release.sh` and verify its `.github/dependencies.sha256`
where present. These scripts require access to ServerAssets. Their `libs/`
directory is a source-build input, not this documentation repository. Use the
repository's pinned setup actions for released TFMC dependencies, or `mvn install`
in their source checkouts to install compatible local builds.

Some TFMC plugins depend on each other in both directions. A full rebuild may
need an authentic existing dependency artifact to bootstrap the cycle, followed
by clean Java 21 builds against the rebuilt dependencies. Keep bootstrap jars
out of the final distribution. Publishing the new dependency artifacts is a
separate step; changing consumer CI to Java 21 does not update an old release
asset automatically.

## Unified source build declarations

The source migrations and Java 21 dependency-pin updates were merged on
**2026-09-22**. The 36 plugin projects below now declare these settings on their
default branches. The eight verified replacement releases are listed below.
Source merges and release publication do not deploy the rebuilt jars; this table
does not certify the live plugin set or Java 21 gameplay compatibility.

| Project | Java release | API | API version |
| --- | --- | --- | --- |
| [AACommandsFiller](projects/AACommandsFiller/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [ActivityTF](projects/ActivityTF/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [AdvancedCrafting](projects/AdvancedCrafting/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [AdvancedGunpowder](projects/AdvancedGunpowder/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [AdvancedResearch](projects/AdvancedResearch/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [ArmourShop](projects/ArmourShop/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [BarterShops](projects/BarterShops/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [BirdMessenger](projects/BirdMessenger/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Cooking](projects/Cooking/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [CoreProtect](projects/CoreProtect/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [DenarEconomy](projects/DenarEconomy/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [DrinkBuilder](projects/DrinkBuilder/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Games](projects/Games/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [GeigerCounters](projects/GeigerCounters/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [GemInfusion](projects/GemInfusion/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Goldsmithing](projects/Goldsmithing/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [GunsAndGadgets](projects/GunsAndGadgets/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [InteractibleFurniture](projects/InteractibleFurniture/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Magic](projects/Magic/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [MarketBlock](projects/MarketBlock/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [MusicalInstruments](projects/MusicalInstruments/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Nutrition](projects/Nutrition/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [PermCleaner](projects/PermCleaner/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [PointShop](projects/PointShop/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Recycler](projects/Recycler/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [RPCharacters](projects/RPCharacters/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [SimpleFactions](projects/SimpleFactions/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Surgery](projects/Surgery/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [TFMCCore](projects/TFMCCore/README.md) | 21 | `paper-api` | `1.21.10-R0.1-SNAPSHOT` |
| [TFMCWeb](projects/TFMCWeb/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Thievery](projects/Thievery/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [TLibs](projects/TLibs/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [VehicleFramework](projects/VehicleFramework/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [VFBuilders](projects/VFBuilders/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [Woodworking](projects/Woodworking/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |
| [WorldBorder](projects/WorldBorder/README.md) | 21 | `spigot-api` | `1.21.10-R0.1-SNAPSHOT` |

ProvinceSystem is a web/backend project and ServerAssets is a private asset
snapshot. Neither produces a Minecraft plugin jar in this build set.
AdvancedCrafting is included because several plugins require it.

## Java 21 dependency replacements

As of **2026-09-22**, the following replacement artifacts passed local JDK 21
verification and are **published**. The previous release versions remain
unchanged for rollback.

| Project | Replacement | Unit tests |
| --- | --- | --- |
| [TLibs](projects/TLibs/README.md) | [1.1.1](https://github.com/TF-Minecraft/TLibs/releases/tag/v1.1.1) | 10 passed |
| [Cooking](projects/Cooking/README.md) | [0.1.6-ALPHA](https://github.com/TF-Minecraft/Cooking/releases/tag/v0.1.6-ALPHA) | 167 passed |
| [GunsAndGadgets](projects/GunsAndGadgets/README.md) | [1.0.7](https://github.com/TF-Minecraft/GunsAndGadgets/releases/tag/v1.0.7) | No tests in repository |
| [VehicleFramework](projects/VehicleFramework/README.md) | [1.1.13](https://github.com/TF-Minecraft/VehicleFramework/releases/tag/v1.1.13) | 369 passed |
| [AdvancedCrafting](projects/AdvancedCrafting/README.md) | [1.2.3](https://github.com/TF-Minecraft/AdvancedCrafting/releases/tag/v1.2.3) | No tests in repository |
| [InteractibleFurniture](projects/InteractibleFurniture/README.md) | [0.1.4-BETA](https://github.com/TF-Minecraft/InteractibleFurniture/releases/tag/v0.1.4-BETA) | No tests in repository |
| [VFBuilders](projects/VFBuilders/README.md) | [1.0.1](https://github.com/TF-Minecraft/VFBuilders/releases/tag/v1.0.1) | No tests in repository |
| [MarketBlock](projects/MarketBlock/README.md) | [0.0.3](https://github.com/TF-Minecraft/MarketBlock/releases/tag/v0.0.3) | No tests in repository |

Each JAR declares API 1.21.10 and contains Java 21-compatible classes. Its
`SHA256SUMS` and `build.json` record the artifact hash, exact source commit and
shared dependency inputs. These are local source builds, so `run` is `null`;
bootstrap API inputs used to resolve dependency cycles are recorded separately
from the released artifacts. Licensed third-party dependency JARs remain private.
Cooking and InteractibleFurniture retain their ALPHA/BETA prerelease channels.

Use the [shared installer](PIPELINES.md#build-dependencies) in latest mode to
select published replacements, or pin the exact versions and hashes from a
successful build for reproduction. The source migrations are merged; deployment
and runtime acceptance remain separate checks.

## Dependencies and validation

Build settings, packaged metadata and gameplay evidence are distinct. A jar
whose classes use Java 21 and whose descriptor declares 1.21.10 still needs its
matching dependency versions, configuration and assets on the server. See
Paper's [plugin.yml reference](https://docs.papermc.io/paper/dev/plugin-yml/#api-version)
for the loader metadata semantics.

Record the source revision and patch, dependency checksums, JDK, Maven command,
unit-test results and artifact checksums with every build. For runtime checks,
record the exact Paper 1.21.10 build, plugin set, configuration/assets, exercised
commands/gameplay, and persistence/restart results. Keep passed, failed and
untested behavior explicit.

The [existing vehicle test report](projects/ServerAssets/docs/TEST-RESULTS.md)
covers fresh cars, trains and artillery with its original dependency set. It
records a restored-state failure and does not certify this Java 21 build set.
Offline authentication and localhost settings in that lab are specific to its
isolated test environment.

## Documentation conventions

Every [project index](README.md#projects) links here. Keep current setup guidance
aligned with Java 21 and Minecraft 1.21.10; preserve the original versions in
dated historical reports. Link to the source repository for code and use
relative links for other Docs guides. See [Maintaining the documentation](MAINTAINING.md).
