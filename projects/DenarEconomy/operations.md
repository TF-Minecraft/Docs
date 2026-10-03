# Commands, permissions, and account storage

[DenarEconomy](README.md) · [All projects](../../README.md)

## Commands

Commands are handled by [CommandManager](https://github.com/TF-Minecraft/DenarEconomy/blob/main/src/main/java/net/tfminecraft/denareconomy/managers/CommandManager.java). Player messages come from `messages.yml`.

| Command | Who | Effect |
|---------|-----|--------|
| `/pouch` | Players | Shows the pouch balance plus withdrawable coins carried in the inventory, with a short cooldown. |
| `/deco bal` | Players | Shows the pouch and bank balances. |
| `/deco pay <amount>` | Players | Takes the amount from the pouch and drops it as coins in the world. |
| `/deco toitem <amount> [coin]` | Players | Converts pouch money into coin items. With a coin id or value, `<amount>` is a whole number of that coin. Items that do not fit are dropped at the player's feet. |
| `/deco topouch` | Players | Puts the withdrawable coin stack in the main hand into the pouch. World payout coins are refused. |
| `/deco deposit <amount>` | Players | Moves money from the pouch to the bank. |
| `/deco withdraw <amount>` | Players | Moves money from the bank to the pouch. |
| `/deco baltop` | Players | Lists the 20 largest combined pouch and bank balances. |
| `/deco reload` | Console, operators or `denareconomy.reload` | Reloads `coins.yml`, `drops.yml` and `messages.yml`. |
| `/deco give <player> <amount> [bank\|pouch]` | Console, operators or `denareconomy.give` | Credits a player's bank (the default) or pouch, online or offline. |

Money amounts must be positive and use at most two decimal places. `deposit` and `withdraw` first fire the cancellable `PlayerBankPulseEvent`, so another plugin can refuse banking at that moment.

### Crediting a player with `/deco give`

`denareconomy.give` and `denareconomy.reload` both default to `op`. The console always passes the check; a player needs operator status or the permission. Tab completion only offers `give` and `reload` to senders who can use them.

`/deco give` resolves the name to an account id in this order:

1. A player with that name who is online now.
2. The server's `usercache.json` and in-memory user cache. Among several matches, an id that already has a DenarEconomy account wins, then a Mojang id over an offline-mode id, then the cache row that expires latest. An offline-mode id with no account is ignored, so money is not written to an account the player will never see.
3. DenarEconomy's own name index, `plugins/DenarEconomy/Data/player-names.json`, which remembers names as players join.

An unknown name gets the default message "No denar account is known for <player>." Online players are credited in their live session and told what they received. Offline players are credited by loading their saved account, changing it and saving it immediately. If that save fails, the balance is restored, the error is logged and the sender sees "Could not pay <player>. Their balance has not changed." Each successful credit is logged with the sender, amount, player name, id and account.

## Account storage

Each account is a JSON file at `plugins/DenarEconomy/PlayerData/<uuid>.json`, relative to the server working directory, holding the pouch and bank balances. Preserve `PlayerData` and `Data` when replacing builds.

Online players' accounts are held in memory while they play. The account is saved when the player quits, and every account still in memory is saved when the plugin disables. Offline balance changes made through `/deco give` or the [OfflineModifier](https://github.com/TF-Minecraft/DenarEconomy/blob/main/src/main/java/net/tfminecraft/denareconomy/accounts/OfflineModifier.java) API are saved at once, and the prior balance is restored if the save fails.

[Database.savePlayerData](https://github.com/TF-Minecraft/DenarEconomy/blob/main/src/main/java/net/tfminecraft/denareconomy/database/Database.java) writes each save as follows:

1. It writes the JSON to a temporary file in `PlayerData` and flushes it to disk.
2. It atomically renames the temporary file over the account file. If the filesystem cannot rename atomically, the save fails and the previous file is left intact. The temporary file is deleted on failure.
3. It syncs the `PlayerData` directory. If that sync fails, the save still counts as committed and a warning is logged that power-loss durability is not guaranteed.

Read and inspection errors are raised rather than treated as a missing account, so a storage fault never creates a fresh zero balance over an existing one.

## Storage failures

When a quit save fails, the account stays in memory and the error is logged. At shutdown, DenarEconomy retries every retained account. If one fails, it logs `Could not save account <uuid>; retained for retry` at `SEVERE` and carries on with the rest.

Retained memory is not durable. If saves keep failing, fix the cause (permissions, free space or filesystem errors on `plugins/DenarEconomy/PlayerData`) while the server is still running. A retained account is written on that player's next successful quit or at the next clean shutdown. If the process exits before then, through a crash, a forced kill or a shutdown whose saves still fail, the unsaved balances are lost.
