> This page is public; linked jars, models and configurations remain in the private server-assets repository and require access. The full ItemsAdder contents archive was removed from server-assets on 2026-09-22; historical lab notes below describe the original snapshot. The existing manifest/materializer may still expect that archive.

# CachyOS Minecraft test lab

Interactive car, rail, coupling and artillery checks have now been run. Fresh
vehicles pass; older/restored instances exposed a model/seat-state failure.
See [TEST-RESULTS.md](TEST-RESULTS.md) for evidence and the remaining limitation.

The private [TF-Minecraft/server-assets](https://github.com/TF-Minecraft/server-assets)
repository holds the supplied jars, model blueprints, configuration snapshots and
resource packs. Its manifest separates the tested runtime from older/reference
jars and records SHA-256 checksums. Keep those binaries in that private repository.
This directory contains the launcher code and findings only.

Installed on CachyOS under:

```text
/home/ryan/.local/share/blightfront-test-runner/vehicleframework/
├── Play Minecraft.desktop       Start server and open the visual client
├── bin/                         lab, server and client launchers
├── server/                      Paper 1.21.10, plugins and disposable world
├── client/                      Isolated Minecraft 1.21.10 installation and screenshots
├── bot/                         Mineflayer, browser viewer and npm lockfile
├── dependencies/                Compile-time jars; README lists missing ones
├── assets/models/               Place vehicle model blueprints here
├── assets/resourcepacks/        Place matching resource-pack ZIPs here
├── source/vehicleframework/     Source snapshot and SOURCE_COMMIT
├── source/tlibs/                Drefvelin's TLibs source
├── tools/                       Private Java 25, Maven, Python venv and Maven cache
├── downloads/                   Download provenance and checksums
├── artifacts/                   Console log, smoke-test results and builds
└── run/                         Private console FIFO
```

From a terminal on CachyOS:

```bash
cd /home/ryan/.local/share/blightfront-test-runner/vehicleframework
./bin/lab play                   # Start server, wait for readiness, open game
./bin/lab smoke                  # Bot joins, moves, writes JSON, disconnects
./bin/lab bot                    # Bot with http://127.0.0.1:3007 browser viewer
./bin/lab console "list"         # Send a server-console command
./bin/lab doctor                 # Show installed/missing components
./bin/lab stop                   # Gracefully stop this test server
```

`start` launches only the server. `client` launches only the graphical client.
The graphical client uses the offline name `VehicleTester`; the bot uses
`VehicleTestBot`. Minecraft connects automatically to `127.0.0.1:25565`.
Use Minecraft's **Direct Connection** with that address if Quick Play fails.
To grant admin commands inside this isolated world:

```bash
./bin/lab console "op VehicleTester"
```

The server and browser viewer bind to localhost. Microsoft authentication and
signed profiles are disabled for this private lab. Do not expose these ports
publicly: offline usernames are not authenticated. RCON and query are disabled.
An SSH tunnel is sufficient for viewing the browser page from another computer.
The optional browser viewer is experimental: this release falls back to 1.21.4
block data for 1.21.10, so blocks may be incorrect. Only its HTTP endpoint has
been checked. Use the full Minecraft client for accurate visuals and ModelEngine.

The server is a transient user systemd unit named
`vehicleframework-test-server.service`, with a four-hour maximum lifetime and
graceful shutdown. It does not start at login. The bot exits after 30 minutes
or Ctrl+C; its smoke test has a 45-second deadline. Normal game clients run
until their window is closed. Existing Minecraft/Prism profiles and system
Java settings are not used or modified. The client's executable uses the
existing Java 21; the server and plugin build use the private Java 25.

## VehicleFramework dependencies

The base server/client/bot can run without VehicleFramework. Vehicle tests need:

- A compatible **ModelEngine runtime jar** and **TLibs.jar** in `server/plugins/`.
- A built **VehicleFramework jar** in `server/plugins/`.
- Vehicle model blueprints installed into ModelEngine and a matching pack
  copied into `client/resourcepacks/` and enabled in the client.

ProtocolLib 5.4.0 and NBTAPI 2.15.5 are installed, matching the live server's
reported versions. The repository's compile-time NBTAPI version 2.15.0 fails
on Minecraft 1.21.10.
That original compile-time jar is retained in `dependencies/`.

The following were checked on **TFMC Roleplay**, after joining through the lobby
NPC using the existing Prism client, on 2026-09-22. These are `/version` responses
from the main server, not the lobby or assumptions from the build file:

| Component | Live version |
| --- | --- |
| Server | Paper 1.21.10 build 130, commit `8043efd` |
| ModelEngine | R4.1.1 |
| ProtocolLib | 5.4.0 |
| TLibs | 1.0 |
| VehicleFramework | 1.1.12 |
| NBTAPI | 2.15.5 |
| MythicMobs | 5.13.1-SNAPSHOT-88530541 |

Java 25 was previously reported by the user; these commands did not reverify it.
The earlier chat's description of the server as Spigot was imprecise: the live
server identifies itself as Paper, and its build already matches this lab.
Evidence is in `artifacts/tfmc-live-versions.json` and
`artifacts/tfmc-version-responses.log`.

Runtime plugins were installed and enabled on Paper 1.21.10 on 2026-09-22:

- **TLibs 1.0**, supplied by the user, is installed as `server/plugins/TLibs.jar`,
  with a build link at `dependencies/TLibs.jar`. This binary includes the SQLite
  API required by VehicleFramework. The earlier public release is backed up under
  `downloads/before-user-tlibs-20260922/`.
- **VehicleFramework 1.1.12**, built from source snapshot
  `bfdb59ba651723200b364b132c0b6969244389ef`, is installed as
  `server/plugins/VehicleFramework.jar`. All **369 Maven tests passed**.
- **ModelEngine R4.1.1**, supplied by the user, is installed as
  `server/plugins/ModelEngine.jar`. It replaces the earlier official R4.1.0 Free
  edition; that jar and configuration are backed up under
  `downloads/before-user-models-20260922/`.

Original public jars and provenance are in `downloads/` and
`downloads/modelengine-tlibs.json`; the later user-supplied runtime is recorded in
`downloads/user-assets.json`. The separate R4.1.1 jar recovered from the earlier investigation was
an API artifact, distinct from the user's complete runtime installed now.
TLibs's source build also requires
ItemsAdder, MMOItems, MythicLib, GunsAndGadgets and Cooking jars.

The user supplied **68 models and 47 YAML config files**. Original archives and
checksums are in `downloads/` and `downloads/user-assets.json`; the complete model
archive is expanded under `assets/models/user-supplied/`. ModelEngine blueprints
contain only `.bbmodel` files (their textures are embedded). The generated pack
is copied to `assets/resourcepacks/vehicleframework-models.zip` and selected in
the isolated client's `client/resourcepacks/` folder.

TFMC's complete server resource pack was recovered from the existing Prism cache
(last used 2026-09-22). An unchanged copy is at
`assets/resourcepacks/tfmc-cached.zip` and `client/resourcepacks/tfmc-cached.zip`;
provenance and hashes are in `downloads/tfmc-cached-pack.json`. It supplies the
custom vehicle sounds and other TFMC client assets. The isolated client selects
this pack below `vehicleframework-models.zip`, so locally generated ModelEngine
assets take precedence. The cached ZIP uses unusual local entry names; keep it
intact rather than extracting it. Java can read its metadata and sound definitions.

Only configuration files were installed into `server/plugins/VehicleFramework/`.
Production logs, saved vehicles, database sidecars and TFMC_Map tracks remain in
the original archive. The lab uses fresh test-world data. Two referenced optional
skins are absent: `biplane_zerratoris` and `passenger_car_glass_roof`. Configs also
reference MMOItems items and custom sounds not provided by this model pack.

The unchanged VehicleFramework POM currently expects these build filenames in
`dependencies/` (these are legacy compile references, not the live versions above):

```text
ModelEngine-4.0.8.jar
TLibs.jar
MythicMobs-5.8.0-SNAPSHOT.jar
```

All system-path filenames are now staged. The legacy ModelEngine filename links
to the installed R4.1.1 runtime; MythicMobs is the official Maven compile artifact
`5.8.0-20250211.022403-143`, not an installed runtime plugin. Run `./bin/lab build` to check
dependencies, compile, run tests and package using the existing POM. Linux paths
are supplied with Maven properties; the project's POM is not rewritten.
Maven may still need network access for its normal dependencies.
Successful builds go to `artifacts/builds/`. Stop the server before installing
or replacing plugin jars, then start it and check `server/logs/latest.log` for
successful plugin enablement. Do not treat the base bot smoke test as a vehicle test.
The successful build is recorded in `artifacts/vehicleframework-build.log`.
`artifacts/vehicle-spawn-smoke.json` records successful spawns of `small_car`,
`simple_locomotive` and `coal_car`, with their model entities received by a real
protocol client. The graphical client loaded the pack and rendered the car;
see `artifacts/vehicle-models-visual.png`. SQLite saved all three vehicles on clean
shutdown. Those initial smoke checks did not cover driving, coupling or weapons;
the later interactive checks are recorded in TEST-RESULTS.md.

To experiment, run `./bin/lab play`, grant the isolated player admin commands with
`./bin/lab console "op VehicleTester"`, and use `/vf spawn small_car` in game.
The three test vehicles are near `(0, -60, 0)`, `(25, -60, 0)` and `(45, -60, 0)`.
`fishingboat` is a supplied model only; the archive includes no fishingboat vehicle
configuration. MMOItems-based tools, fuel and ammunition now have their supplied
plugin/configs installed, as detailed below.

From the user's `/home/ryan/Downloads/refs2.zip`, ItemsAdder **4.0.18** and
MythicLib **1.7.1-SNAPSHOT (20260819.194904-107)** were installed and enabled.
ItemsAdder uses no-host mode with automatic pack application disabled; the client
already selects both local packs. MMOItems **6.10.1-SNAPSHOT (20250521.175300-22)**
failed during construction in MythicLib's `MMOPlugin` and was removed from
`server/plugins/`; the tested jar remains in `downloads/refs2-selected/`.
See `artifacts/refs2-compatibility.log` and `downloads/refs2-selected.json`.
The user subsequently supplied MMOItems **6.10.1-SNAPSHOT build 59 (20260531)**,
MMOCore **1.13.1-SNAPSHOT build 59 (20260531)**, MythicLib **1.7.1 build 107**,
and MythicMobs **5.13.1-SNAPSHOT-88530541**. All four are now installed and enabled;
MMOItems integrates with ItemsAdder, MMOCore and MythicMobs, and TLibs registers
its MMOItems bridge successfully. Player connection/movement passes with this set.
See `downloads/mmo-suite-user.json` and `artifacts/mmo-suite-startup.log`.
The supplied `utils.yml` (39 definitions) and `item-types.yml` are now installed
under `server/plugins/MMOItems/`. Creation of all 14 required UTILS items was
verified through client inventory tags, including `/vf ammo` through TLibs; see
`artifacts/item-definition-smoke.json`. The installed `trains.yml` recorder path
was corrected from `m.utils.train_track_recoder` to `m.utils.train_track_recorder`
to match `TRAIN_TRACK_RECORDER`. Originals are backed up under
`downloads/before-user-item-definitions-20260922/`.
An actual right-click refuel test consumed one `ARCANE_FUEL` item and the car
reported `Fuel: 100/500`; see `artifacts/refuel-smoke.json`.

The user's `ItemsAdder.part1.rar` and `ItemsAdder.part2.rar` passed archive testing
and were extracted together into `assets/imports/itemsadder-20260922/ItemsAdder/`.
The five ItemsAdder rail definitions (`tfmc:track_small`, `track_medium`,
`track_large`, `railroad_switch`, `train_track`) and their required models/textures
are installed in `server/plugins/ItemsAdder/contents/tfmc_vehicle_test/`.
Their original model IDs were preserved to match the cached TFMC resource pack.
The full extracted folder remains available; unrelated contents, player storage,
hosting settings and library caches were not copied into the running server.
See `downloads/itemsadder-tracks.json` for provenance and ID mappings.

The optional MMOItems `MISCELLANEA/VEHICLE_REMOVER` definition from
`item/miscellanea.yml` is still absent. Default MMOItems sample
crafting recipes report missing sample types with TFMC's custom type configuration;
these recipes are unrelated to the verified vehicle items.

## Evidence and maintenance

`e2e-controller.cjs` is the interactive protocol harness used for the later tests.
Install it into `run/`, create `artifacts/e2e/`, then run
`node run/e2e-controller.cjs` from the lab root with an interactive stdin. It
accepts one JSON action per line, such as `{"action":"state"}` or
`{"action":"input","inputs":{"forward":true},"ticks":20}`. Inspect current
entity IDs before interacting; IDs from earlier runs are not reusable. The
harness ops only VehicleTestBot and deops/disconnects on quit or its 20-minute
deadline. Send `{"action":"quit"}` when finished. Raw evidence includes failed
early harness attempts; consult TEST-RESULTS.md for the accepted checks.

`e2e-visual.py` is the PC-side X11 helper for the isolated graphical client. It
requires python-xlib and ImageMagick and identifies the window by the PID of
`vehicleframework-e2e-visual.service`. It checks focus before input and saves
`artifacts/e2e/current.png`. It is not a generic controller for personal Prism
instances. See LEARNINGS.md for the protocol and asset integration pitfalls.

- `artifacts/bot-smoke.json`: bounded connection and movement test result.
- `artifacts/server-console.log`: startup/shutdown history.
- `server/logs/latest.log`: current Minecraft log and plugin enablement.
- `client/screenshots/`: screenshots made with Minecraft's F2 key.
- `downloads/manifest.json`: downloaded server, plugins and tools with SHA-256.
- `downloads/build-dependencies.json`: public compile-time dependency provenance.
- `bot/package-lock.json`: exact Node dependency resolution.

The files alongside this README are the maintained launcher sources. Installed
copies live in `bin/` and `bot/` within the lab. The server properties here are
initial defaults; editing this template does not overwrite the live world's settings.
Node dependencies can be restored with `npm ci` inside the installed `bot/`
folder. Its package metadata permits only canvas's required native install script
on npm versions supporting `allowScripts`. The initial 1.21.8 smoke world and
server jars are archived under `downloads/initial-1.21.8/`; all launchers use 1.21.10.

Useful upstream references: [Paper settings](https://docs.papermc.io/paper/reference/server-properties/),
[Mineflayer](https://github.com/PrismarineJS/mineflayer),
[client launch library](https://minecraft-launcher-lib.readthedocs.io/en/stable/modules/command.html),
[TLibs](https://github.com/Drefvelin/tlibs).
