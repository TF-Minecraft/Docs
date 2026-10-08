# Commands and ammunition handling

[GunsAndGadgets documentation](README.md) · [All projects](../../README.md)

## Staff gun commands

`/gg give <player> <rifle|pistol|shotgun|launcher> <part> [part...]`

Gives one completed, unloaded gun to an online player. Use part IDs from
`parts.yml` and supply exactly one enabled, compatible part for every category in
`required-parts` in `config.yml`. The normal assembly builder applies stats,
skins, and part provenance. Conflicting class requirements and invalid designs
are rejected. The recipient needs an empty inventory slot.

No crafting materials are charged. The item explicitly records an empty set of
consumed crafting inputs, so compatible recycling cannot return unpaid materials.
Load ammunition normally.

`give-permission` in `config.yml` defaults to `gunsandgadgets.give` (operators).
Set it to your staff permission; a blank value disables giving. This permission
is independent of `gunsandgadgets.reload`, which gates `/gg reload` and
`/gg refresh`. Reload configuration with `/gg reload`. Tab completion suggests
recipients, weapon types, and configured part IDs.

`/gg refresh` is player-only and force-refreshes the gun in the main hand. See
[revision and craft provenance](docs/REVISION_SYSTEM.md) for automatic refresh
triggers and the data preserved when stats change.

## Ammunition selection

Crouch and right-click with a gun to cycle through compatible ammunition carried
in the inventory. The next reload uses the selected calibre, and the choice is
saved on that gun. Already loaded ammunition stays loaded. Without a selection,
reloads use the first compatible ammunition carried.

The action bar confirms the selection and carried amount, or reports that no
compatible ammunition is available. Selection is blocked while the gun is
reloading.
