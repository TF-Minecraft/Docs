> Canonical documentation: [TF-Minecraft/docs](https://github.com/TF-Minecraft/docs). [Source snapshot](https://github.com/TF-Minecraft/rpcharacters/blob/9e2d9f0d7ca9e7080f0748a654eab535c2c9c663/docs/graves-system/04-interact.md). Commands and plain-text code/config paths refer to the source repository unless stated otherwise.

# Batch 4 - Interact, protect, world protection

## Owner

Right-click: no inventory GUI. `addItem` all stacks. Leftovers drop at grave. Give XP. Remove chest + hologram + file.

## Insurance item

Right-click the configured TLibs insurance item (see `graves.yml` `insurance.item`) to recover the **newest** grave owned by that player from anywhere. Same give-all + XP + despawn as chest recover. Overflow drops at the player. Consumes one charge only when loot or XP was transferred; empty graves despawn without consuming. The item path must stay in `excluded-items` so it survives death. No fetch/list/teleport commands.

## Non-owner

Cancel vanilla open. If locked and not killer: locked message. Else do not give items (Thievery batch 5).

## Protect

Hoppers, break, explode, pistons: cancel for tagged graves.

## Done when

Owner click recovers without a chest screen; overflow drops; hoppers cannot drain the grave.
