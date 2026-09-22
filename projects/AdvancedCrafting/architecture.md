# Architecture, data and integrations

[Project index](README.md)

## Source ownership

The root package is `net.tfminecraft.advancedcrafting` (case-sensitive).
`AdvancedCrafting` owns enable/disable, default files, loaders, listeners and
manager startup. `Loaders` interpret YAML registries. `Managers` own station,
alloy, ingredient and command interactions. `Objects` contains recipes, craft
state, ingredients, alloys, schemes and stat templates. `Utils` handles stat
calculation/refresh, permissions, lore, item tags and provenance.

Enable loads revision metadata, schemes, categories, stats, socket groups and
recipes before ingredient/hit/quality configuration, then registers listeners and
starts the managers. Socket groups load before recipes so their references can
be validated. Item refresh listeners and MMOItems rebuild handling apply revision
changes to existing items.

## Persistence

Back up `plugins/AdvancedCrafting/` as a whole, including configuration and data.
Stations are JSON files under `data/stations`; alloy state is under `data/alloys`;
alloy recipes are under `data/alloy-recipes`. `data/revisions.json` tracks item
configuration revisions. `data/forged-alloys/<player-uuid>.json` tracks each
player's discovered/forged alloys. Crafted items also retain tags and provenance
in their persistent data containers.

On disable the plugin flushes revisions, clears saved station files, and rewrites
stations from the in-memory manager. Use a clean stop for backups and restores;
do not delete or replace live data while the plugin runs. This repository import
and dependency migration do not change persistence formats or player data.

## Public API

Events live in `net.tfminecraft.advancedcrafting.lifecycle`:

| Event | Payload |
| --- | --- |
| `ItemCraftedEvent` | Player, player UUID, recipe ID, category ID |
| `SmithingHitEvent` | Player, player UUID, hit ID |
| `AlloyCraftedEvent` | Player, player UUID, alloy ID |
| `AlloyDiscoveredEvent` | Player, player UUID, alloy ID on their first recorded forge |

`CraftLifecycle.fireAlloyOutcome` records the forge, emits `AlloyCraftedEvent`,
then emits `AlloyDiscoveredEvent` for a first forge. Category, hit and alloy IDs
are normalised in the lifecycle helpers. Events expose ordinary Bukkit HandlerLists.
`Utils.ThieveryBridge` provides guarded ingredient/alloy/provenance access for
Thievery. Recycler uses item/craft types; ActivityTF and TFMCCore consume lifecycle
APIs. The bridge class does not create a compile-time dependency on Thievery.

Consumers declare `net.tfminecraft:advancedcrafting` with `provided` scope and
`${advancedcrafting.version}`. The shared installer downloads the published API
JAR, checks its hash and installs a minimal POM. Runtime plugins remain separate;
provider implementation dependencies are not transitively copied or shaded.
See [build dependency management](../../PIPELINES.md#build-dependencies).
