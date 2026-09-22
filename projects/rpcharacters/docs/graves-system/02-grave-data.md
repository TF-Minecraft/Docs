> Canonical documentation: [TF-Minecraft/docs](https://github.com/TF-Minecraft/docs). [Source snapshot](https://github.com/TF-Minecraft/rpcharacters/blob/9e2d9f0d7ca9e7080f0748a654eab535c2c9c663/docs/graves-system/02-grave-data.md). Commands and plain-text code/config paths refer to the source repository unless stated otherwise.

# Batch 2 - Grave model, PDC, persist

## Files

- `grave/Grave.java` - owner, killer, protected, created, experience, storage/armor/offhand, hologram UUID, block location
- `grave/GraveManager.java` - `Map` by block key, `getAt`, save/load Gson, PDC keys on chest
- `grave/GraveKeys.java` or namespaced keys on `RPCharacters.plugin`

## PDC

Chest block (or tile entity) tagged so lookup works after restart before Gson matches.

## Done when

Save/load round-trip of items + killer UUID + excluded slots stored as empty.
