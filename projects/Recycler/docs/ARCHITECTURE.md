# Recycler - Architecture

[Recycler](../README.md) · [All projects](../../../README.md)

Recycler resolves item provenance through its provider chain and persists deposited items in escrow before recycling.

## Package map

```text
net.tfminecraft.recycler/
  Recycler.java              # bootstrap, folders, reload
  Cache.java                 # scalars from config.yml
  GuiCache.java              # item refs from gui.yml
  Messages.java              # messages.yml

  loader/
    ConfigLoader.java
    GuiLoader.java
    RecipeLoader.java        # recipes/*.yml fallback registry

  model/
    RecycleOutput.java
    RecycleSession.java

  event/
    RecycleCompleteEvent.java

  provider/
    RecycleProvider.java
    RecycleContext.java
    RecycleResult.java
    RecycleProviderChain.java
    AdvancedCraftingProvider.java
    AlloyScrapProvider.java
    MagicGearProvider.java
    GunsAndGadgetsProvider.java
    GoldsmithProvider.java
    ConfigProvider.java

  manager/
    RecyclerManager.java     # Listener: station, GUI lifecycle
    InventoryManager.java    # GUI build + preview
    EscrowManager.java       # crash-safe held items

  gui/
    RecyclerGuiHolder.java

  util/
    GridLayout.java
    DurabilityScaler.java
    RecycleGuard.java
    ItemRef.java
    ItemGive.java

  command/
    CommandManager.java
```

## Provider chain

Specialized providers run before the config fallback:

| Priority | Provider | When active |
|----------|----------|-------------|
| 10 | `AdvancedCraftingProvider` | AdvancedCrafting plugin present |
| 11 | `AlloyScrapProvider` | AdvancedCrafting present; scrap tagged with its base ingredient |
| 15 | `MagicGearProvider` | Magic present; weapon has `gear_craft_inputs` (Magic 0.4.7+) |
| 20 | `GunsAndGadgetsProvider` | GunsAndGadgets present; gun has `gg_craft_inputs` (2.0.6+) |
| 25 | `GoldsmithProvider` | GemInfusion present; piece has `goldsmith_inputs` (2.2.5+) |
| max | `ConfigProvider` | Always (yaml recipes) |

Resolution flow:

1. `canHandle(item)` on each provider in order.
2. `resolveBaseOutputs(item)` returns base material amounts.
3. `RecycleContext` applies the provider's `returnRate()` (its `return_rates` entry: 0.5 by default, 1.0 for config recipes) and durability factor.
4. `floor(base * rate * durability * stackSize)` per output line. Alloy scrap lines carry a per-unit chance instead; `RecycleResult.roll()` rolls them only on confirmation.

## Escrow (crash safety)

The GUI is **not** the source of truth for the input item.

1. On accept: remove from player inventory, store in `EscrowManager`, write `data/escrow/<uuid>.json` immediately.
2. On cancel/close/quit: return from escrow, delete file.
3. On confirm: clear escrow first, then consume and spawn outputs.
4. On disable: return all online players; offline entries move to `data/pending_returns/`.
5. On join: deliver any pending return file.

## Dependencies

- **Required:** TLibs, ItemsAdder (station block + icons)
- **Soft:** AdvancedCrafting, Magic, GunsAndGadgets, GemInfusion, MMOItems

AdvancedCrafting, Magic, and GunsAndGadgets providers require stamped provenance from those plugins. The alloy scrap provider needs AdvancedCrafting 2.2.5 or newer (`ScrapProvenance.readInputs`). Magic, GunsAndGadgets and goldsmithing need the craft-input stamps from Magic 0.4.7, GunsAndGadgets 2.0.6 and GemInfusion 2.2.5. Admin escrow tooling: `/recycler escrow list|return`.

## What not to add yet

- One file per GUI slot
- Hardcoded item ids outside yaml
- Putting the escrow item only in the chest inventory without disk backup
