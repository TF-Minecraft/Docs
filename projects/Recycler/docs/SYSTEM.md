# Recycler - System design

[Recycler](../README.md) · [All projects](../../../README.md)

Player-facing recycling station at ItemsAdder furniture `iaf(tfmc:recycling_station)`.

## Station interaction

1. Right-click furniture (TLibs `BlockChecker` on configured path).
2. Open 27-slot GUI (9x3 chest).
3. Click item in player inventory to deposit into the station (one stack max for stackables).
4. Right side previews scaled outputs; left side shows input at slot 10.
5. Click confirm (slot 0, `ia.mcicons:icon_confirm`) to recycle.
6. Close without confirm returns the escrowed item.

## GUI layout (fixed slots)

| Slot | Role |
|------|------|
| 0 | Confirm (`ia.mcicons:icon_confirm`) |
| 3, 12, 21 | Arrow decorators (`ia.mcicons:icon_right_gray`, blank display, hidden tooltip) |
| 10 | Input item display |
| Cols 0-2 except 10 | Gray glass filler (blank display, hidden tooltip) |
| Cols 4-8 | Preview outputs (up to 15 slots) |

Reference: `util/GridLayout.java`.

## Return math

Every provider except alloy scrap uses the same formula with its own rate:

```
final_amount = floor(base_amount * return_rate * durability_factor * stack_amount)
```

`return_rate` comes from `return_rates` in `config.yml` (Recycler 0.3.0+):

| Key | Provider | Default |
|-----|----------|---------|
| `advanced_crafting` | `AdvancedCraftingProvider` | `0.5` |
| `alloy_scrap` | `AlloyScrapProvider` | `0.5` (chance per recorded base unit; see [alloy scrap](#advancedcrafting-alloy-scrap)) |
| `magic_gear` | `MagicGearProvider` | `0.5` |
| `guns` | `GunsAndGadgetsProvider` | `0.5` |
| `goldsmith_jewelry` | `GoldsmithProvider` | `0.5` |
| `recipes` | `ConfigProvider` | `1.0` (the amounts written in `recipes/*.yml`) |
| `artifacts` | `ArtifactProvider` | `1.0` (the rarity amounts in `artifact_returns`) |

- Rates are clamped to `0.0`-`1.0` with a console warning; non-finite values use the default.
- A missing key falls back to the pre-0.3.0 keys when present: `max_return_rate` for the four crafted-item providers, `scrap_return_rate` for alloy scrap.
- `durability_factor`: `0.0` when broken, `1.0` when full (`1.0` for items without durability). MMOItems custom durability (`MMOITEMS_DURABILITY` / `MMOITEMS_MAX_DURABILITY`, used by AdvancedCrafting gear) wins when present; a missing `MMOITEMS_DURABILITY` means never damaged. Otherwise the vanilla damage against the item's `max_damage` component (MMOItems `max-item-damage`, e.g. mage weapons), or the material's default maximum. Before Recycler 0.3.1 this factor was always `1.0` for our gear.
- `stack_amount`: full stack placed in station (one stack per deposit).
- Use `floor`; zero yield blocks confirm when `block_confirm_when_zero_yield` is true.
- Alloy scrap rolls a chance per material unit instead; see [alloy scrap](#advancedcrafting-alloy-scrap).

## Provider inputs

Crafted equipment providers read recorded inputs. AdvancedCrafting ingredient
paths and alloy recipes are resolved from current definitions, as described
below. Items without the required crafting record are skipped by those
providers; an explicit config recipe may still handle them. Artifact and config
providers use configured outputs instead of crafting records.

### AdvancedCrafting (crafted items)

Read `CraftProvenance` from item PDC (`ac_craft_inputs` JSON list of kind/id/amount/revision), which lists the deposited inputs.

Map `ingredient.*` inputs to live `Ingredient.getPath()` x stamped amount. Map `alloy.*` inputs by decomposing each alloy's forge recipe (base + catalyst ingredient paths) x stamped amount.

Raw AC ingredients/alloys (`ac_ingredient_id` / `ac_alloy_id`) are not provenance-backed; use config recipes to recycle them.

### AdvancedCrafting (alloy scrap)

Scrap recovery requires AdvancedCrafting 2.2.5 or newer. A failed alloy forge tags its scrap with the base ingredient id (`ac_scrap_base`) and records the quantity of every ingredient it consumed, base and catalysts (`ac_scrap_inputs`). `AlloyScrapProvider` handles any scrap with a base tag and reads the inputs with `ScrapProvenance.readInputs`. Scrap with only a base tag (forged before the inputs were recorded) returns only its recorded base, since its catalysts were never saved. Scrap with no base tag is not handled. Scrap with different recorded inputs does not stack.

Each recorded input maps to its live `Ingredient.getPath()`; ingredients missing from AdvancedCrafting are skipped with a console warning. Every recorded unit in each stacked scrap rolls once, independently, on confirmation:

- **Base:** the chance is `return_rates.alloy_scrap`. The base always uses this rate and bypasses the catalyst whitelist.
- **Catalysts:** only paths matching `scrap_catalyst_return_rates.whitelist_paths` can return. Each uses the rate for its live AdvancedCrafting ingredient tier.

A failed roll still consumes the scrap. The preview lists every possible quantity with a "Recovery chance" lore line and does not roll. Lines with a `0` chance are omitted, so scrap whose lines all have a zero chance is a zero-yield deposit. Durability does not affect scrap.

```yaml
scrap_catalyst_return_rates:
  whitelist_paths:
    - m.gemstones.*
  default: 0.01
  tiers:
    '1': 0.01
    '2': 0.25
    '3': 0.5
    '4': 0.75
```

| Key | Default | Effect |
|-----|---------|--------|
| `whitelist_paths` | `[m.gemstones.*]` | Catalyst item paths that may return: case-insensitive exact paths, or prefixes ending in `*`. Every other catalyst is excluded; `[]` excludes all catalysts. |
| `tiers.<tier>` | `1`: `0.01`, `2`: `0.25`, `3`: `0.5`, `4`: `0.75` | Chance per catalyst unit by AdvancedCrafting ingredient tier. Tiers 1-4 keep their defaults unless overridden; other tier keys may be added. |
| `default` | `0.01` | Chance for tiers not listed under `tiers`. |

Rates use `0.0`-`1.0`: out-of-range values are clamped and non-finite values reset to the default, with a console warning. When `scrap_catalyst_return_rates` is absent, the legacy `scrap_gem_return_rates` section supplies `tiers` and `default`, and the whitelist stays at its gem-only default.

### Magic (mage weapons)

Magic 0.4.7+ stamps the materials a craft actually charged on the weapon (`magic:gear_craft_inputs`, JSON item path to amount; empty for staff bypass crafts) and carries it through socket rewrites and refreshes. `MagicGearProvider` reads it with `GearProvenance.readInputs`. Broken weapons, weapons with socketed runes, and weapons without the stamp are not handled.

### Magic (artifacts)

`ArtifactProvider` returns the configured item by the artifact's recorded
rarity. Artifacts are found rather than crafted, so they do not need a crafting
record. Stored aura is lost.

```yaml
artifact_returns:
  min_muffle: 0.0
  item: m.currency.enchanted_dust
  rarities:
    common: 4
    uncommon: 8
    rare: 12
    epic: 16
    legendary: 28
  default: 4
```

The default `min_muffle: 0.0` accepts any artifact; `1.0` requires it to be fully
muffled. Missing or unrecognised stored rarities use `default`. Omitted standard
rarity keys retain their shipped defaults; set a rarity to `0` to refuse it.
Artifacts below the muffle requirement or with no configured output are refused
before recipe fallback, so a matching config recipe cannot bypass these rules.

`return_rates.artifacts` multiplies these amounts using the normal return math.
The shipped rarity table is tuned so recycling the artifacts from a Dowsing
Artifact Mine node yields roughly half the enchanted dust of a Dust Mine node.

### GunsAndGadgets (guns)

GunsAndGadgets 2.0.6+ stamps the materials a craft actually took on the gun (`gunsandgadgets:gg_craft_inputs`; empty for staff bypass or when inputs are not required) and keeps it through stat refreshes. `GunsAndGadgetsProvider` reads it with `GunCraftInputs.readFrom`. Broken guns and guns without the stamp are not handled.

### Goldsmithing (GemInfusion jewelry)

A bench slot accepts any material of its type, so the project recipe is not always what went in. GemInfusion 2.2.5+ stamps the deposited materials on the finished piece (`geminfusion:goldsmith_inputs`); `GoldsmithProvider` reads it with `GoldsmithProvenance.read`. The infused gem is not returned. Pieces with socketed gems and pieces without the stamp are not handled.

### Config fallback (`recipes/*.yml`)

Recipe id is a label; matching uses the `input` tlibs path.

```yaml
recipes:
  iron_sword:
    input: v.iron_sword
    outputs:
      - v.iron_ingot 2
      - m.materials.steel_ingot 1
```

Each output line is `path amount` or `path(amount)`. Legacy map-style outputs under a path key are still supported.

Matched via `TLibs ItemChecker`. The listed amounts are scaled by `return_rates.recipes` and durability.

## Confirm flow

1. Validate escrow + non-zero yield.
2. Set `session.confirmed = true` (so close handler does not return input).
3. Clear escrow file.
4. `player.closeInventory()` immediately so outputs can be picked up in the world.
5. Play processing VFX at station block.
6. Spawn each output with Research-style kick-out (`ResultSpawnEffects` pattern): upward velocity, crit trail, staggered ticks.

## Sounds and effects (whole interaction)

Configured in `config.yml` under `effects`:

| Moment | Config key |
|--------|------------|
| Open station | `open` |
| Item accepted | `input_accept` |
| Item rejected | `input_reject` |
| Preview refresh | `preview_refresh` |
| Confirm click | `confirm` |
| Complete | `complete` |
| Cancel / return | `cancel` |

Confirmation uses particles and a wave animation.

## Deposit policy

Configured under `deposit` in `config.yml`. `RecycleGuard` runs before provider resolution:

- `whitelist_mode`: only paths in `whitelist_paths` may be deposited (prefix match with trailing `*` supported).
- Otherwise `blacklist_paths` block matching paths.
- `block_unbreakable`: reject items with `ItemMeta.isUnbreakable()`.

Rejected deposits use `station.blocked` and the input-reject sound.

## Profession hooks

`RecycleCompleteEvent` fires after a successful confirm (player, input clone, provider id, scaled outputs, station location). Other plugins (e.g. Professions) may listen for perks or logging.

`professions.recycler_1/2/3` currently unlock crafting recipes (raw gold/iron/diamonds). Perks that bump the return rates or gate station access are not implemented in Recycler itself.
