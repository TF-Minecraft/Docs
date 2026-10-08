# VFBuilders

[Source repository](https://github.com/TF-Minecraft/VFBuilders) · [All projects](../../README.md)

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

See the [shared API versions](../../PLATFORM.md#shared-api-versions) for the matching provider dependency set.

VFBuilders adds configurable vehicle-building stations and blueprints to
[VehicleFramework](../VehicleFramework/README.md).

## Setup and build

Use JDK 21 and Maven from `main`. The POM resolves Paper API
**1.21.10-R0.1-SNAPSHOT** with `provided` scope and targets Java 21. Install
the declared TLibs, VehicleFramework and CoreProtect versions with the
[shared installer](../TLibs/README.md) in pinned mode.

Prepare the authorized private dependencies with
`.github/scripts/prepare-release.sh` and verify `.github/dependencies.sha256`.
The private inputs in `libs/` are `ItemsAdder-4.0.18.jar`,
`json-simple-1.1.1.jar`, `gson-2.14.0.jar`, `ModelEngine-R4.1.1.jar` and
`NBTAPI-2.16.1.jar`. ModelEngine and NBTAPI are test dependencies.

```sh
mvn clean verify
```

Maven writes the JAR under `target/` using the version declared in `pom.xml`.
Validate VFBuilders against the intended Java 21 server and VehicleFramework
build before deployment.

## Configuration and integration

The [plugin manifest](https://github.com/TF-Minecraft/VFBuilders/blob/main/src/main/resources/plugin.yml)
requires TLibs and VehicleFramework. The
[entrypoint](https://github.com/TF-Minecraft/VFBuilders/blob/main/src/main/java/net/tfminecraft/vfbuilders/VFBuilders.java)
loads `config.yml`, `stations.yml`, `categories.yml` and files under
`plugins/VFBuilders/blueprints/`, then starts the station manager. It creates a
`data/` directory under the plugin's data folder.

The JAR bundles `config.yml` plus empty `stations.yml` and `categories.yml`
defaults, and copies them when missing. Existing files are preserved. The
`blueprints/` directory starts empty: configure stations, categories and
blueprints before players can begin construction.

`/vfbuilders reload` reloads configuration and rebinds stations. It requires
`vfbuilders.reload`, granted to operators by default.

## Validation

Run a Paper 1.21.10 startup, build-station and reload test for the exact
plugin and dependency set. Record the source commit and results with the release.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
