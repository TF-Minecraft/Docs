# ServerAssets (private)

[ServerAssets](https://github.com/TF-Minecraft/ServerAssets) stores plugin/API
binaries, configuration snapshots, ModelEngine blueprints and client resource
packs. Its `main` branch and `manifest.json` define the available assets.

## Contents

- `jars/`: plugin and API binaries, grouped by SHA-256 prefix with versioned filenames.
- `configs/`: plugin settings, MMOItems definitions, ItemsAdder content and captured ModelEngine resource dependencies.
- `configs/Archaeo/`: TFMC's Archaeo preset and lore catalogs, preserved from the
  source repository. See [configuration ownership and installation](../Archaeo/docs/configuration.md).
- `models/`: ModelEngine blueprints and editable ItemsAdder model sources.
- `resourcepacks/`: client resource packs.
- `manifest.json`: file paths, sizes, checksums, provenance and dependency mappings.

Assets are maintained on `main`; this repository does not publish versioned releases.
Pin a commit SHA for reproducible build inputs. Keep licensed binaries and
private configurations in this repository. Use the [jar inventory](JARS.md)
for dependency selection.

## Verify assets

Run from an authorized checkout of ServerAssets `main`:

```sh
python3 -m pip install PyYAML==6.0.3
python3 tools/verify.py
python3 tools/verify_magic.py
python3 tools/verify_companionpets.py
```

CI checks the size and SHA-256 checksum of every file in the manifest, rune and
spell bindings, and CompanionPets provider and resource references. Results are
printed to the terminal; there is no coverage gate. These checks do not establish
the current live deployment or verify client rendering. Keep private snapshot
instructions with the assets in ServerAssets.
For the Archaeo configuration import, these checks verify the transfer; its
`unverified-import` role does not claim runtime validation.

Use each consuming plugin's committed dependency scripts and checksums to select
build inputs. See the [shared pipeline guide](../../PIPELINES.md#build-dependencies).
