# VehicleFramework

[Source repository](https://github.com/TF-Minecraft/VehicleFramework) · [All projects](../../README.md)

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

Published Java 21 replacement: [1.1.13](https://github.com/TF-Minecraft/VehicleFramework/releases/tag/v1.1.13), verified locally. See the [replacement release status](../../PLATFORM.md#java-21-dependency-replacements) for provenance, verification and deployment status.

Technical documentation is maintained here. Run commands from the source checkout unless a guide says otherwise.

- [Architecture and configuration](overview.md)
- [Trains](docs/trains.md)

## Minecraft 1.21.10 test lab

- [Setup and client/server tooling](../ServerAssets/docs/LAB.md)
- [Integration learnings and dependency compatibility](../ServerAssets/docs/LEARNINGS.md)
- [Runtime evidence and unresolved restoration issue](../ServerAssets/docs/TEST-RESULTS.md)
- [Jar inventory](../ServerAssets/JARS.md) (binaries remain private)

Use `m.utils.arcane_fuel` for fuel. Matching MMOItems UTILS definitions, item types, ItemsAdder rails, ModelEngine blueprints and client resource packs are required alongside the jars. See the linked lab guide for the tested versions.

## Build

Use JDK 21 and Maven from the source checkout. Prepare the pinned private jars
with `.github/scripts/prepare-release.sh`, verify `.github/dependencies.sha256`,
and install the matching TLibs and CoreProtect Maven dependencies using their
source builds or CI release setup actions. Then run `mvn clean verify`; the
output from the replacement release source at `v1.1.13` is
`target/vehicleframework-1.1.13.jar`.

The ModelEngine build alias `ModelEngine-4.0.8.jar` points to the supplied R4.1.1
runtime in the dependency script. Its newer-server adapters may contain newer
bytecode; the Minecraft 1.21.10 adapter and API compile on Java 21. Keep the exact
checksum-matching jar instead of substituting an older binary by filename.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, dependency selection and rollback.
