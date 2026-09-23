# ServerAssets (private)

[ServerAssets](https://github.com/TF-Minecraft/ServerAssets) stores plugin/API
binaries, configuration snapshots, ModelEngine blueprints and client resource
packs. Its `main` branch and `manifest.json` define the available assets.

## Contents

- `jars/`: plugin and API binaries, grouped by SHA-256 prefix with versioned filenames.
- `configs/`: plugin settings, MMOItems definitions and ItemsAdder rail assets.
- `configs/Archaeo/`: TFMC's Archaeo preset and lore catalogs, preserved from the
  source repository. See [configuration ownership and installation](../Archaeo/docs/configuration.md).
- `models/`: ModelEngine blueprints with embedded textures.
- `resourcepacks/`: client resource packs.
- `manifest.json`: file paths, sizes, checksums, provenance and dependency mappings.

The retained ItemsAdder content is the rail subset. Keep licensed binaries and
private configurations in this repository. Use the [jar inventory](JARS.md)
for dependency selection.

## Verify assets

Run from an authorized checkout of ServerAssets `main`:

```sh
python3 tools/verify.py
```

Verification checks the size and SHA-256 checksum of every file in the manifest.
For the Archaeo configuration import, these checks verify the transfer; its
`unverified-import` role does not claim runtime validation.

Use each consuming plugin's committed dependency scripts and checksums to select
build inputs. See the [shared pipeline guide](../../PIPELINES.md#build-dependencies).
