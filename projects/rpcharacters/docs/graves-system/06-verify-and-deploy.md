> Canonical documentation: [TF-Minecraft/docs](https://github.com/TF-Minecraft/docs). [Source snapshot](https://github.com/TF-Minecraft/rpcharacters/blob/9e2d9f0d7ca9e7080f0748a654eab535c2c9c663/docs/graves-system/06-verify-and-deploy.md). Commands and plain-text code/config paths refer to the source repository unless stated otherwise.

# Batch 6 - Verify and deploy

## Tests

1. Walk land, jump in void: grave on last land, not in void.
2. Die with items in slots 9-12: those items are **not** in the grave. After respawn they are back in those slots.
3. Owner click: items in inv, overflow on ground, hologram gone.
4. Second player, locked, not killer: locked, items remain.
5. Killer click: stealable items taken up to budget/space; rest remain; no GUI.
6. Hopper under grave: no drain.
7. Restart server: grave **chest** persists; hologram text is re-sent by `GraveVisualManager` tick (not a saved world entity).
8. Knockout PvP (non-lethal): no grave.
9. Two players at one grave: both see victim name (+ killer line if configured).
10. Killer with loot-graves trait sees **Right click to rob**; other player does not.
11. Owner and bystanders never see the rob hint.
12. Grave despawn / owner recover: fake holograms removed for all viewers; no orphaned world `TextDisplay` entities after reload (legacy cleanup).

## Deploy

- Unload other death-chest plugins from the server `plugins` folder.
- Deploy RPCharacters then Thievery.
- Confirm `graves.yml` `excluded-slots` matches the live reserved UI (default 9-12).
