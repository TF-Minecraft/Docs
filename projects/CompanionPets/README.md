# CompanionPets

[Source repository](https://github.com/TF-Minecraft/CompanionPets) · [All projects](../../README.md)

CompanionPets is an early scaffold for companion pet hatching, care, training,
and play. The current plugin only logs startup and shutdown. The design notes
below describe planned systems, not implemented gameplay.

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
optional integrations. The scaffold does not currently call their APIs.
There is no unit-test suite yet.

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
