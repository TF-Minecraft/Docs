# Estates

[DenarEconomy](README.md) · [All projects](../../README.md)

When a dead character's estate is decided, DenarEconomy moves the character's pouch and bank to the estate's money recipient, and keeps moving any money that reaches those accounts later. RPCharacters decides who receives what (the will heir's bank, the death guild's treasury or the realm treasury, or nothing, which leaves the money for staff); DenarEconomy only moves the money. The rules for the whole estate are in the [RPCharacters estate guide](../RPCharacters/README.md).

The code is the `denareconomy` [estate participant](https://github.com/TF-Minecraft/DenarEconomy/blob/main/src/main/java/net/tfminecraft/denareconomy/ledger/MoneyEstates.java) and the package-private `Ledger.sweepEstate` in [Ledger](https://github.com/TF-Minecraft/DenarEconomy/blob/main/src/main/java/net/tfminecraft/denareconomy/ledger/Ledger.java). It needs TLibs 2.6.0 or later; on an older TLibs the participant does not register and dead characters' money stays where it is.

## The sweep

A sweep first checks, outside any transaction, that the character directory is available and that the character is DEAD with the estate's death ID. If not, it records nothing: a revived, missing or unknown character is never swept.

Then, in one SQLite transaction, it:

1. takes the highest number `n` among operations named `estate:<deathId>:<number>`, whatever their status, or 0 if there are none;
2. reads the character's pouch and bank;
3. if either holds money, posts operation `estate:<deathId>:<n+1>` with reason `estate:<deathId>`: one debit for each account, including a zero one, and one credit of the total to the recipient.

Two zero balances post nothing. Because every stored number counts, including a refused one, a number is never posted twice and a sweep cannot return `CONFLICT`. A sweep is refused only when the credit would overflow the recipient's balance; that number then stays `REFUSED` and the next sweep uses the next one. Reading and posting in one transaction means there is no plan file and nothing to replay after a crash.

## When sweeps run

RPCharacters calls the participant when it decides an estate, when a revision changes a recipient, and hourly while the participant last answered `RETRY`. DenarEconomy also sweeps every decided estate itself at the first server tick and then every hour. That second loop forwards money credited after the decision, such as SimpleFactions wages and dividends, vehicle refunds and RPCharacters paid-change refunds, with no time limit.

Each sweep first checks the estate guard: the character is DEAD with the estate's death ID, and the estate is DECIDED (not reverted) at the revision being settled. A revived character, a later death or a reverted estate stops all further sweeps. A sweep that already committed stays; money that arrives after a revive stays with the character.

## Recipients

When both of the character's accounts are empty there is nothing to move, and the participant answers `DONE` without asking about the recipient, so a gone guild never holds up an estate that has already been swept. Otherwise, estate money goes only to a character account (normally the heir's bank) or a `guild:` treasury; any other account is listed for staff (`BLOCKED`). Before moving money to a treasury, the participant asks SimpleFactions whether the guild still exists:

| Answer | Action |
|---|---|
| Live | The money goes to the guild's treasury. |
| Gone, and it was the death guild whose realm is live | The money goes to the treasury SimpleFactions names for the realm. If the decision did not record the realm, SimpleFactions is asked again for the death guild's realm. |
| Gone, and its realm is gone or unknown, or the guild was the realm's own capital, or staff chose the guild | Nothing moves; the estate is listed for staff (`BLOCKED`). |
| SimpleFactions cannot answer, or is not installed | Nothing moves this time (`RETRY`). |

## What the participant reports

| Outcome | When |
|---|---|
| `DONE` | A sweep completed at the current revision, the accounts were already empty (whatever became of the recipient), or the money is FROZEN. |
| `RETRY` | The guard does not hold, the ledger or character directory is unavailable, the sweep was refused, or SimpleFactions could not answer. |
| `BLOCKED` | The money recipient is not a character account or guild treasury, the guild and any realm to take its money are gone, or (in principle) a sweep conflicted. |

`DONE` carries `cents` (everything moved by the estate's applied sweeps so far, capped at the largest int) and `postings` (how many), with the operation IDs as the moved records. The hourly loop reports an outcome when it differs from the last one the estate service accepted for that death since the server started; a report that fails is sent again at the next pass. One estate that fails is logged and does not stop the others. `cents` is a count for `/estate show`; the site shows the amount moved from RPCharacters' own record.

`describe` gives the will screen and staff a character's money today: `cents` and one line with the pouch and bank.

FROZEN money stays on the dead character's accounts. Staff send it on with `/estate assign` in RPCharacters, or move it by hand with [`/deco move`](operations.md#checking-and-correcting-accounts). MISSING characters get no estate and their accounts stay frozen for staff.

## Checking and rolling back

`/deco account <character>` shows a dead character's balances and the `estate:<deathId>` postings. Every sweep is an ordinary posting, so the ledger format does not change and a jar rollback needs no data change. To undo a sweep, staff post a `/deco move` from the recipient back to the character's account.
