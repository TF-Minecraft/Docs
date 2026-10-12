# Commands and permissions

[DenarEconomy](README.md) · [All projects](../../README.md)

## Commands

Commands are handled by [CommandManager](https://github.com/TF-Minecraft/DenarEconomy/blob/main/src/main/java/net/tfminecraft/denareconomy/managers/CommandManager.java). Player messages come from `messages.yml`.

Every money command acts on the character the player is playing now. A player with no current character is told "You carry no purse until you take up a character." and nothing changes. If the [ledger](ledger.md) is closed after a database error, money commands answer "The bankers' ledger is closed. Nothing has changed."

| Command | Who | Effect |
|---------|-----|--------|
| `/pouch` | Players | Shows the character's pouch balance plus withdrawable coins carried in the inventory, with a short cooldown. |
| `/deco bal` | Players | Shows the character's pouch and bank balances. |
| `/deco pay <amount>` | Players | Takes the amount from the pouch and drops it as coins in the world. |
| `/deco toitem <amount> [coin]` | Players | Converts pouch money into coin items. With a coin id or value, `<amount>` is a whole number of that coin. Items that do not fit are dropped at the player's feet. |
| `/deco topouch` | Players | Puts the withdrawable coin stack in the main hand into the pouch and saves the player at once, so a crash cannot return the coins. World payout coins are refused. |
| `/deco deposit <amount>` | Players | Moves money from the pouch to the bank. |
| `/deco withdraw <amount>` | Players | Moves money from the bank to the pouch. |
| `/deco baltop` | Players | Lists the 20 characters with the largest combined pouch and bank. |
| `/deco history` | Players | Lists the character's last 20 postings, newest first, with the change to its pouch and bank. |
| `/deco history <player>` | Console, operators or `denareconomy.admin` | The same for another online player's current character. |
| `/deco reload` | Console, operators or `denareconomy.reload` | Reloads `coins.yml`, `drops.yml` and `messages.yml`. |
| `/deco give <player> <amount> [bank\|pouch]` | Console, operators or `denareconomy.give` | Credits the bank (the default) or pouch of the character an online player is playing. |
| `/deco legacy` | Console, operators or `denareconomy.admin` | Lists pre-ledger money that has not reached a character yet. |
| `/deco legacy assign <account> <character>` | Console, operators or `denareconomy.admin` | Moves an account's legacy money to one of that account's characters. |

Money amounts must be positive and use at most two decimal places. `deposit` and `withdraw` first fire the cancellable `PlayerBankPulseEvent`, so another plugin can refuse banking at that moment. Coins that leave the pouch as items (`pay`, `toitem`) go to the mint account, and coins that come back (`topouch`, pickups) come from it.

Tab completion only offers `give`, `reload` and `legacy` to senders who can use them.

## Crediting a player with `/deco give`

The console always passes the permission check; a player needs operator status or `denareconomy.give`. The target must be online and playing a character; otherwise the sender sees "<player> is not online playing a character." The credit is a ledger posting from the mint with reason `staff:give`, so a dead character can still be credited. If the posting does not apply, the sender sees "Could not pay <player>. Their balance has not changed." Each successful credit is logged with the sender, amount, player name, character ID and account.

## Assigning legacy money

`/deco legacy` lists every account whose pre-ledger money is still waiting, with the account UUID, last known name, and pouch and bank amounts. Most accounts move to their reviewed heir automatically (see [the legacy claim](ledger.md#legacy-money)); the list shows those that have no heir yet.

`/deco legacy assign <account uuid> <character uuid>` moves both amounts to the chosen character's pouch and bank. The character must belong to that account. The move is the account's one claim operation, `claim:<account>`, so it cannot run twice: an account with nothing left answers "has no unclaimed legacy money". Each assignment is logged with the sender, account and character.

## Coins in the world

A picked-up coin is credited as operation `coin:<item entity UUID>`. The coin is removed only after that posting applies, so a coin that reappears after a crash cannot pay twice, and a player without a character leaves coins where they are. Coins a character drops are marked with that character; picking them up again is untaxed, while any other character, including another character of the same player, pays tax on them. Coins dropped before the ledger release carry the account instead of a character and are taxed when picked up.

A PvP death drops the victim character's pouch as coins unless keep-inventory or the `simplefactions.keep-pouch` metadata applies. If the character is already dead when the pouch would drop, its pouch is frozen and nothing drops.
