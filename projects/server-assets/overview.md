> Canonical documentation: [TF-Minecraft/docs](https://github.com/TF-Minecraft/docs). [Source snapshot](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/README.md). Commands and plain-text code/config paths refer to the source repository unless stated otherwise.

> This page is public; linked jars, models and configurations remain in the private server-assets repository and require access. The full ItemsAdder contents archive was removed from server-assets on 2026-09-22; historical lab notes below describe the original snapshot. The existing manifest/materializer may still expect that archive.

# TFMC server assets (private)

Versioned inputs for the TFMC Minecraft 1.21.10 test lab, captured 2026-09-22.
The source, launchers and integration findings are on
[vehicleframework: chore/cachyos-lab-learnings](https://github.com/TF-Minecraft/vehicleframework/tree/chore/cachyos-lab-learnings/tools/minecraft-lab).

## Contents

- `runtime/plugins/`: the ten original plugin jars enabled in the tested lab.
- `runtime/server/`: Paper 1.21.10 build 130.
- `jars/`: other distinct supplied/reference and historical plugin/API binaries.
- `configs/`: the tested VehicleFramework configs, MMOItems UTILS and item types,
  the five ItemsAdder rail item definitions plus their assets, and the lab's
  ModelEngine/ItemsAdder settings.
- `models/`: all 68 supplied ModelEngine blueprints with embedded textures.
- `resourcepacks/`: unchanged cached TFMC pack and the locally generated ModelEngine pack.
- `archives/`: the complete supplied ItemsAdder contents, reconstructed from both RAR volumes.
- `manifest.json`: SHA-256, byte lengths, original filenames/sources, roles and build aliases.
- `JARS.md`: human-readable inventory, with the tested runtime separated from other versions.
- `docs/`: test results, findings and local lab setup notes.

Identical jars from multiple sources are stored once, with all source aliases
recorded in the manifest. Runtime jars are the original inputs, not Paper's
remapped caches. Downloaded transitive libraries, personal launcher accounts,
production databases, player data and machine credentials are not part of this snapshot.
Older jars are retained for reference, not included in the runtime plugin folder.

## Verify and prepare

```sh
git clone https://github.com/TF-Minecraft/server-assets.git
cd server-assets
python3 tools/verify.py
python3 tools/materialize.py /path/to/an/empty-lab
```

Materialization verifies every recorded asset, copies the tested runtime and
localhost-only server properties,
configuration, blueprints and resource packs, and recreates the build dependency
filenames from the manifest. It refuses a nonempty destination and does not
start Minecraft, accept an EULA, or replace a running installation. Install the
launchers and isolated Java/Maven/client tooling described in `docs/LAB.md`.
The existing CachyOS lab is already installed under
`/home/ryan/.local/share/blightfront-test-runner/vehicleframework/`.

Select `tfmc-cached.zip` below `vehicleframework-models.zip` in the client.
Keep the cached pack intact: Java can read it, but its unusual ZIP local entry
names cause some Python extraction tools to reject entries. Checksum verification
is safe. The full ItemsAdder archive is retained; only the rail subset is
integration-tested and materialized by default.

## Validated scope

The source build at `bfdb59ba651723200b364b132c0b6969244389ef` passed 369 tests.
Fresh cars, rail placement, fresh train coupling/movement, and artillery reload,
firing and a controlled 28-damage hit passed runtime checks. Some older/restored
vehicles lost usable model/seat state or train following. That restoration issue
remains unresolved; see `docs/TEST-RESULTS.md` for evidence and limitations.

The older public TLibs lacks the required SQLite API, and MMOItems build 22 failed
with this MythicLib stack. Use `runtime/plugins/` as a set. The build alias
`ModelEngine-4.0.8.jar` deliberately maps to the tested R4.1.1 binary; it does not
identify the runtime version. No third-party binaries have been relicensed.
