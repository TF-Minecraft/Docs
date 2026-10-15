# Treasuries and financial recovery

SimpleFactions uses DenarEconomy's ledger for guild money. Each guild incarnation
has a `guild:<incarnation UUID>` account; its location and display name do not
identify its money. Recreating a disbanded guild gives it a different account.
`Bank.getWealth()` is a read-only denar view. Guild debt remains signed, and
moving or removing a bank does not transfer its balance.

DenarEconomy and TLibs character identity read only on the main thread. Income
previews that calculate off it, such as branch upgrades and law or treaty
estimates, use every guild's balance and each realm's espionage stability
(including a dead Spymaster's vacancy) as they were when the menu opened.

Legacy treasury balances and accumulated citizen tax are imported once using
`import-guild:<incarnation>` and `import-tax:<incarnation>` operation IDs.
Citizen tax is withheld inside the earning transaction and credited to
`guildtax:<incarnation>`. SimpleFactions registers its tax policy only after
startup recovery completes. Consumers must defer taxable transactions while
that policy is unavailable.

## Daily settlement

The day counter tracks server uptime, rather than calendar dates. One balanced
posting, `sf:settle:<day>`, covers every realm's daily money movements. The
stored plan includes all cents, account IDs and resulting financial state;
recovery never recalculates a published plan.

Preparation records the calculation timestamp, upkeep decisions and the selected
province losses before applying nonfinancial changes. It then records exact
movement organization and offline-day values. Recovery finishes this same
prepared day before allowing new gameplay or death reconciliation.

The settlement preserves the order of army and installation upkeep, trade and
other income, inter-guild transfers, liquidation, dividends and wages, loan
and contract updates, and finally vehicle upkeep. Army upkeep can preserve debt.
Unaffordable installation upkeep downgrades or removes the installation without
charging it. Vehicle upkeep requires the full projected amount, including any
tax; insufficient funds leave the balance intact and record unpaid maintenance.
Personal vehicle payers are captured character IDs.

Available payout funds are shared between dividends and wages. Unpaid wages and
fixed claims owed to deceased characters remain owed. Death dividend claims
reserve part of the dividend pool before living members receive their shares;
they do not add another copy of that payout. Claims against a disbanded guild
can still use its preserved incarnation treasury.

All monetary legs post together. Only an `APPLIED` result permits the recorded
branch levels, loan balances, histories, maintenance state and payment receipts
to be saved. A failed save stops faction gameplay until recovery. The completed
day clock is persisted with these effects; a restart cannot pay that day twice.

## Other financial actions

Deposits, withdrawals, staff `addguildbank`, branch changes, loan acceptance and
repayment, mercenary formation, capital changes, relocation and pillage use
durable operation intents. They capture the actor's character session and the
participating guild incarnations. Confirmations cannot act for a new character
or a replacement guild.

Loan offer IDs are paid once. An offer book records the lending guild's
incarnation; books written before that binding existed, or whose lending guild
has been deleted and recreated under the same ID, are rejected as out of date
and the lender must issue a new agreement. Principal acceptance and its debt record recover
together. Manual repayments credit the lender directly and persist exact debt
and credit-score changes; they do not create another daily receipt. Pillage
uses the war identity and attacker incarnation to recover the same loot and
penalties. Capital and relocation recovery also repairs an interrupted change
across faction files before those files are loaded into domain objects.

Material deposits credit the captured character's bank and actual citizen tax
holding account in one posting. Materials are removed only after `APPLIED`,
and the player then sees the credited amount and any tax in chat.
Staff physical coin withdrawals record the proposed inventory change before
posting. An interrupted material removal or coin delivery requires staff
reconciliation: recovery does not repeat physical delivery automatically.

Games casino profit bookkeeping has its own durable intent. The money has
already reached the guild treasury; this records its taxable income once.
Startup finishes an incomplete bookkeeping save before daily settlement. An
exact retry after the profit has been settled does not tax it again.

## Vehicle finance

Vehicle payments use the selected living character. Construction and
maintenance capture a character session; handovers capture both participants,
so switching characters cannot redirect an armed payment. `Cache/vehicles_registry.json`
keeps PERSONAL records whose `playerUuid` is the payer character UUID and whose
`accountUuid` caches that character's account for slot limits; personal daily
upkeep and vehicle tax charge only that recorded payer, never the account's
current character. Upkeep covers every vehicle VehicleFramework names a
character or legacy account as owner of, minus faction vehicles; without a
readable VehicleFramework it covers the personal rows. [Vehicle owners](vehicle-owners.md)
covers how owners and rows are kept in step.

On the first vehicle stage (see [Vehicle owners](vehicle-owners.md#startup)),
`identity/vehicle-payers.json` records every player-owned vehicle from
VehicleFramework's persisted
repository, mapping the account to its legacy heir character. Existing registry
records win, the plan is saved before the registry changes, and it never
reinterprets later owner-tag changes. Unresolved owners keep a null payer and
stay unpaid; there is no in-game command to reassign them, and the completed
plan must not be deleted to force a new mapping.

Fees, refunds and maintenance use durable intents in `vehicle-payments/`,
recovered at startup before realm settlement. `Cache/vehicle_fees.json` holds
outstanding build, claim and handover receipts; an unfinished receipt blocks
new ownership payments for its vehicle and leaves its daily upkeep unpaid,
rather than charging the previous payer. A construction refund pays the
originally captured character from the original guild incarnation, limited to
the treasury's positive balance. Maintenance explicitly selects bank or pouch
and never falls back to the other. Daily vehicle charges run last inside the
single `sf:settle:<day>` posting, as described above.

## Saved recovery state

Paths are relative to `plugins/SimpleFactions/`:

| Path | Purpose |
| --- | --- |
| `day-preparation/<day>.json` | Captured timestamp and nonfinancial day preparation |
| `settlements/<day>.json` | Immutable realm posting and exact financial after-values |
| `economy/callers/` | Interactive treasury and topology operation intents |
| `external-income/` | Idempotent external casino income bookkeeping |
| `deaths/` | Death cleanup, succession and outstanding character claims |
| `deaths/payments/` | Settlement acknowledgments for those claims |
| `vehicle-payments/` | Vehicle fee, refund and maintenance intents |
| `identity/vehicle-payers.json` | One-time legacy vehicle payer migration plan |
| `vehicles/owner-migration.json` | One-time vehicle owner migration plan ([Vehicle owners](vehicle-owners.md#files)) |
| `Cache/vehicles_registry.json` | Vehicle ownership scopes and personal payer characters |
| `Cache/vehicle_fees.json` | Outstanding vehicle payment receipts and owner history |
| `Cache/vehicle_maintenance.json` | Vehicle upkeep and unpaid maintenance state |

An intent is forced to storage before its dependent action. Completed intents
and receipts are financial history, not disposable retry files. Restoring a
completed receipt without its corresponding DenarEconomy posting is rejected.

For an unresolved operation, retain its file, operation ID and matching ledger
status. For physical items, also inspect the captured character, inventory
snapshot, item bytes and amount. There is no command to discard an ambiguous
physical intent. Correct the underlying persistence or data problem, reconcile
physical evidence where necessary, and restart to resume the saved intent.

Back up or roll back SimpleFactions, RPCharacters and DenarEconomy together using
a consistent stopped-server copy. Do not combine an old ledger with newer
faction journals or delete receipts to force another payment.

See [character membership](characters.md) and the shared
[DenarEconomy guide](../../DenarEconomy/README.md).
