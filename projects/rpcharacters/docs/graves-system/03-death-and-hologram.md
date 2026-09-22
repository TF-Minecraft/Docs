> Canonical documentation: [TF-Minecraft/docs](https://github.com/TF-Minecraft/docs). [Source snapshot](https://github.com/TF-Minecraft/rpcharacters/blob/9e2d9f0d7ca9e7080f0748a654eab535c2c9c663/docs/graves-system/03-death-and-hologram.md). Commands and plain-text code/config paths refer to the source repository unless stated otherwise.

# Batch 3 - Death spawn and hologram

## Files

- `grave/GraveDeathListener.java` - `PlayerDeathEvent` **HIGHEST**
- `grave/GraveVisualManager.java` - per-viewer fake `TextDisplay` packets via ProtocolLib (not a shared world entity)
- `grave/GraveHologramTexts.java` - victim name, optional killer line, rob hint when `GraveLootRules.canSteal`

## Copy rules

Copy from `PlayerInventory` by slot. Skip `excluded-slots`. Stash those stacks and restore them on respawn. Then clear `event.getDrops()` and zero dropped XP after storing XP.

## Names

`DisplayIdentityService.resolveCharacterName` for victim and player killer. Not mask, not `%rpcharacters_display%`.

## Done when

Dying in lava/void places a chest on last solid ground with per-viewer hologram text; excluded slots are not in the chest; other drops do not appear on the ground.
