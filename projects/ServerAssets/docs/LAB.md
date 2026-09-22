# CachyOS Minecraft test lab

Use Java 21 and Paper 1.21.10 under the [shared platform baseline](../../../PLATFORM.md).
Build the TFMC plugins from `main` with their committed dependency versions.
The private [ServerAssets repository](https://github.com/TF-Minecraft/ServerAssets)
provides binaries, configurations, blueprints and packs; follow
[asset preparation](../overview.md#verify-and-prepare) before setting up a lab.

## Installed tooling

The isolated CachyOS lab is under
`/home/ryan/.local/share/blightfront-test-runner/vehicleframework/`.
These commands refer to that installed environment:

```bash
cd /home/ryan/.local/share/blightfront-test-runner/vehicleframework
./bin/lab doctor                 # Inspect installed components
./bin/lab play                   # Start the server and graphical client
./bin/lab smoke                  # Bounded bot connection and movement check
./bin/lab console "list"         # Send a server-console command
./bin/lab stop                   # Stop this test server
```

The installed launchers are local tooling. Check their Java selection and source
checkout before each run; verify that both the build and server use Java 21.
Build from the plugin source checkout using the [current build instructions](../../VehicleFramework/README.md#build).
Stop the test server before replacing its plugin jars, then check startup logs
for successful enablement.

The graphical client uses `VehicleTester`; the bot uses `VehicleTestBot`.
Connect to `127.0.0.1:25565`. The lab uses offline authentication, so keep the
server bound to localhost. Use an SSH tunnel for the optional browser viewer.
Keep personal Minecraft profiles, production configuration and player data separate.

## Assets and dependencies

Install the matching ModelEngine runtime and TFMC plugin set, MMOItems UTILS
and item-type definitions, ItemsAdder rail registrations and ModelEngine blueprints.
Enable `vehicleframework-models.zip` above `tfmc-cached.zip` in the isolated client.
Keep the cached pack intact; its ZIP entry names are not compatible with every
extraction tool. A client pack alone does not register server-side items.

Use `m.utils.arcane_fuel` for vehicle fuel. Check that the recorder item path is
`m.utils.train_track_recorder`. Use the [manifest](../JARS.md) for the exact asset
inputs and the plugin POMs for build dependencies.

## Validation

Record the current source commit, JDK, Paper version, plugin versions and hashes,
and configuration with each test run. Exercise:

- Fresh vehicle spawning, model rendering, seating, controls and fuel consumption.
- Rail placement, train coupling and movement.
- Weapon reload, firing and damage against a controlled target.
- Unload/reload and server restart with saved vehicles and trains.
- Client resource-pack rendering and sounds.

A bot connection test covers connection and movement only. Use the graphical
client for models and UI, and compare fresh and restored state when diagnosing
persistence problems. See [integration notes](LEARNINGS.md).

Keep evidence in the run's `artifacts/` directory or the associated PR. Useful
outputs include `server/logs/latest.log`, `artifacts/server-console.log`,
`artifacts/bot-smoke.json` and `client/screenshots/`. Results apply to the recorded
commit and dependency set; rerun relevant checks after changes.
