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

## Character sessions and reload cleanup

The build pins TLibs 2.3.0. With an older TLibs that lacks the character API,
GunsAndGadgets logs an update message and disables itself at startup.
RPCharacters is neither a build dependency nor a `softdepend`: GunsAndGadgets
listens for the shared `CharacterSessionEndEvent`, which RPCharacters 2.16.0
fires when installed. Without a character provider guns work normally; with one,
gun use waits until the character has a ready session.

A reload reserves the exact ammunition stacks it consumes and captures the current
session. Its timer checks that session before progressing; a stale session or a
provider appearing during account fallback cancels it. Switching character,
permanent death, quit and provider shutdown cancel the reload while the outgoing
inventory is still loaded, before it is saved or replaced. Cancellation restores
the reserved items, drops only overflow and clears the reload marker. Duplicate
end/quit notifications and late reload timers cannot refund twice or cancel a
newer reload. GunsAndGadgets also refunds active reloads on its own disable,
covering either plugin shutdown order. Its quit listener remains available when
there is no identity provider.

The deferred held-slot validation captures the current session. It stops if that
session ends, even when the player switches away and back to the same character.
It also stops on disconnect, pending character readiness, or a provider appearing
between scheduling and completion.

To check on a server, start a reload and end the session by switching, permanent
death, quitting and shutdown. Each time the ammunition must return to the outgoing
character's inventory and the next character must not finish the old reload.
Repeat without RPCharacters to check quit cleanup. See the
[shared identity API](../TLibs/character-identity.md) and
[RPCharacters provider](../RPCharacters/docs/character-identity.md).
