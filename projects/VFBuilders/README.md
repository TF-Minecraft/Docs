# VFBuilders

[Source repository](https://github.com/TF-Minecraft/VFBuilders) · [All projects](../../README.md)

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

See the [shared API versions](../../PLATFORM.md#shared-api-versions) for the matching provider dependency set.

VFBuilders adds configurable vehicle-building stations and blueprints to
[VehicleFramework](../VehicleFramework/README.md).

## Setup and build

Use JDK 21 and Maven from the source checkout. The migration POM resolves
Spigot API **1.21.10-R0.1-SNAPSHOT** with `provided` scope and targets Java 21.
Install the compatible TLibs **1.1.1** and VehicleFramework **1.1.13** builds in
local Maven, or use the repository's shared setup action in latest mode. See the [shared baseline](../../PLATFORM.md) for the
local migration and release status.

Prepare the authorized private dependencies with
`.github/scripts/prepare-release.sh` and verify `.github/dependencies.sha256`.
The remaining local inputs in `libs/` are `ItemsAdder_3.5.0-r2.jar`,
`json-simple-1.1.jar` and `gson-2.10.1.jar`.

```sh
mvn clean verify
```

The replacement release source at `v1.0.1` produces
`target/vfbuilders-1.0.1.jar`. These compile-time
inputs do not identify the tested runtime stack: the earlier vehicle lab uses
ItemsAdder 4.0.18. Validate VFBuilders against the intended Java 21 server and
VehicleFramework build before deployment.

## Configuration and integration

The [plugin manifest](https://github.com/TF-Minecraft/VFBuilders/blob/main/src/main/resources/plugin.yml)
requires TLibs and VehicleFramework. The
[entrypoint](https://github.com/TF-Minecraft/VFBuilders/blob/main/src/main/java/net/tfminecraft/vfbuilders/VFBuilders.java)
loads `config.yml`, `stations.yml`, `categories.yml` and files under
`plugins/VFBuilders/blueprints/`, then starts the station manager. It creates a
`data/` directory under the plugin's data folder.

Only `config.yml` and `plugin.yml` are present in the reviewed source resource
directory. The entrypoint attempts to copy missing station/category defaults
from the jar, so a fresh install needs those configurations supplied and checked;
the source checkout alone does not establish a complete first-start setup.

`/vfbuilders reload` reloads configuration and rebinds stations. It requires
`vfbuilders.reload`, granted to operators by default.

## Validation

The migration build passes with JDK 21. A Paper 1.21.10 startup/build-station/reload
test is still needed for the exact plugin and dependency set. The
[VehicleFramework lab report](../ServerAssets/docs/TEST-RESULTS.md) does not
include VFBuilders acceptance tests.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
