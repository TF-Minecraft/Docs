# /tfmc player commands

TFMCCore registers `/tfmc` as a Paper Brigadier command. Each subcommand declares its permission, and the client receives the same filtered tree, so players are only offered commands they can run.

Before this, `/tfmc` was served by AACommandsFiller (suggestions only) with ConditionalEvents triggers doing the work.

## Subcommands

| Subcommand | Who | Effect |
|---|---|---|
| `tips enable\|disable` | everyone | Toggles `tips.off` (LuckPerms, this server's context) |
| `pack` | everyone | Sends the resource pack |
| `pack auto\|manual` | everyone | Toggles `tfmcresourcepack.enable`, which the join event uses to send the pack on login |
| `booster` | `group.legacy`, `group.ascended` | Starts MMOCore profession boosters and thanks the player server-wide; 3-day cooldown |
| `drinks` | `group.noble`, `group.gilded`, `group.ascended`, `group.legacy` | Opens DrinkBuilder |
| `patreon`, `map` | everyone | Links; `map` has a 10 s cooldown |
| `date` | everyone | Roleplay weekday and month |
| `statues` | everyone | Armor Statues book |
| `patterns` | everyone | The ten banner patterns; 10 s cooldown |
| `masks` | everyone | A random mask; 10 s cooldown |
| `poster <name>` | everyone | Places a configured image poster |
| `ban <player> [reason]` | `tfmc.helper` | Essentials `tempban` for 8 hours |
| `promote\|demote` | the step's permission on the player's highest track | One step along that LuckPerms track (see below) |

### Promote and demote

`helper-tracks` in `tfmc.yml` lists the LuckPerms tracks lowest first (`helper`, `helper+`, `staff`) with a promote and a demote permission for each. A player's highest track is the last one whose promote or demote permission they hold, and `promote` and `demote` always act on it. Each is offered only when the player holds that step's permission on that track. On every track, the `_player` group grants the promote permission and the `_inactive` group grants the demote permission. The active group inherits both.

### Disabled by default

These sections ship with `enabled: false` in `tfmc.yml` and stay out of the command tree until enabled. TFMCDev01 enables them; Main does not have the content yet.

| Subcommand | Who | Effect |
|---|---|---|
| `tutorial <name> clear` | everyone | Takes back the items a tutorial lantern handed out (`tutorials.list`); 10 s cooldown per tutorial |
| `parrot` | `group.ascended` (Ascended and Legacy; `parrot.permissions`) | Parrot disguise and 20 s of slow flight; 5 min cooldown. Flight settings are restored on expiry, `unparrot`, logout or plugin disable |
| `unparrot` | everyone | Ends a parrot flight early |
| `worldboss info` | everyone | World-boss explainer |

## Configuration

`plugins/TFMCCore/tfmc.yml` holds the messages (MiniMessage), console commands, item and mask lists, calendar names, donor tiers and posters. Reload it with `/tcore reload tfmc`.

The booster cooldown is stored in `plugins/TFMCCore/tfmc-cooldowns.yml`. On the first start without that file, TFMCCore imports last-use times from `plugins/ConditionalEvents/players/*.yml` (`events.global_booster.cooldown`).

## Adding a subcommand

Add the node in `TfmcCommand.build()` with a `requires(...)` permission if it is restricted, put its content in `tfmc.yml`, and cover it in `TfmcCommandTest`. Do not add a ConditionalEvents trigger for `/tfmc`: ConditionalEvents sees every typed command, so a trigger would run alongside, or cancel, the native command.
