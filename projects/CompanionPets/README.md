# CompanionPets

[Source repository](https://github.com/TF-Minecraft/CompanionPets) · [All projects](../../README.md)

CompanionPets adds companion pet hatching, care, training, and play. It keeps
one record per pet (name, sex, personality, needs, bond, tricks, and a rolled
favourite toy); the Minecraft entity is only the pet's current body. Vanilla
wolves, cats, and foxes need no model plugin.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md)
for runtime, build, and validation conventions.

## Guides

- [Gameplay](docs/gameplay.md) — hatching, care, training, orders, play, and menus
- [Configuration](docs/configuration.md) — interaction items, per-pet overrides,
  learnable, default and custom tricks, and moments
- [Pet types and ModelEngine](docs/models.md) — bodies, eggs, animation clips, and
  model authoring
- [Staff commands](docs/staff.md) — commands, permissions, and audit
- [Saved data and recovery](docs/saved-data.md) — persistence files, backups, and
  recovery after a failed save
- [Testing](docs/testing.md) — automated coverage and the dev-only Paper helper
- [Default configuration](https://github.com/TF-Minecraft/CompanionPets/blob/main/src/main/resources/config.yml)
- [Plugin commands and permissions](https://github.com/TF-Minecraft/CompanionPets/blob/main/src/main/resources/plugin.yml)

## Build and dependencies

Build the source repository with Java **21** and Maven:

```sh
mvn clean verify
python3 .github/scripts/plugin-artifact.py --jar target/companionpets-main-SNAPSHOT.jar --version main-SNAPSHOT
```

The build uses `io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT` with
`provided` scope. No private jars or shared TFMC plugin artifacts are required.
The plugin entry point is `net.tfminecraft.companionpets.PetsPlugin`.

The descriptor soft-depends on MythicMobs, ModelEngine, ItemsAdder, MMOItems, and
MythicLib so that they load first when installed; none of them is required. The
plugin calls their APIs by reflection: MythicMobs and ModelEngine supply bodies
and models (`integration/`), and MMOItems and ItemsAdder supply interaction items
and eggs (`item/ItemBridge.java`). MythicLib is only a load-order dependency.
CompanionPets has no runtime dependency on Archaeo, Cooking, or MCPets.

The build command runs the tests under `src/test/java` and enforces 100%
production line coverage. Surefire reports are in `target/surefire-reports/` and
JaCoCo reports are in `target/site/jacoco/`. Coverage runs in every normal
verification; the `coverage` profile is only a compatibility alias.

## Testing on a Paper server

The source repository includes a dev-only
[integration helper](docs/testing.md#paper-integration-helper)
that runs once against a real Paper server with the configured providers and
reports `COMPANIONPETS_INTEGRATION PASS` or `FAIL` in the log. It does not
establish correct rendering in a Minecraft client.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md). Pull requests build
`companionpets-DEV-<UTC date>-<UTC time>.jar`; `main` uses `main-SNAPSHOT`.
Version tags trigger a verified draft release containing the runtime jar,
checksums, and build metadata.
