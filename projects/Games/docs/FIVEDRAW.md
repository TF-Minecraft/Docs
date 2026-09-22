# Five-Draw

Five-card draw uses a player-funded pot, with two betting streets and one draw round.

Games **owns rules**. Engines stay dumb: ranking stays in the game package (`HoldemRank` is 5-card compare, not Hold'em-only). No second display stack. Rules live in [DrawGame.java](https://github.com/TF-Minecraft/Games/blob/main/src/main/java/net/tfminecraft/games/game/DrawGame.java). Keep draw separate from [PokerGame.java](https://github.com/TF-Minecraft/Games/blob/main/src/main/java/net/tfminecraft/games/game/PokerGame.java) or `freeplay`.

Player pot, not house. Guild auto-dealer / staff mint / tray stay blackjack.

Saved `gameId` is **`draw`**. Hold'em stays **`poker`**. Player-facing names are `label` / GUI copy, not the yaml key.

## Rules

- Five-card draw. No board, no flop/turn/river, no discards after the draw round.
- 2+ seated (`actives`) to start. Idle shoe click by a seated player deals.
- Button is `table.dealerId()`. First chip-in is the button. Leave/logout passes in seat order. After a **finished** dealt hand (fold-win or showdown), rotate. Session stop does **not** rotate.
- No ante. No jacks-or-better to open. No blinds (no hologram blinds line, no options blinds).
- Betting: chat **check**, **call**, **fold**, **raise** (same engine path as Hold'em). Raise = this-street chips already above the call, then the word. Short **call** is in for that amount (`capped` this street). Side pots at showdown from total invested, same layers as Hold'em.
- Hand: exactly the five cards you hold. Rank with `HoldemRank` (ace-high, wheel). Fold-win skips ranking.
- Draw round: once around, left of button, skip folded. Actor may discard **selected** cards (existing F / selected return), then is dealt that many. **Stand pat** (keep all): type **draw** with nothing selected. Then next live seat. After everyone has drawn, second betting street, then showdown.
- Burn cards are not supported.

## Config

`games.yml` key `draw`:

- `label: Five-Draw`
- `icon: ia.tfmc_games:seithr_5`
- `card-set: french_52`
- Felt ring like poker. No `blinds` section.

Hold'em `poker.label` is **Tenceur Hold'em** (lore). Id stays `poker`.

GUI: `place.gui_draw`. Place command / tab: `draw`. Select GUI gets a fourth slot.

## Place and seats

`games.yml` `draw`, `GamesRegistry`, select icon, `/games place draw`. `DrawGame`: seats, button, idle sandbox shoe, `minActives` 0. A seated shoe click starts the deal with at least two players. No blinds.

## Deal five

Seated shoe click with 2+ seats: `beginSession`, five cards each (left of button first, one around until 5). `ROUND` reshuffle at start. Live: no sandbox draw; F still works. Session stop mucks, no button rotate. Leave to fewer than 2 seated ends the session.

## First betting street

After the deal: actor left of button. Chat check/call/fold/raise. Fold-win: `endSession`, `passButton`. All matched: draw phase (no showdown yet). Short call caps this street.

## Draw

Phase `draw`. Only the actor. Selected return discards, then `dealToPlayer` that many. Word **draw** (thin engine `playWord`) stands pat or finishes after discards. Next live seat. When all live have drawn: street 2, `currentBet` 0, capped cleared, actor left of button.

## Second street and showdown

Use the same rules as the first betting street. When matched: `publishHand`, rank 5-card hands, side-pot layers (copy Hold'em pot math in `DrawGame`), `endSession`, `passButton`. Empty pot still ends and passes the button.

## Later

Shuffle options GUI (Shoe/Round, no blinds). Jacks-or-better / ante: out unless this file says so.

## Validation

1. Place Five-Draw: hologram Five-Draw, seithr 5 icon in select. Hold'em still Tenceur Hold'em / `poker`.
2. Two seated, click shoe: five each, shoe locked.
3. Check around: draw turn. Stand pat with `draw`. Discard two with F, get two, then next player.
4. Fold: other wins, button moves. Short call then raise: side pot at showdown.
