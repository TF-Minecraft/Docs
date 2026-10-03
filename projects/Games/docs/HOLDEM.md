# Hold'em

Texas Hold'em is displayed as **Tenceur Hold'em** and saved with `gameId: poker`. See [Five-Draw](FIVEDRAW.md) for the separate `draw` game.

Games **owns rules**. Engines stay dumb: no Hold'em ranking on `Card`, no second display stack, no blackjack box/tray copy. Rules live in [PokerGame.java](https://github.com/TF-Minecraft/Games/blob/main/src/main/java/net/tfminecraft/games/game/PokerGame.java). Call `dealToPlayer`, `dealToTable`, `muck*`, `flushPiles`, session APIs.

Hold'em is a **player pot**, not a house game. Guild auto-dealer, staff mint, and tray float stay blackjack.

## Rules

- No-limit Hold'em. Stacks are chips on the felt.
- 2+ players to start a hand (seated in `actives`). At a cash table, an idle shoe click by a seated player or the host deals. At a [tournament](#tournaments) table only the host or staff deal.
- Button is `table.dealerId()`. First player to chip in is the button. When they leave or log out, the button passes to the next seated player in seat order (`actives` insertion order). After a finished dealt hand (fold-win), rotate around that circle.
- Blinds default from `games.yml` `poker.blinds.small` / `big`. Each table can change them in options. They are shown on the hologram and posted at the start of each hand: heads-up, the button posts the small blind; otherwise the seat after the button does, and the next seat posts the big blind. Preflop action starts after the big blind. A player who cannot cover a blind goes all in for what they have.
- No straddles, bomb pots, or other variants.
- Optional burn cards: later.
- Side pots: a short call is in for that amount; extra chips from others make a side pot at showdown.

## Seats and button

Seats, the dealer button and configured blinds appear on the hologram. The shoe supports sandbox draws while idle; a seated player starts a hand with at least two seats occupied.

## Dealing

Seated player clicks the shoe with 2+ seats: `beginSession`, two hole cards each (left of button first, one around then another). Live: no sandbox draw or selected return. F still works. `/games session stop` mucks holes and does not rotate the button. Walking off to one player ends the session.

## Test

One seated: shoe still draws. Two seated, seated click: holes deal, shoe locked. Unseated click still draws. Session stop mucks. One of two leaves: session ends.

## Betting

Preflop chat: **check**, **call**, **fold**, **raise** and **allin** (`all in` also works), or `/games bet <word>` (same path as blackjack hit/stand). Raise is chips already on this street above the call, then the word; check or call with chips above the bet counts as a raise. At a cash table, stakes go on the felt only on the current player's turn. **All in** stakes the player's entire remaining coins (or tournament stack). No `/wager` commit for Hold'em. Last player standing wins without ranking: session ends, button moves.

## Community cards

When a street matches, deal the next board automatically (flop 3, then turn 1, then river 1), all face-up on `board`. New street number so only this-street chips count. Same chat betting; folded stays folded. No burns.

## Showdown

When river betting matches, remaining holes are shown, best 5-card Hold'em hand wins (ace-high, wheel straight). Even split among tied winners of a pot; leftover denars go left of the button among those winners. Then session end and button move. Fold-win still skips ranking.

## Short calls and side pots

**Call** with fewer chips than the bet is allowed: they are in for that amount and skip the rest of the street. **Raise** still needs more than the bet. At showdown, pots are layers by total invested (all streets). Folded chips stay in the pots they paid into. No extra chat word.

## Table options

Place and sneak-edit: small/big blinds and Shoe vs Round shuffle. Defaults from `games.yml`. `ROUND` reshuffles at hand start. Tournament blinds also start from these values.

## Test

Place poker 5/10 Round: hologram blinds + Round. Edit 0/0: no blinds line. Old JSON without fields: yaml blinds. Non-owner sneak still flushes. Blackjack options unchanged.

## Tournaments

Tournament settings live on the table with its other house settings; the rules are in [PokerTournament.java](https://github.com/TF-Minecraft/Games/blob/main/src/main/java/net/tfminecraft/games/game/PokerTournament.java) and the commands in [PokerCommands.java](https://github.com/TF-Minecraft/Games/blob/main/src/main/java/net/tfminecraft/games/command/PokerCommands.java). `/games poker` commands need `games.bet` and act on the nearby `poker` table. The table host is the player who placed the deck; "host" below also covers staff with `games.admin` or `games.autodealer.staff`. The host stays the same as the button rotates.

| Command | Who | Behaviour |
|---------|-----|-----------|
| `/games poker [status]` | Anyone | Show buy-in, starting chips, rebuys, ante and blind interval. |
| `/games poker configure <buy-in Denars> <starting chips> <max rebuys> <ante chips> <blind minutes>` | Host | Only at an idle table with no money on it and nobody bought in. Buy-in `0` selects cash play. Limits: buy-in 0 to 1,000,000; starting chips 1 to 1,000,000; rebuys 0 to 100; blind interval 0 to 10,080 minutes. Starting blinds come from the table options menu. |
| `/games poker buyin` | Player | Pay the buy-in before the first hand and receive the starting stack. |
| `/games poker rebuy` | Busted player | Between hands, within the configured rebuy limit. |
| `/games poker start` | Host | Deal the next hand, also done by right-clicking the shoe. The host does not need to buy in. Needs two players with chips. |
| `/games poker bet <chips>` | Current actor | Put extra chips into the pot, then say `raise` or `check`. |
| `/games poker kick <player>` | Host | Between hands. Removes a registered player who is online. |
| `/games poker finish` | Host | Between hands, once only one positive stack remains: pays that player the Denar prize pool. |

Play:

- Chips are counters on the table. They never enter player inventories or Denar payouts; the buy-ins are held in the table ledger as the prize.
- Each hand collects the ante from every seat as dead money, then posts the blinds. With a blind interval above `0`, blinds double every interval after the first hand, and each new level is collected from the next hand dealt; `0` keeps them fixed.
- `call` takes the chips needed to match automatically; a short stack goes all in. Players with no chips sit out until they rebuy.
- Leaving or being kicked before the first hand refunds the buy-in. After play starts it forfeits the entry.
- When Games is disabled (server stop or plugin reload), tables reset to idle: tournaments end, Denar stakes still on the table return to their owners through the table's refund path (dropped at the table for offline owners), and chip stacks are cleared. Tournament settings persist.
