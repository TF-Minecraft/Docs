# Configuration ownership

[Archaeo documentation](../README.md)

Archaeo has three configuration sets with different purposes. Choose the set
for your server; they are not interchangeable copies.

| Set | Maintained location | Purpose |
| --- | --- | --- |
| Plugin defaults | [Archaeo `src/main/resources/`](https://github.com/TF-Minecraft/Archaeo/tree/main/src/main/resources) | Bundled vanilla-item defaults and generic catalogs, copied into the plugin data folder when missing. |
| Optional custom-pack preset | [Archaeo `pack/plugins/Archaeo/config.yml`](https://github.com/TF-Minecraft/Archaeo/blob/main/pack/plugins/Archaeo/config.yml) | MMOItems and ItemsAdder item mappings; use with the [pack installation guide](pack-installation.md) and default catalogs. |
| TFMC settings and lore | [Private ServerAssets `configs/Archaeo/`](https://github.com/TF-Minecraft/ServerAssets/tree/main/configs/Archaeo) | Server-specific configuration and catalogs, formerly under `Archaeo/TFMC/configs/`. Requires access to ServerAssets. |

`plugin.yml` is build metadata. Its sole maintained copy is in
`Archaeo/src/main/resources/`; Maven filters its version into the JAR. Do not
copy a separate `plugin.yml` into the server's plugin data folder.

## Install the TFMC configuration

The seven YAML files were transferred unchanged from Archaeo commit
`bbe3a6dbe85039dd15bb0f58ed4b6a3b46298923`. The move preserves their content;
it does not establish that this preset or its external item mappings passed
runtime testing. ServerAssets records their original source, size, and checksum
in `manifest.json` with the `unverified-import` role.

1. Stop the Minecraft server and back up its existing `plugins/Archaeo/` folder.
2. Install the Archaeo JAR in `plugins/` and the external item definitions needed
   by the preset. Check its MMOItems and ItemsAdder IDs against the packs you
   actually load; the optional generic pack uses some different IDs.
3. Copy all seven files from `ServerAssets/configs/Archaeo/` into
   `plugins/Archaeo/`: `config.yml`, `artifacts.yml`, `hints.yml`, `interest.yml`,
   `interpretations.yml`, `materials.yml`, and `strata.yml`. Keep these catalogs
   together because their material, artifact, and interpretation IDs refer to
   one another. Preserve any existing world/site data in the data folder.
4. Start the server and check item resolution and the catalogs using the
   [lore editing checklist](lore-catalogs.md).

Do not subsequently overwrite this `config.yml` with the optional generic pack
preset. Make TFMC adjustments in ServerAssets; keep generic plugin defaults in
Archaeo. Updating a JAR does not replace existing server configuration files.

ServerAssets' materializer copies the entire `configs/` tree, including this
preset, into the prepared lab's `server/plugins/` directory. The import does not
add or enable an Archaeo runtime JAR or change the recorded lab validation scope.
