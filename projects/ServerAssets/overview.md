# ServerAssets (private)

[ServerAssets](https://github.com/TF-Minecraft/ServerAssets) stores plugin/API
binaries, configuration snapshots, ModelEngine blueprints and client resource
packs. Its `main` branch and `manifest.json` define the available assets.

## Contents

- `runtime/plugins/` and `runtime/server/`: stored plugin and Paper binaries.
- `jars/`: additional plugin and API inputs, identified by the manifest.
- `configs/`: plugin settings, MMOItems definitions and ItemsAdder rail assets.
- `configs/Archaeo/`: TFMC's Archaeo preset and lore catalogs, preserved from the
  source repository. See [configuration ownership and installation](../Archaeo/docs/configuration.md).
- `models/`: ModelEngine blueprints with embedded textures.
- `resourcepacks/`: client resource packs.
- `manifest.json`: file paths, sizes, checksums, provenance and dependency mappings.

The retained ItemsAdder content is the rail subset. Keep licensed binaries and
private configurations in this repository. Use the [jar inventory](JARS.md)
for dependency selection.

## Verify and prepare

Run from an authorized checkout of ServerAssets `main`:

```sh
python3 tools/verify.py
python3 tools/materialize.py /path/to/an/empty-lab
```

Materialization verifies the manifest, copies its runtime and configuration set,
blueprints and resource packs, and creates the mapped dependency filenames.
This includes the Archaeo configuration import, whose checksums verify the
transfer but whose `unverified-import` role does not claim runtime validation.
It does not add or enable an Archaeo runtime JAR.
It requires an absent or empty destination and does not start Minecraft or
accept its EULA. The stored runtime set is an asset input; build the TFMC plugins
from `main` using their committed dependencies before testing current source.

See the [test lab guide](docs/LAB.md) for the installed tooling and
[integration notes](docs/LEARNINGS.md) for asset and protocol requirements.

## Validation

Use Java 21 and Paper 1.21.10 under the [shared baseline](../../PLATFORM.md).
Record the source commit, dependency checksums, server version, configuration and
results for each run. Check fresh vehicles and persistence after unload/restart,
as well as rail placement, train coupling, movement, weapons and client rendering.
Store logs and captures with the run or PR; compilation alone does not verify
these behaviors.
