# Ledger, migration and API

[DenarEconomy](README.md) · [All projects](../../README.md)

DenarEconomy keeps every balance and every money movement in one SQLite database, `plugins/DenarEconomy/ledger.db`. Each change is a posting: a set of legs that add up to zero, applied in one transaction under an operation ID that is kept forever. A posting therefore applies completely or not at all, and posting the same operation ID again never applies it twice.

The store is [Ledger](https://github.com/TF-Minecraft/DenarEconomy/blob/main/src/main/java/net/tfminecraft/denareconomy/ledger/Ledger.java). Other plugins use the [Denars](https://github.com/TF-Minecraft/DenarEconomy/blob/main/src/main/java/net/tfminecraft/denareconomy/api/Denars.java) API described [below](#api-for-other-plugins).

## Storage

The database runs in WAL mode with `synchronous=FULL`, so a committed posting survives a crash or power loss. DenarEconomy holds one connection, opened on enable and closed on disable, and every read and write happens on the main thread; a call from another thread throws `IllegalStateException`. TLibs' `SqliteDatabase` opens the file with the SQLite driver that Paper ships.

| Table | Contents |
|---|---|
| `accounts` | One row per account that has been posted to: `id`, `kind`, `owner`, `character`, `label` and the balance `cents`. |
| `operations` | One row per operation ID: `op_id`, `fingerprint`, `status` (`APPLIED` or `REFUSED`), `created` (epoch milliseconds) and `reason`. |
| `legs` | The net change each applied operation made to each account, in cents. |

Amounts are whole cents in 64-bit integers. Balances are read from the database each time; there is no cached copy to lose.

### Accounts

| Account ID | Holds | May go below zero |
|---|---|---|
| `char:<character>:pouch`, `char:<character>:bank` | A character's pouch and bank. | No |
| `guild:<incarnation>` | A guild treasury. A negative balance is the guild's debt. | Yes |
| `guildtax:<incarnation>` | Citizen tax held for a guild until its settlement. | No |
| `legacy:<account>:pouch`, `legacy:<account>:bank` | Pre-ledger money of a Minecraft account that has not reached a character yet. | No |
| `server:mint` | The source and sink for coins entering or leaving as items, staff credits and imports. | Yes |
| `server:tax-void` | Tax with no jurisdiction. | Yes |

UUIDs in account IDs are lower case. Any other account ID is rejected.

### Postings

A posting first adds together the legs on each account, using checked arithmetic. If the legs do not sum to zero, or an operation ID, reason or account ID is malformed, the call throws `IllegalArgumentException` and nothing is recorded. Otherwise the transaction does one of the following:

- **The operation ID already exists with the same reason and legs.** It returns the stored result and changes nothing. The fingerprint compares the reason and the sorted legs, so the order of legs does not matter.
- **The operation ID exists with a different reason or legs.** It returns `CONFLICT`, logs a warning and changes nothing. The first result stands.
- **An account would go below zero where it may not, a sum overflows, or a dead character would be debited.** It records the operation as `REFUSED` and changes nothing. Posting the same ID again returns `REFUSED` again, even if the money has since arrived.
- **Otherwise** it applies every leg, records the operation as `APPLIED` with its legs, and commits.

A dead character's accounts still receive credits such as wages, dividends and refunds. Debits from them are refused unless the posting's reason starts with `staff:` or `estate:`. DenarEconomy asks the TLibs character API for the character's status at posting time.

### Failures

Any SQLite error during a read or a posting logs `Ledger ... failed; refusing all postings until DenarEconomy restarts` at `SEVERE` and closes the ledger. An uncommitted transaction is discarded with the connection. From then on every posting returns `UNAVAILABLE`, balances read as zero, players are told that the ledger is closed, and nothing is kept in memory instead. If the file cannot be opened at startup, the same applies from the start.

Fix the cause, such as permissions, free space or a damaged file, then restart the server. Nothing needs replaying: a posting either committed before the error or did not happen.

### Backups

Back up `ledger.db` together with `ledger.db-wal` and `ledger.db-shm` while the server is stopped, or take a consistent copy of a running server with SQLite's online backup (`sqlite3 ledger.db ".backup copy.db"`). Restore all three files together, and restore the matching RPCharacters and SimpleFactions data from the same backup set. Read the ledger from a copy rather than opening the live file in another tool.

## Legacy money

Before the ledger, each Minecraft account had one pouch and one bank in `plugins/DenarEconomy/PlayerData/<account>.json`. [LegacyMigration](https://github.com/TF-Minecraft/DenarEconomy/blob/main/src/main/java/net/tfminecraft/denareconomy/ledger/LegacyMigration.java) moves that money to characters in two steps, both ordinary postings.

**Import.** On enable, every `PlayerData/*.json` file is posted as operation `import:<account>`, moving its pouch and bank from `server:mint` into `legacy:<account>:pouch` and `legacy:<account>:bank`. When every file has been imported, the folder is renamed `PlayerData.imported` and kept. If the server stops before the rename, the next start imports again and each file's operation ID makes that a no-op. A file that cannot be read, or whose import does not apply, is logged at `SEVERE` and keeps the folder in place for the next start; the other files are still imported. A negative pouch or bank imports as zero with a warning naming the account and amounts.

**Claim.** RPCharacters reports when it knows every account's reviewed heir (`Characters.legacyHeirsReady()`). DenarEconomy checks on enable, whenever a plugin enables, and every five seconds until then. Once ready, it posts `claim:<account>` for each legacy account that holds money and has an heir, moving both legacy balances to the heir's pouch and bank in one transaction. A crash leaves the money either in the legacy account or with the heir. The run logs how many accounts moved and how many still wait. Claims run again on every start, so an heir reviewed later is picked up after the next restart.

Accounts without an heir keep their money in `legacy:` accounts. Staff list them with `/deco legacy` and move them with `/deco legacy assign` (see [Commands](operations.md#assigning-legacy-money)). Nothing chooses a character automatically.

To check a migration, compare the sum of all character and legacy accounts with the sum of every pouch and bank in the old files:

```sql
SELECT SUM(cents) FROM accounts WHERE kind IN ('char', 'legacy');
```

## API for other plugins

Depend on DenarEconomy with `provided` scope and call [Denars](https://github.com/TF-Minecraft/DenarEconomy/blob/main/src/main/java/net/tfminecraft/denareconomy/api/Denars.java) on the main thread.

| Method | Purpose |
|---|---|
| `ready()` | Whether the ledger is open and a character provider is registered. |
| `active(Player)` | The character the player is playing now, or empty. |
| `pouch(CharacterRef)`, `bank(CharacterRef)`, `guild(UUID)`, `guildTax(UUID)`, `MINT`, `TAX_VOID` | Account IDs. |
| `balance(String account)` | Balance in cents; zero when the ledger is unavailable. |
| `post(opId, reason, List<Leg>)` | Any balanced posting. |
| `transfer(opId, reason, from, to, cents)` | A positive amount between two accounts. |
| `status(opId)` | The stored result of an operation, or empty if it was never posted. |
| `earn(opId, character, account, cents, taxable)` | New money for a character, credited from the mint. |
| `trade(opId, reason, buyerAccount, seller, sellerAccount, cents, taxable)` | A sale: the buyer pays the seller. |
| `taxFor(character, cents)` | The tax the registered policy would take. |

Every posting returns a `Result`: `APPLIED`, `REFUSED`, `CONFLICT` or `UNAVAILABLE`. Act on a payment only after `APPLIED`.

Choose operation IDs so that a retry reuses the same ID. Derive the ID from the event when the event can repeat, for example `coin:<item entity UUID>` or `shop:<shop>:<transaction nonce>`, and store a generated ID before any side effect that depends on the payment. A fresh random ID suits a one-off player command. DenarEconomy's own commands use `<kind>:<random UUID>`.

**Tax.** For a taxable `earn` or `trade`, DenarEconomy loads a [TaxPolicy](https://github.com/TF-Minecraft/DenarEconomy/blob/main/src/main/java/net/tfminecraft/denareconomy/api/TaxPolicy.java) from Bukkit's `ServicesManager` and asks it for the holding account and the tax on the gross amount. The earner receives the gross less tax, and the tax leg is part of the same posting. Without a registered policy nothing is taxed. A policy that asks for more than the gross makes the call throw `IllegalStateException`.

**Events.** `PlayerEarnMoneyEvent` fires after a taxable earning or trade has applied, with the earner's account name, the gross amount and `getCharacter()`. It can fire again when an operation is retried, and changing its amount no longer affects tax. `PlayerBankPulseEvent` fires before `/deco deposit` and `/deco withdraw`, and `PlayerDepositMaterialsEvent` fires on a main-hand right click with an item; both carry `getCharacter()` and fire only for a player with a current character.

**Older calls.** `OfflineModifier.apply/change/balance`, `MoneyManager.addMoney/addMoneyToAccount/changeBal/doTaxes/getBalance`, `PlayerManager.get` and the per-player `Database` methods still compile. They act only on an online player's current character: changes post from the mint with reason `api` and never overdraw, and `doTaxes` returns the policy's tax. For an offline player or one without a character they refuse (false, zero or nothing) and log the first caller of each method with a stack trace. `PlayerManager.get` returns read-only balances whose `Account` mutators throw `UnsupportedOperationException`. Move callers to `Denars`; these methods are kept for one release.
