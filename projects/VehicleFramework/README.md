# VehicleFramework

[Source repository](https://github.com/TF-Minecraft/VehicleFramework) · [All projects](../../README.md)

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

See the [shared API versions](../../PLATFORM.md#shared-api-versions) for the matching provider dependency set.

Technical documentation is maintained here. Run commands from the source checkout unless a guide says otherwise.

- [Architecture and configuration](overview.md)
- [Trains](docs/trains.md)

## Assets and dependencies

See the [jar inventory](../ServerAssets/JARS.md) for the private binary inputs.

Use `m.utils.arcane_fuel` for fuel. Matching MMOItems UTILS definitions, item types, ItemsAdder rails, ModelEngine blueprints and client resource packs are required alongside the jars. Use the asset manifest and record the exact versions for each test run.

## Build

Use JDK 21 and Maven from the source checkout. Prepare the pinned private jars
with `.github/scripts/prepare-release.sh`, verify `.github/dependencies.sha256`,
and install the matching TLibs and CoreProtect Maven dependencies using their
source builds or the shared installer in pinned mode. Then run
`mvn clean verify` from `main`; Maven writes the JAR under `target/` using
the version declared in `pom.xml`.

The ModelEngine build alias `ModelEngine-4.0.8.jar` points to the supplied R4.1.1
runtime in the dependency script. Its newer-server adapters may contain newer
bytecode; the Minecraft 1.21.10 adapter and API compile on Java 21. Keep the exact
checksum-matching jar instead of substituting an older binary by filename.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, dependency selection and rollback.
