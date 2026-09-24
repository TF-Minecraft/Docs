# CompanionPets

[Source repository](https://github.com/TF-Minecraft/CompanionPets) · [All projects](../../README.md)

CompanionPets adds companion pet hatching, care, training, and play. It keeps
one record per pet (name, sex, needs, bond, tricks, and a rolled favourite toy);
the Minecraft entity is only the pet's current body. Vanilla wolves, cats, and
foxes work without other plugins.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md)
for runtime, build, and validation conventions.

## Build and dependencies

Build the source repository with Java **21** and Maven:

```sh
mvn clean verify -DskipTests=false -Dmaven.test.skip=false
python3 .github/scripts/plugin-artifact.py --jar target/companionpets-main-SNAPSHOT.jar --version main-SNAPSHOT
```

The build uses `io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT` with
`provided` scope. No private jars or shared TFMC plugin artifacts are required.
The plugin entry point is `net.tfminecraft.companionpets.PetsPlugin`.

The descriptor declares MythicMobs, ModelEngine, ItemsAdder, and MMOItems as
optional integrations. MythicMobs and ModelEngine are loaded by reflection when
installed (`integration/MythicSpawn.java`, `integration/ModelHook.java`); the
plugin does not call ItemsAdder or MMOItems. The build command above runs the
unit tests under `src/test/java`.

## Design notes

The original design notes are preserved in Spanish:

- [Pet identity, entities, and movement](docs/design/nucleo-mascota.md)
- [Care and needs](docs/design/cuidado.md)
- [Training and tricks](docs/design/entrenamiento.md)
- [Play and toys](docs/design/juego.md)
- [Hatching, ownership, and management](docs/design/gestion.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md). Pull requests build
`companionpets-DEV-<UTC date>-<UTC time>.jar`; `main` uses `main-SNAPSHOT`.
Version tags trigger a verified draft release containing the runtime jar,
checksums, and build metadata.
