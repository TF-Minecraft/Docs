# Recycler - Architecture

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
| 11 | `AlloyScrapProvider` | AdvancedCrafting present; scrap tagged with its base metal |
| 15 | `MagicGearProvider` | Magic present with stamped gear provenance |
| 20 | `GunsAndGadgetsProvider` | GunsAndGadgets present with stamped provenance |
| 25 | `GoldsmithProvider` | GemInfusion present; item matches one jewelry project |
| max | `ConfigProvider` | Always (yaml recipes) |

Resolution flow:

1. `canHandle(item)` on each provider in order.
2. `resolveBaseOutputs(item)` returns base material amounts.
3. `RecycleContext` applies the provider's `returnRate()` (`max_return_rate`, default 0.8; `scrap_return_rate`, default 0.5, for alloy scrap; 1.0 for config recipes) and durability factor.
4. `floor(base * rate * durability * stackSize)` per output line.

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

AdvancedCrafting, Magic, and GunsAndGadgets providers require stamped provenance from those plugins. The alloy scrap provider needs AdvancedCrafting 2.2.0 or newer (`ScrapProvenance`). Goldsmithing matches the live jewelry project for the item. Admin escrow tooling: `/recycler escrow list|return`.

## What not to add yet

- One file per GUI slot
- Hardcoded item ids outside yaml
- Putting the escrow item only in the chest inventory without disk backup
