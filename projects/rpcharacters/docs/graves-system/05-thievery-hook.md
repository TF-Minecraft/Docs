> Canonical documentation: [TF-Minecraft/docs](https://github.com/TF-Minecraft/docs). [Source snapshot](https://github.com/TF-Minecraft/rpcharacters/blob/9e2d9f0d7ca9e7080f0748a654eab535c2c9c663/docs/graves-system/05-thievery-hook.md). Commands and plain-text code/config paths refer to the source repository unless stated otherwise.

# Batch 5 - Thievery hook

RPC does not import Thievery. Public grave accessors only.

## Thievery changes

- Delete `steal/AngelChestManager.java`, `steal/source/AngelChestStealSource.java`
- Remove AngelChestAPI from `pom.xml` and `depend` in `plugin.yml`
- Add RPCharacters to `depend` if not already a hard depend (already systemPath)
- New `steal/GraveManager` listener name: `GraveStealListener` (avoid clashing with RPC `GraveManager`)
- `steal/source/GraveStealSource.java` - same 41-slot mapping as `PlayerSlotMap`
- `config.yml` key `graves.budget` (not a third-party plugin name)
- `ContainerManager` skip when RPC grave is at the clicked block

## Steal behaviour

No GUI. One greedy pass. Budget + `StealTakeHandler.maxFitInPlayerInventory`. Stop when full. Do not drop leftover stealable items. Clues and ignore rules skipped. Killer bypasses lock; owner never stolen from.

## Done when

Thievery compiles without any death-chest API; killer can steal from a locked grave; non-killer cannot; owner recover still works via RPC.
