# Configuration and commands

[Project index](README.md)

Runtime configuration lives in
[src/main/resources](https://github.com/TF-Minecraft/AdvancedCrafting/tree/main/src/main/resources).
The source defaults are examples; item paths and MMOItems templates must exist on
the target server. Existing files are preserved when the plugin enables.

| Files | Purpose |
| --- | --- |
| `config.yml` | Station/item paths, alloy discovery chance, stat offsets/aliases, permissions and debug logging |
| `ingredients.yml`, `ingredient-types.yml`, `conversions.yml` | Ingredient definitions, types and item conversions |
| `recipes/*.yml`, `recipe-categories.yml` | Crafting recipes, MMOItems template references, categories and ingredient quantities |
| `hit-types.yml`, `crafting-hits.yml` | Smithing action definitions and requirements |
| `qualities.yml`, `stats.yml`, `socket-groups.yml` | Quality tiers, stat templates and validated socket group references |
| `colour-schemes/`, `model-schemes/`, `naming-schemes/` | Material-dependent appearance and names |

`config.yml` defaults the crafting station to `v(ANVIL)` and the alloy/conversion
stations to ItemsAdder furniture paths. Alloy discovery chance is capped and uses
the configured base percentage plus the square root of total ingredient value
multiplied by its bonus. `global-stat-offsets` converts configured scales before
template factors; the supplied movement-speed offset is 100.

The admin permission is `advancedcrafting.admin` (operators by default).
Recipe/profession permissions use the configured `permission-prefix` and namespaces.

| Command | Effect |
| --- | --- |
| `/ac reload` | Reload configuration; supports console |
| `/ac inspect` | Inspect the player's held crafted item |
| `/ac refresh` | Force stat refresh of the player's held AdvancedCrafting item |
| `/ac sync recipes` | Inspect stored alloy recipe synchronisation |
| `/ac sync recipes repair` | Repair stored alloy recipe synchronisation; back up data first |
| `/ac give alloy <id> [player]` | Give an alloy item |
| `/ac give equipment <recipe> <ingredient.id\|alloy.id> [player] [quality]` | Give finished equipment using the separate staff permission described below |
| `/ac alloy info <id>` | Show alloy information |
| `/ac craft <percent>` | Arm the player's next station craft for 30 seconds, clamping quality to 0–100 |
| `/alloy name <name>` | Name an alloy through the existing player workflow |

All `/ac` actions above except `give equipment` require the admin permission.
`give equipment` uses its configured permission; `/alloy name` follows its own
alloy manager checks. Consult
[CommandManager](https://github.com/TF-Minecraft/AdvancedCrafting/blob/main/src/main/java/net/tfminecraft/advancedcrafting/managers/CommandManager.java)
for parsing and player/console restrictions. Use a restart when changing plugin
JARs; configuration reload does not replace loaded classes.

## Staff equipment grants

`/ac give equipment <recipe> <ingredient.id|alloy.id> [player] [quality]`
gives one finished item using a configured recipe and compatible main material.
For example, `/ac give equipment heavy_chestplate ingredient.steel_ingot Alex 100`.
Tab completion lists loaded recipes, compatible ingredients/alloys and online players.
Omit the player to give to yourself; console must specify an online player.
Quality defaults to 100 and accepts finite values from 0 to 100 (specify the player
before quality). Alloy IDs are the loaded discovery IDs, not display names.

Secondary recipe ingredients use the lowest configured tier, then ingredient ID
alphabetically to break ties. Their stats and appearance participate normally.
The item retains normal stats, quality sockets, appearance, tier and crafting
provenance; no materials are consumed and no XP or activity rewards are granted.
Full inventories drop the item at the recipient's location.

Set `give-equipment-permission` in `config.yml` and run `/ac reload` to change
access. Missing or blank settings default to `advancedcrafting.admin` (operators).
Grant a custom permission only to staff; it does not grant other admin commands.
