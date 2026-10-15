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
requires TLibs and VehicleFramework. VFBuilders is built against TLibs 2.4.1
for its character session API. That API is main-thread only, so the manifest
does not declare Folia support. The
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

## Construction credit

Each build records two identities when the player left-clicks the building
site:

- `constructorUuid` is the player's **account**.
- `constructorCharacterId` is the character in the player's current session
  (`Characters.currentSession(player)` filtered by `Characters.isCurrent`).

A player without a current character session can still build. The character
is then null. If the installed TLibs lacks the session API, VFBuilders logs one
warning on the first build and records no character from then on.

Projects in progress are saved in `plugins/VFBuilders/data/stations.json` with
both fields. Saves made before the character was recorded load with a null
character. VFBuilders does not look up heirs. SimpleFactions treats a null
character as "resolve the account's heir, or quarantine".

Accepted construction is saved immediately. Progress is checkpointed every 30
seconds while a build is queued, and completion, cancellation and station removal
also save the queue. Interrupted shutdowns can add up to 30 seconds of repeated
building time. Snapshots replace the previous file atomically and do not remove
timer displays. If the initial save fails, construction is cancelled through the
normal material and registration-fee refund path.

A queued project's optional `outputUuid` records the vehicle created during
completion. Recovery checks VehicleFramework's stored rows, including destroyed
vehicles, before spawning another output. The output must be saved before the
station clears its job. Keep a backup of `stations.json` before upgrading; before
downgrading, resolve any projects with `outputUuid` because older VFBuilders
versions ignore that field. Accepted-start and output-recovery messages identify
the station and build in the server log. This recovery protects saved jobs; it
does not reconstruct jobs that were never saved. Inventory, registration fees
and the station file are separate stores, so a process failure during their
handoff can still require staff reconciliation.

### API for other plugins

[`BeginVehicleConstructionEvent`](https://github.com/TF-Minecraft/VFBuilders/blob/main/src/main/java/net/tfminecraft/vfbuilders/events/BeginVehicleConstructionEvent.java),
[`VehicleConstructEvent`](https://github.com/TF-Minecraft/VFBuilders/blob/main/src/main/java/net/tfminecraft/vfbuilders/events/VehicleConstructEvent.java)
and
[`VehicleConstructionCancelEvent`](https://github.com/TF-Minecraft/VFBuilders/blob/main/src/main/java/net/tfminecraft/vfbuilders/events/VehicleConstructionCancelEvent.java)
expose `UUID getConstructorCharacterId()`. The construct and cancel events
also expose the account as `getConstructorUuid()`. The begin event carries the
`Player`.

Cancellation listeners must read the blueprint and constructor from the event's
getters; the station's queued job has already been cleared durably.

[`ConstructionFreeze`](https://github.com/TF-Minecraft/VFBuilders/blob/main/src/main/java/net/tfminecraft/vfbuilders/api/ConstructionFreeze.java)
providers are registered with Bukkit's `ServicesManager`. Each second, every
station still counting down calls
`freezeReason(UUID account, UUID character)` on each provider. The default
implementation asks `freezeReason(UUID account)`, so account-only providers
keep working. Override the two-argument form to freeze by character.

Plugins that must also run against older VFBuilders jars should probe these
methods by reflection before calling them, for example
`VehicleConstructEvent.class.getMethod("getConstructorCharacterId")`.

## Validation

Run a Paper 1.21.10 startup, build-station and reload test for the exact
plugin and dependency set. Record the source commit and results with the release.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
