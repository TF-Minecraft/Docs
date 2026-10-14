# Wager engine

Every denar that moves on a table moves through `net.tfminecraft.games.wager`. Games describe what they want and commit once; they never touch a player's inventory, the ledger, or a guild bank themselves.

## Accounts

A `MoneyAccount` is a place money can sit. All of them answer the same questions: what have you got, can you produce exactly this much without moving it yet, and will you take this.

| Account | Holds | Notes |
|---|---|---|
| `PlayerAccount` | Coins in an inventory | Filtered, so a blackjack box only takes real money coins. Falls back to dropping at the table when the player is gone, so a payout is never deleted |
| `BucketAccount` | One owner's stakes in the `TableLedger` | The tray is the bucket keyed by the table's own id |
| `BankAccount` | Captured guild incarnation account | Reads Denars balance; mutations are legs of the transaction posting |
| `MintAccount` | Nothing, creates money | Refuses on anything but a staff-mint table |
| `TaxSink` | Withheld chips | Credits their actual whole-chip value to the captured tax account in the same posting |

Build them through `Accounts`: `bucket`, `tray`, `pockets`, `coins`, `declared`, `payee`, `ground`, `bank`, `mint`, and `house`, which picks mint or bank depending on the table.

## A transaction

```java
MoneyTx tx = WagerEngine.get().begin(table, "double down");
tx.move(Accounts.coins(table, player), Accounts.bucket(table, owner).at(spot), bet);
TxResult result = tx.commit();
if (!result.ok()) {
    player.sendMessage(Messages.get(result.messageKey()));
    return;
}
```

Legs come in four shapes:

- `move` - exactly this much or the whole transaction refuses.
- `moveUpTo` - as much as the source can hand over exactly, never more than asked, never a failure for being short.
- `moveAll` and `moveStreet` - everything a bucket holds, or everything it holds from one betting street.
- `spread` - one amount covered by several sources in turn, which is how a pot pays out of the buckets that built it.

`commit()` plans sources on detached copies, reserving each take before planning the next. Reuse one source handle for multiple legs; distinct handles naming the same source are refused. Destinations confirm acceptance before anything moves.

For guild-bank or tax legs, the transaction writes a flushed, atomic intent under `Data/wager-intents/<table-id>.json` before one balanced `Denars.post`. The `games:<table-id>:<uuid>` operation records its legs, item templates, destinations, captured tax quote and expected float/profit. Physical chips exchanged with a guild bank use the Denars mint account as the other ledger leg. Bank-funded tax directly debits the guild and credits the tax destination; it never mints the gross win into a character pouch.

Only `APPLIED` authorizes the planned item and float changes. The engine rechecks physical inventory and character snapshots, applies the changes, saves the table durably, then records casino profit with the same operation ID. The journal is removed only after all steps succeed. A repeated successful `commit()` returns the previous result without delivering again. An unchanged prepared intent can retry in the same process using its original operation ID.

A known tax-readiness wait creates no payment intent. Refused postings leave items, float and profit untouched. A failure after posting may already have moved value; the retained journal freezes the table for staff review. Callers must not compensate or repeat delivery based solely on a failed result. See the recovery procedure below.

`TxResult.reason()` names why a refusal happened - `PLAYER_SHORT`, `NO_CHANGE`, `FELT_SHORT`, `BANK_SHORT`, `NO_TEMPLATE`, `MINT_REFUSED`, `NO_TABLE` - and `messageKey()` maps it to `messages.yml`, so the player is told the real problem rather than a guess.

## Chips are only ever a picture

`PayoutFlight` animations are drawn from what a committed transaction moved and carry no value. Chip piles are a projection of the ledger, refreshed once per commit through `WagerHost`, which `TableManager` implements. Set `wager.show-chips: false` and the tables still work, with amount labels instead of piles.

A `Stake` carries the spot it was put down on, so a player's chips sit where they clicked rather than on a spiral off one anchor per box. A spot is part of a stake's identity: coins landing within `wager.merge-range` of a stack of the same kind grow it, and coins landing anywhere else start a new heap. Only deliberate placement takes a spot, via `BucketAccount.placedAt`. Money the house puts down uses `at` instead and has no spot, which is what leaves the auto dealer's tray on its own layout grid.

## Profit, and what a guild owes tax on

`BankAccount` is the only door between a guild bank and a table, so it is also where profit is worked out. Money going out raises the table's `houseFloat`; money coming in settles that float first, and only what is left over is profit. A guild pays tax on the profit, never on a float it took out and handed straight back.

Casino-profit bookkeeping moves no extra money. Winnings enter the guild account in the transaction posting. After saving the resulting table, `GuildBank.declareProfit` reports only the surplus into the owning guild's SimpleFactions ledger as its `GAMBLING` cashflow, using `addCasinoProfitEntry(operationId, amount)`. Exact retries do not count profit twice, even after a tax settlement. That entry is gross counted, so it widens guild tax, overlord tax, tribute and reparations, and it settles as a ledger line with no delta of its own. Adding a delta would pay the guild for the same denars twice.

A six-box table at 1000 reserves 48000. If players net lose 1500 the tray banks 49500, the float is cleared and 1500 is declared. If players net win 2000 only 46000 comes back, the float stays 2000, nothing is declared, and the table's next 2000 of winnings is sheltered until it is level again. So a losing streak carries forward by itself, and a bank covering a winner directly leaves the float raised for the same reason: the house is down until it earns that back.

`houseFloat` lives on `Table` and is saved with it, with a checked durable save before its money intent can complete. It is zeroed if a table changes owning guild, since a float belongs to whoever put it up. Staff mint tables never reach `BankAccount` at all, so they declare nothing, and a private table with a human dealer returns its float to the dealer rather than a bank and is likewise untaxed.

## Player coin profit this round

`RoundMoney` on each `Table` tracks coin `moneyIn` and `moneyOut` per player for the current session. `MoneyTx` updates it on every successful leg: pockets to the felt raise `moneyIn`, any payout to a `PlayerAccount` raises `moneyOut` (tray, bank, pot, or a dealer covering from pockets). Loot stakes are ignored via `ChipItems.moneyValue`. `moneyProfit` is `max(0, moneyOut - moneyIn)`. Maps are cleared at settled session end and are not saved as a resumable game. Unpaid outcomes and interrupted postings retain separate durable records and prevent automatic reset.

Blackjack settle calls `WagerEngine.payWin`, which quotes citizen tax on the `pay` map profit for the captured wager character, and sends DenarEconomy's `money.tax` line.

Hold'em and Five-Draw pot payouts include the winner's own stake. `RoundMoney.taxableProfit(owner, payout)` subtracts stake still returning (`moneyIn - moneyOut`) before tax applies. `WagerEngine.payFromPot` and `sweepPot` spread net coins to the payee and tax to `TaxSink` from the same `potAccounts` in one transaction, then `sweepPot` transfers remaining loot. A failed residual transfer is retained for review. `returnStakes` stays untaxed. `coinPot` sums coin denars across pot buckets for sweep tax math.

## Character ownership and recovery

Private table ownership uses a separate recorded owner character and the [idle-only property estate participant](OWNERSHIP.md). Transferring the table never changes its wager identities or money. Pending ownership prevents new stakes/sessions; existing captured payouts can finish subject to the original money and identity guards. Held raw ownership persistence refuses further money writes, and ownership recovery never replays or removes a wager intent.

A table stores `wagerCharacters`, mapping account UUIDs to the character captured when money enters play or the session begins. Tax quotes use that immutable character reference, including offline winners. A missing reference or another active character on the same account cannot collect a payout or refund. A settled round clears bindings when no player stakes remain, even if the house tray is nonempty; the next occupant can then bind their own character.

The synchronous character session-end listener can pay that exact captured character into its still-loaded outgoing body after the current session clears. Sources retain current-session checks. Every outgoing payout leg reserves storage space before effects; another captured character, a successor session, a dead body or insufficient room keeps the money on the felt with a review record. No ending-session authority survives into deferred callbacks. The inventory delivery and table save remain separate effects and require manual review after an interrupted tick; see [OWNERSHIP.md](OWNERSHIP.md).

Citizen tax is a pure `TaxPolicy` quote. Whole-chip rounding and source priority remain unchanged: net payout first, then whatever tax chips the sources can actually supply. The credited tax is exactly the chip value destroyed, in cents, even when the quote rounds or the payout is partial. Partial payments retain the paid amount, actual withholding and remaining obligation separately; they never retry the full gross amount automatically.

Interrupted intents, unresolved identity/tax policy, partial winnings and failed guild tray settlements freeze further transfers, round clearing, editing and pickup. On restart the table and journal remain for review. Legacy saved player stakes without a recorded character also require review; loading never guesses from the account's current or last-played character.

Staff recovery is manual because Minecraft inventory delivery and the money ledger are not one atomic store:

1. Preserve the table JSON, `Data/wager-intents/<table-id>.json` and any guild migration backup before investigating.
2. Inspect the operation ID, ledger legs, encoded items, captured character/tax destination, float before/after and `unpaidOutcomes`. The latter are observations of failed or partial settlement attempts; repeated observations must not be summed as independent debts.
3. Check Denars status for the recorded operation and compare the saved table, inventories and casino-profit bookkeeping. `prepared` does not prove no posting occurred; `applying` does not prove delivery finished.
4. Reconcile the verified remaining obligation once through a reviewed ledger operation and item correction. Never recalculate the original tax against today's character or guild, replay gross winnings, or remove the journal merely to unfreeze a table. Keep the evidence with the correction.

Physical item escrow and automatic recovery of ambiguous item delivery are outside this system. There is no automatic journal replay on startup.

## Coin selection is exact, not greedy

`CoinPlanner` does exact subset selection over distinct `(unit, count)` pairs, by depth-first search with memoisation on `(unitIndex, remaining)`.

Greedy largest-first is wrong here. Holding 6, 5 and 5 and needing 10, greedy takes the 6 and strands the rest. Ledger stakes carry arbitrary units, because `wager.items` entries declare any value and `proposeLoot` lets a player wager a loot item for any denar amount, so odd sets are normal rather than hypothetical. The same planner backs both `PlayerAccount` and `BucketAccount`, so a take and its refund can never disagree.

`CoinPlanner` has no Bukkit in it and is covered by `CoinPlannerTest`.

## The denomination set, and change

The live coins are pouch 100, stack 10, handful 5, gold coin 1, and `v.gold_ingot` at 1 with `withdraw: false`. Silver at 0.1, 0.05 and 0.01 exists but cannot be staked, since anything below a whole denar is rejected.

The usable set is therefore 100, 10, 5, 1. There is no 25 or 50 coin, so a 50 double needs five stacks and a player holding only one pouch cannot pay it exactly.

So DenarEconomy makes change. `MoneyManager.breakCoin(stack, minUnitValue)` returns strictly smaller coins worth exactly the same, honouring `canWithdraw()` so a gold ingot is never produced, and refusing to break below 1 denar because the result would be unstakeable. The arithmetic sits in `CoinChange`, which is Bukkit-free and tested in `CoinChangeTest`.

When a player's coins cannot make an exact plan, `PlayerAccount` breaks the smallest coin that would help and plans again, gated on free inventory space. The break happens inside the take, as part of the same transaction, and is value neutral: the player is carrying different coins worth the same amount.

## Invariants

`LedgerAudit.check` runs after every commit and complains about a negative table total, a negative bucket, a stake counting below zero, and a chip worth nothing, which is money that can neither be paid out nor taken away.

`LedgerAudit.checkLoaded` totals each table on startup against the figure in its file, so a stake dropped on load is noticed before anyone plays on it.

Blackjack adds `checkBoxBets`, which asserts a box's ledger total equals the sum of its hands' bets. That is the check that catches a doubled bet backed by money that was handed back.

Nothing here corrects a total. Quietly fixing one would hide the bug that caused it, and a papered-over total is how a table ends up inflated with nobody knowing when it started. Everything goes to `MoneyLog.mismatch`; `wager.audit-log` turns the full trail on.

## Related

- [BLACKJACK.md](BLACKJACK.md) for the house reserve and split money flow
- [GUILD_TABLES.md](GUILD_TABLES.md) for where house money comes from
