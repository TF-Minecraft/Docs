# BarterShops

[Source repository](https://github.com/TF-Minecraft/BarterShops) · [All projects](../../README.md)

Sign-based item shops with DenarEconomy payments and faction embargo checks.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Run Maven with **JDK 21** from the source checkout. The POM sets `maven.compiler.release=21` and resolves `io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope from the PaperMC Maven repository. The plugin descriptor declares `api-version: 1.21.10`.

Install these matching Java 21 TFMC artifacts into local Maven before building: `net.tfminecraft:denareconomy:0.3.0`, `net.tfminecraft:simplefactions:4.0.0`, `me.plugins:tlibs:2.6.0`. Their source repositories use `mvn clean install`; CI uses the pinned dependency setup actions.

Populate `libs/` with the exact files and hashes listed in `.github/dependencies.sha256`. `.github/scripts/prepare-release.sh` downloads those pinned private assets when supplied with the approved dependency token.

Install the pinned shared plugin dependencies, download the private build
inputs, then run the build with Java 21. In Bash:

```bash
python3 path/to/TLibs/tools/install-plugins.py --pom pom.xml --mode pinned &&
  (read -rsp 'ServerAssets token: ' GH_TOKEN && echo && export GH_TOKEN &&
    bash .github/scripts/prepare-release.sh) &&
  mvn clean verify
```

The installer comes from a separate TLibs checkout
(`git clone https://github.com/TF-Minecraft/TLibs.git`); point `path/to/TLibs` at it. The token needs Contents read access
to TF-Minecraft/ServerAssets. The prompt keeps it out of shell history, the
subshell keeps it out of your session and Maven, and Maven only runs if both
preparation steps succeed. CI supplies it from `DEPS_TOKEN`.

Use `mvn clean install` when another plugin needs the result as a Maven dependency. The plugin JAR is written under `target/`. Gameplay and web integration checks on the Minecraft 1.21.10 server remain separate from build verification.

## Runtime and configuration

Required plugins declared by the manifest: MMOItems, MythicLib, DenarEconomy and TLibs. Character sessions and reviewed legacy heirs come from RPCharacters. When SimpleFactions is installed, use its character-member release (4.0.0). Shops wait for its migration and tax setup before allowing trades; a disabled or failing provider also closes trades. SimpleFactions remains optional when absent.

`ShopEvents` handles sign interactions and posts currency trades through the DenarEconomy character ledger. `ShopEmbargo` provides the SimpleFactions integration. Shop JSON lives under `plugins/BarterShops/Data`; preserve it across upgrades. The manifest declares one staff command, `/bartershops intent` (see [interrupted trades](#payments-and-interrupted-trades)).

Only the shop's owning character, or staff with `bartershops.admin` (default: op), can break a shop sign or any block the plugin can tell would bring it down: the block the sign is fixed to, every hanging sign above it in a chain, and the block under any sand, gravel or other falling block that holds the sign up. Anyone else is refused with a message. Wall hanging signs stay up when the blocks beside them go, so anyone can break those blocks.

When physics or an explosion would destroy a shop sign, the plugin blocks it and the sign stays where it is, even with nothing left holding it up. That covers blocks that give way later, such as a cactus under a sign, fire burning a wooden support, and pistons moving a support away. Commands that replace blocks, such as `/setblock` with `destroy`, still remove the sign and leave its shop record behind. A shop record is removed when the owner or staff breaks the sign, or when a sign their break was expected to bring down falls within the next minute. A sign that has not fallen by then stays up and keeps its shop.

During setup, BarterShops rejects chest clicks already denied by Thievery or another protection listener. Public and otherwise permitted shared chests can still be linked. Existing links are not revalidated when chest access changes. Linking a chest as a shop's storage gives it no protection, but a chest that a shop sign is fixed to is protected as that sign's support.

## Character ownership and migration

New shops belong to the creating character. The shop file keeps `owner` as the
account UUID and `owner character` as the character UUID; its filename UUID is
the stable shop ID. Another character on the same account cannot remove the
shop. A character switch during setup cancels the next setup step.

BarterShops waits until the identity provider and reviewed heirs are ready. It
checks again every five seconds, keeping creation, trading and owner removal
closed while waiting. Staff removal and sign protection remain available.
Migration writes each original shop to `migrations/backup/<shopId>.json` before
changing it, with a SHA-256 hash and progress record in
`migrations/character-v1/<shopId>.json`. An interrupted migration restores the
verified original before retrying. Existing backups are never overwritten.

An account without a reviewed heir keeps its original shop file and cannot
trade or remove the shop except through staff. The quarantine entry preserves
the complete original JSON; `migrations/quarantine.txt` lists unresolved shops.
After staff correct the reviewed heir mapping, restarting the plugin as part
of a server restart retries the mapping. Backup/hash/write errors keep shops
closed for review. Preserve `Data`, `migrations` and `trades` alongside the
ledger when backing up; rollback restores the same pre-cutover data set for
identity, shops, factions and economy together.

## Payments and interrupted trades

Buying from a shop debits the active customer's pouch and credits the shop
owner's character bank, including while the owner is offline or playing another
character. Selling to a shop debits that owner's bank and credits the active
customer's pouch. Both directions apply the seller's tax inside the same
ledger posting. An owner with insufficient money cannot buy goods on credit.
Zero-price shops record a zero-value posting and still exchange their items.

Items move only after an applied posting. Refused payments leave inventory
unchanged. Each trade first writes `trades/<shopId>.json`, containing its
`shop:<shopId>:<nonce>` operation ID, character references, direction, amount,
quantity and encoded item. A temporary ledger outage retains the same ID for
a retry by the same customer with the same terms. The journal is removed only
after delivery succeeds. Payment event handlers cannot silently change the
character or inventory between payment and delivery: that leaves a review
record instead.

A remaining trade file after restart, conflicting intent, or interrupted item
delivery blocks further trades at that shop. Do not simply delete an unresolved
record or replay its delivery: some or all items may already have moved. Item
inventories and the ledger do not share a transaction, so crash rollback of
Minecraft item saves still requires reconciliation; automatic item escrow is
not provided.

Staff with `bartershops.admin` resolve a blocked shop in game:

```text
/bartershops intent <shopId>                    show the trade record and its posting
/bartershops intent <shopId> clear              clear it when no money moved
/bartershops intent <shopId> clear --confirm    clear it after settling by hand
```

Tab completion offers IDs with retained unfinished trades, including unreadable
records, followed by matching `clear` and `--confirm` keywords on their valid
paths. The ID index loads canonical filenames at startup and follows trade
changes; manual file edits appear at restart or when the record is inspected.
A directory traversal failure logs a warning and retains any IDs already found.

The shop ID is the file name in `Data/` and `trades/`. The command reads the
record's state and asks the ledger for the posting's result:

| Record | Command |
|---|---|
| `prepared`, posting absent or REFUSED, ledger ready | `clear` removes the record. No money moved. |
| `prepared`, posting APPLIED (or CONFLICT) | Shown only. The customer paid but the items did not move: hand them over, then `clear --confirm`. |
| `delivering` or `conflict` | Shown only. The items may already have moved: check the chest and the customer, put things right, then `clear --confirm`. |
| unreadable | Shown only; `clear --confirm` removes it after staff check by hand. |
| ledger not ready | Nothing clears, even with `--confirm`. |

Clearing deletes `trades/<shopId>.json` and the running server's copy of the
trade, so the shop trades again at once without a restart. Every use, viewing
included, is written to the server log and to
`plugins/BarterShops/logs/staff-audit.log` with the record's state, posting
result, operation ID and terms.

## Death and estates

A shop whose owning character is not alive is paused: both buying and selling
answer "This shop's owner has died." A shop whose owner cannot be read (an
unreadable or quarantined account) stays closed with the usual closed message.
A revived owner's shop trades again.

With TLibs 2.6.0 or later, BarterShops takes part in RPCharacters estates as the
`bartershops` participant. When an estate is decided, each shop owned by the
dead character goes to the estate's property recipient (the will heir, or the
death guild's leader): the shop file's `owner` and `owner character` are
rewritten in place in `Data/<shopId>.json`, keeping the shop ID and terms.
Waiting or frozen property leaves the shops paused with the dead owner until
staff assign it. Moves happen only while the dead character is still dead with
that death and the estate is decided at the current revision; a revived
character keeps whatever had not moved yet.

Before changing any shop, BarterShops writes `estates/<deathId>.json` listing the
shops it will move and their recipient, then marks each one moved. A crash
between shops is finished at the next settle, and the outcome reported to the
estate always lists every shop ID moved, which `/estate show` displays. To undo
a move by hand, restore the testator as owner of the shops listed there whose
current owner is still the recipient.

A shop with an unfinished trade in `trades/` is not moved. Its estate answer is
BLOCKED and names the shop; staff resolve it with `/bartershops intent`, then run
`/estate retry <deathId> bartershops`. The stock chest's Thievery lock is
separate property and moves at the next restart. The will screen and
`/estate show` list the character's shops and where their signs stand.

BarterShops settles each decided estate on the first tick after start-up, again
as soon as its own character migration has finished (it waits for that), and then
every hour. It reports to RPCharacters only when its answer changes. On TLibs 2.5.0 it starts
normally without joining estates: shops of dead owners stay paused with them.

## Verification

`tfmc-mvn -o -B --no-transfer-progress clean verify` runs the tests using the
workspace Maven wrapper. The suite covers character ownership, same-account
separation, readiness, backup and interrupted migration recovery, embargo
character arguments, both taxable trade directions, insufficient funds,
durable operation retries and delivery failures, the dead-owner pause, estate
transfers with their journal and crash replay, blocked shops, the hourly
reconcile and every row of the `/bartershops intent` table. Plain `mvn clean verify`
also works with Java 21 and prepared dependencies. Live Minecraft persistence
and a coordinated data migration rehearsal remain separate checks.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
