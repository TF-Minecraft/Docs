# Guild tables and house bank

Guild-house tables connect blackjack operation to guild permissions, auto-dealer limits and the faction bank.

Bank money reaches the felt only through `BankAccount`, as a leg of a wager transaction. See [WAGER_ENGINE.md](WAGER_ENGINE.md).

Games requires DenarEconomy and **softdepends SimpleFactions** for guild identity, modifiers and profit bookkeeping. SimpleFactions **does not** import Games, persist table ids, or listen to table events. **No Bukkit events** for create, dealer, or bank.

## Modes

| Mode | Auto play | Tray money | Expansion slot |
|------|-----------|------------|----------------|
| Private dealer, no guild | No | Dealer stocks the tray by hand and gets the float back | No |
| Guild, human dealer | No | Withdraw the round reserve from the **owning guild bank** | No |
| Guild auto | Yes | Withdraw the round reserve from the **owning guild bank**, then spawn chips on the tray | Yes |
| Staff auto | Yes | **Mint** shortfall (current behavior) | No |

Who turns the cards and who funds the house are separate questions. `GuildTables.houseBacked` answers the money one: a staff mint or a guild bank behind the table. A guild table is bank funded either way, because a non-member cannot take the shoe, so the tray is the guild's float and its winnings are the guild's. Only a table with no guild at all is stocked by its dealer, and on a backed table hand-stocking the tray is refused outright with `wager.tray_is_funded`.

Staff auto needs `games.autodealer.staff`. It is not the default for a normal place.

`games.yml` `blackjack.auto-dealer` is only the **options-GUI default when the placer has staff perm**. Player tables default auto **off**. Min/max/bet-seconds in yaml stay the starting values for the GUI.

## Ownership

On place, store:

- `ownerPlayer` (placer UUID)
- `ownerGuildId` (guild id at place time, or null for a personal table)
- `ownerGuildIncarnation` (the owning guild's permanent UUID)

Guild membership and leadership use the active character. Editing or picking up a guild table requires that character to lead the captured guild incarnation, or staff permission. The placer account alone gives no guild-table rights. The account remains the host of a personal table.

The captured incarnation selects the `guild:<uuid>` Denars account. A deleted guild's later namesake cannot use its tables, bank or expansion slots. Missing guilds, unavailable faction services and unresolved incarnations refuse funding; tray settlement retains the table and chips for review instead of dropping money through a failure fallback.

Existing guild tables wait for `SimpleFactionsApi.ready()`. Migration preserves each original JSON file in `migrations/guild-tables/backup/` and writes a complete migration plan before applying it. Each table resolves its guild id once. Restart reuses that plan; an unresolved guild remains unresolved even if a namesake appears later. Deferred loads retry every five seconds without reloading already active tables.

## Cap

SF `GuildModifier.AUTO_DEALER_TABLES` from an **expansion upgrade** (not a branch). `allowed-types`: `guild` and `realm`. Stacks with upgrade level via existing `Guild.getModifier`.

A non-staff guild table counts against the cap when its guild id and captured incarnation match the current guild.

Refuse (do not place, or do not turn auto on) when `count >= cap`. Cap `0` means guild auto is off. Missing SF: guild auto off; staff mint still works.

If upgrades drop so `count > cap`, **do not** pick up tables or cancel a live round. Every counted table of that guild **cannot start a new round** until `count <= cap` (turn auto off or pick up extras). A bet window that was already open refunds and does not deal.

Human takeover changes who deals; guild ownership and its slot remain.

## House float (any backed table)

No "please top up" wait. Cover is withdraw-or-refuse.

1. During the bet window, after a legal chip-in, `need = max(0, action - tray)`. Only auto tables run a bet window, so on a human-dealt table the round reserve at step 5 is the only cover step.
2. If `need == 0`, do nothing.
3. Staff auto: spawn `need` (today).
4. Guild auto: if bank wealth `< need` or bankrupt / no bank, **do not accept that chip-in** (restore item, message). Else post the guild debit through Denars, then materialize the planned chips on the tray.
5. When bets close, blackjack reserves the round's worst case: `sum(boxStake) * max-hands-per-box * 2`, rounded up to a whole coin. Withdraw-or-refuse again, but at round scope: if the bank cannot supply it the round does not start and every box is refunded. Splits and doubles inside the round then take their cover from the reserve and never touch the bank. `closeBets` is the gate for both modes: the bet timer calls it on auto tables, and a human dealer reaches it with `/games bet close`, which is also the only way their round starts.
6. Player wins peel the tray. The settle shortfall path still exists but the reserve should make it unreachable, so it logs a mismatch when `wager.audit-log` is on.
7. Round end (settled or abandoned): the whole tray `deposit`s back to the owning guild bank, so the float is zero between rounds and house wins are banked each round rather than piling up as chips. Staff mint burns it. A table with no guild returns the float to its dealer instead.
8. Pickup / teardown: any remaining tray on a backed table `deposit`s to the owning guild bank; if the guild or posting is unavailable, retain the table and tray for review. Staff mint tray is despawned, not dropped. Player pots still drop.

A guild running several tables shares one bank, so reserving per round is also what stops two tables from both counting the same denars.

## Tax on winnings

A guild owes tax on what its tables win, not on the float they were stocked with. Each table counts the denars it has taken out of the bank and not yet paid back, and money returning to the bank clears that count before any of it is called profit. Only the excess is declared, as the `GAMBLING` cashflow on the owning guild's ledger, which is folded into the guild's gross taxable income.

Tables settle separately, so a table that is up declares its winnings even if another table under the same guild is down. A table that is down carries its shortfall forward and pays nothing until it is level again. The guild that owns the table declares it, so a branch guild's takings show on the branch and reach the capital through the ordinary tax on guilds.

Staff mint tables and private tables with a human dealer owe nothing: neither is backed by a guild bank, so neither has winnings to declare. See [WAGER_ENGINE.md](WAGER_ENGINE.md) for how the count is kept.

## Dealer

Not during a live round.

Right-click shoe (existing claim path):

- Already this player: **unset** dealer.
- Empty seat, human table: **set** if the player is in `ownerGuildId` (or staff). No guild on the table: placer / staff only.
- Guild auto, between rounds: **takeover** - become human dealer, `autoDealer=false`, tray and guild ownership stay.
- Staff auto: guild members **cannot** takeover. Staff can turn mint off from options (when not live) or pick up the table.

Leave-distance still does not clear dealer. Logout / pickup still does (existing).

## Options GUI

After game-select **blackjack** (not free play / poker): second inventory.

- Auto on/off
- Staff mint on/off (hidden without perm)
- Bet min / max (anvil or click steps; stay within yaml bounds unless staff)
- Max boxes (num players)
- Shuffle: **each round** vs **shoe** (recycle when empty; allows counting)

Confirm places the table. Changing options later: sneak-click shoe while not live, same GUI, re-check cap if turning auto on.

## Shuffle

| Policy | Behavior |
|--------|----------|
| `ROUND` | Full shuffle into the shoe at each round start (after muck / before deal) |
| `SHOE` | Keep the current recycle-when-empty shoe |

Default `SHOE`. Engine stays dumb; blackjack asks the table for policy.

## Isolation

Guild access checks plugin presence, enabled state and `SimpleFactionsApi.ready()` before character membership and incarnation lookups. Errors fail closed. Denars owns money posting; SimpleFactions only reads identity/modifiers and records idempotent casino profit. New rounds wait for `Denars.taxReady()`.

SimpleFactions integration: `GuildModifier` entry + `upgrades.yml` row. No Games dependency in SF `pom` / `plugin.yml`.
