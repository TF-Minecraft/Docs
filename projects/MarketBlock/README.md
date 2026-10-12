# MarketBlock

[Source repository](https://github.com/TF-Minecraft/MarketBlock) · [All projects](../../README.md)

Technical documentation is maintained here. Run commands from the source checkout unless a guide says otherwise.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

See the [shared API versions](../../PLATFORM.md#shared-api-versions) for the matching provider dependency set.

## Character payments

A sale credits the seller's current character pouch through DenarEconomy 0.3.0.
Realm tax is part of the same ledger posting. Without an active character, the
sale is refused. Goods are removed only after the ledger confirms payment;
refused or unavailable payments leave the goods untouched.

Before posting, MarketBlock saves the operation ID, owner account, character,
gross cents and inventory plan in `plugins/MarketBlock/pending-sales/<owner>.properties`.
Completed and refused intents are removed. An unavailable payment or interruption
keeps its intent and blocks new sales for that account until staff reconcile it.
Repeating the same click does not create another sale.

To reconcile an interrupted sale, stop further sales for that player and inspect
the saved operation in the DenarEconomy ledger alongside the player's inventory.
An applied operation already paid the captured character; never credit it again.
Resolve any outstanding item removal before archiving the intent. An operation
absent from the ledger has not paid; retain the goods and archive the intent only
after confirming that state. Do not delete pending files as routine cleanup.

The payment is transactional, but Minecraft inventory saves and ledger commits
are separate. A crash can leave an applied payment with goods still present;
this requires reconciliation rather than automatic replay.

## Build and dependencies

From the MarketBlock source checkout, install the shared plugin versions pinned
in `pom.xml` (TLibs 2.4.0 and DenarEconomy 0.3.0), then verify with Java 21:

```sh
python3 path/to/TLibs/tools/install-plugins.py --pom pom.xml --mode pinned &&
  mvn clean verify
```

Point the installer at a separate TLibs checkout. See
[build dependencies](../../PIPELINES.md#build-dependencies) for access and checksum verification.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
