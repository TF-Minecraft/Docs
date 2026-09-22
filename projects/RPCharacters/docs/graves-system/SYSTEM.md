# Graves

RPCharacters owns grave creation, recovery, protection, persistence and visuals.
Thievery reads its public grave API to handle stealing. Current source lives in
[the grave package](https://github.com/TF-Minecraft/RPCharacters/tree/main/src/main/java/net/tfminecraft/rpcharacters/grave).

## Configuration

`plugins/RPCharacters/graves.yml` controls the system. Bundled defaults include:

| Key | Default | Purpose |
| --- | --- | --- |
| `enabled` | `true` | Enable graves |
| `protect-by-default` | `true` | Protect against non-killer theft |
| `snapshot-interval-ticks` | `20` | Last-solid-position tracking |
| `expire-seconds` | `1200` | Expiry; zero disables expiry |
| `material` | `CHEST` | Grave block |
| `hologram-show-killer` | `true` | Include killer information |
| `hologram-radius` | `32` | Viewer range |
| `insurance.item` | `m.miscellanea.grave_insurance` | Remote recovery item |
| `insurance.consume` | `true` | Consume insurance on successful recovery |

Exclusions are independent: `excluded-slots` excludes whole inventory slots;
`excluded-slot-items` excludes matching TLibs items only in specified slots;
`excluded-items` excludes matching items in every slot. The bundled configuration
excludes remodeled vanilla diamond hoes in slots 9–12 and grave insurance in
all slots. It does not exclude every item in slots 9–12.

## Death and storage

Last-solid tracking records a usable location. The death listener checks
keep-inventory and placement conditions before transferring drops and experience
into a grave. Failed placement leaves normal death handling available. Excluded
items are retained for respawn rather than stored in the grave.

The logical inventory has 41 slots: storage 0–35, armor 36–39 and offhand 40.
Graves persist owner/killer identity, location, items, experience and protection.
Gson files live under `plugins/RPCharacters/graves/`. Reload and expiry handling
must preserve or release remaining contents without duplication.

## Recovery, theft and protection

Owners recover through interaction; items that do not fit are dropped and stored
experience is returned. Recovery removes the grave. The insurance item recovers
the owner's newest grave remotely. `/grave unlock` unlocks the newest grave for
other players.

Protected graves allow the killer to steal while other non-owners are blocked.
Thievery takes items subject to its budget and inventory capacity; excess stays
in the grave. RPCharacters does not dump contents for non-owners when Thievery
is absent. Normal chest opening, breaking, hoppers, pistons and explosions are
blocked through grave protection listeners.

`rpchar.grave.protect` and `rpchar.grave.admin` control protection and staff access.
The hologram uses per-viewer ProtocolLib packets, with owner/killer information,
expiry text and a robbery hint for eligible viewers.

## Validation

Build from `main` with matching dependencies and test on Paper 1.21.10:

- Ordinary death, keep-inventory, empty inventories and failed placement.
- Whole-slot, per-slot-item and global item exclusions, including respawn.
- Owner recovery, inventory overflow, insurance and `/grave unlock`.
- Killer and stranger access before and after unlocking; theft with a full inventory.
- Chest opening, hopper, piston, explosion and break protection.
- Restart, chunk unload/reload and expiry with items and experience remaining.
- Hologram visibility, timer updates and cleanup for every viewer.

Record results for the tested commit and configuration.
