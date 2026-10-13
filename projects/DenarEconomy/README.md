# DenarEconomy

[Source repository](https://github.com/TF-Minecraft/DenarEconomy) · [All projects](../../README.md)

Shared currency plugin for each character's bank and pouch, coins and money drops, kept in a transactional ledger.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Run Maven from the source checkout. The current [POM](https://github.com/TF-Minecraft/DenarEconomy/blob/main/pom.xml) declares Java **release 21** and **paper-api 1.21.10-R0.1-SNAPSHOT**; [plugin.yml](https://github.com/TF-Minecraft/DenarEconomy/blob/main/src/main/resources/plugin.yml) declares `api-version: 1.21.10`. The build and loader metadata target the shared runtime. Gameplay validation remains separate from build verification.

Build with JDK 21. Install the matching TLibs Maven release and populate `libs/` using `.github/scripts/prepare-release.sh`, then verify `.github/dependencies.sha256` and run `mvn clean verify`. The primary output is `target/denareconomy-<version>.jar`. The current CI workflow records the exact dependency setup.

## Runtime and configuration

Required plugins declared by the manifest: MMOItems, MythicLib, TLibs.

Startup loads `coins.yml`, `drops.yml` and `messages.yml`, opens the ledger at `plugins/DenarEconomy/ledger.db`, imports any pre-ledger `PlayerData` files and registers the money and player listeners. `/deco` and `/pouch` are the entry commands. Config reload uses `denareconomy.reload`, `/deco give` uses `denareconomy.give`, and legacy money, other players' history, `/deco account` and `/deco move` use `denareconomy.admin` (all op by default). With TLibs 2.6.0 or later, DenarEconomy also registers the `denareconomy` estate participant, which moves dead characters' money; on an older TLibs it logs that it takes no part in estates.

Money belongs to characters. RPCharacters supplies the current character through the TLibs character API; a player with no current character cannot use money. Preserve the whole data directory when changing builds, including `ledger.db` with its `ledger.db-wal` and `ledger.db-shm` files, `Data` and `PlayerData.imported`.

- [Commands and permissions](operations.md) — the full command reference.
- [Ledger, migration and API](ledger.md) — accounts, postings, failures, backups, the move from `PlayerData` files to characters, and the `Denars` API for other plugins.
- [Estates](estates.md) — how a dead character's pouch and bank reach the heir, guild or realm, and how staff check and correct it.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, dependency selection and rollback.
