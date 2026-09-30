# Recycler - System design

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

Every provider uses the same formula with its own rate:

```
final_amount = floor(base_amount * return_rate * durability_factor * stack_amount)
```

`return_rate` comes from `return_rates` in `config.yml` (Recycler 0.3.0+):

| Key | Provider | Default |
|-----|----------|---------|
| `advanced_crafting` | `AdvancedCraftingProvider` | `0.5` |
| `alloy_scrap` | `AlloyScrapProvider` | `0.5` (1 base metal per 2 scrap) |
| `magic_gear` | `MagicGearProvider` | `0.5` |
| `guns` | `GunsAndGadgetsProvider` | `0.5` |
| `goldsmith_jewelry` | `GoldsmithProvider` | `0.5` |
| `recipes` | `ConfigProvider` | `1.0` (the amounts written in `recipes/*.yml`) |

- Rates are clamped to `0.0`-`1.0` with a console warning; non-finite values use the default.
- A missing key falls back to the pre-0.3.0 keys when present: `max_return_rate` for the four crafted-item providers, `scrap_return_rate` for alloy scrap.
- `durability_factor`: `0.0` when broken, `1.0` when full (`1.0` for items without durability). MMOItems custom durability (`MMOITEMS_DURABILITY` / `MMOITEMS_MAX_DURABILITY`, used by AdvancedCrafting gear) wins when present; a missing `MMOITEMS_DURABILITY` means never damaged. Otherwise the vanilla damage against the item's `max_damage` component (MMOItems `max-item-damage`, e.g. mage weapons), or the material's default maximum. Before Recycler 0.3.1 this factor was always `1.0` for our gear.
- `stack_amount`: full stack placed in station (one stack per deposit).
- Use `floor`; zero yield blocks confirm when `block_confirm_when_zero_yield` is true.

## Provider inputs

Every provider returns what actually went into the item, never the recipe as it reads today. Items crafted before their plugin recorded this are not handled (the station says they cannot be recycled).

### AdvancedCrafting (crafted items)

Read `CraftProvenance` from item PDC (`ac_craft_inputs` JSON list of kind/id/amount/revision), which lists the deposited inputs.

Map `ingredient.*` inputs to live `Ingredient.getPath()` x stamped amount. Map `alloy.*` inputs by decomposing each alloy's forge recipe (base + catalyst ingredient paths) x stamped amount.

Raw AC ingredients/alloys (`ac_ingredient_id` / `ac_alloy_id`) are not provenance-backed - handle via config recipes or a future AC rule.

### AdvancedCrafting (alloy scrap)

A failed alloy forge tags its scrap with the base ingredient id (`ac_scrap_base`, AdvancedCrafting 2.2.0+). `AlloyScrapProvider` reads it with `ScrapProvenance.readBaseId` and returns one live `Ingredient.getPath()` per scrap, scaled by `alloy_scrap`. Output rounds down per deposit, so a single scrap at `0.5` is a zero-yield deposit; players stack scrap first. Scrap forged before 2.2.0 has no tag and is not handled. Scrap from different base metals does not stack.

### Magic (mage weapons)

Magic 0.4.7+ stamps the materials a craft actually charged on the weapon (`magic:gear_craft_inputs`, JSON item path to amount; empty for staff bypass crafts) and carries it through socket rewrites and refreshes. `MagicGearProvider` reads it with `GearProvenance.readInputs`. Broken weapons, weapons with socketed runes, and weapons without the stamp are not handled.

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
