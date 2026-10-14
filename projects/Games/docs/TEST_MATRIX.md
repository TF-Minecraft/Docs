# Games - Manual test matrix

Run the checklist for the source and dependency versions being released. Player-facing strings must not use an em dash (U+2014).

Run these checks on Minecraft **1.21.10** with the intended plugin dependencies and JVM from the [shared platform baseline](../../../PLATFORM.md). Record the source revision, server build, JVM and results; the checklist alone is not evidence of a passing release.

## Automated tests

`tfmc-mvn -o -B clean verify` runs the JUnit suite (MockBukkit and Mockito) and writes JaCoCo reports to `target/site/jacoco/`. JaCoCo measures every production class with no exclusions and enforces no threshold; open `target/site/jacoco/index.html` to inspect uncovered behaviour. Coverage data is replaced on each run, so use the full suite when assessing repository-wide coverage.

Game scenarios drive public callbacks through complete Poker, Draw and Blackjack rounds across the real table, deck and money implementations, and assert game rules, money conservation or player-visible effects. Tests should protect supported behaviour, not create impossible internal states merely to execute a branch. Where no real caller can reach a branch, remove the branch rather than force it.

Packet tests verify ProtocolLib requests through mocked boundaries only. Packet encoding and client rendering are covered by the manual checks below.

---

## Build and startup

- [ ] `mvn package` succeeds
- [ ] Plugin enables with TLibs, ItemsAdder, ProtocolLib
- [ ] Default yaml copied to `plugins/Games/` (`config.yml`, `messages.yml`, `cards.yml`, `games.yml`)
- [ ] `/games` with no args shows usage
- [ ] `/games reload` as op succeeds
- [ ] No permission: denial from `messages.yml`
- [ ] `debug: true` logs cache values on load/reload

---

## ItemsAdder

- [ ] Pack `tfmc_games` loads
- [ ] `deck`, `card_back`, `card_base`, and 52 faces obtainable (suits: cerrith, mitlan, oseni, seithr)
- [ ] Ace items use `_1` / rank 1, not 14 (e.g. `tfmc_games:cerrith_1`)
- [ ] No `_14` item ids
- [ ] Jokers are not in the pack yet; `french_54` lists the same 52 ids as `french_52`
- [ ] `card_base` is an IA item but not in either set

---

## Deck engine

- [ ] `/games deck test` uses `poker.card-set` (`french_52`)
- [ ] Reports 52 cards, 0 jokers, remaining 0 after draw-all
- [ ] Empty draw does not yield a card
- [ ] After return, remaining is 1
- [ ] `/games deck test french_54` matches until jokers exist
- [ ] Unknown set name is rejected

---

## Display

- [ ] `/games display test` (player, ProtocolLib up)
- [ ] Nearby players see a packet ItemDisplay
- [ ] Per-viewer item: command sender sees a face, others see the back
- [ ] Slide uses transform interpolation (not teleport)
- [ ] Rejoin while the token is live still shows it
- [ ] Right-click the Interaction reports a click; label "Display test" is visible
- [ ] Token, interaction, and label despawn after about 8 seconds

---

## Place table

- [ ] `/games place poker`, hold deck, right-click a block
- [ ] Label reads Poker; cards lie flat (not standing)
- [ ] At most `stack-visible-max` backs
- [ ] Restart / chunk load restores the table
- [ ] Left-click the Interaction drops a deck item and removes entities / json

---

## Hand

- [ ] Right-click draws one card into a sorted fan
- [ ] Fan sits at table height between player and stack
- [ ] Other players see backs
- [ ] Leave-distance returns cards and restacks
- [ ] Standing (no chair) still places the hand correctly

---

## Select and return

- [ ] Right-click a fanned card toggles it (swing on hit only)
- [ ] Selected cards sit at `selected-distance`
- [ ] Right-click the shoe with a selection returns those cards without drawing
- [ ] Right-click the shoe with nothing selected still draws

---

## Wager

- [ ] Denars escrow and refund
- [ ] Item proposal requires agreement
- [ ] Pot displays at the `pot` anchor
- [ ] Disconnect / table break refunds

- [ ] Shift+right-click the shoe pays the pot to you (engine). Set games, including poker, disable this.

---

## Blackjack

See [BLACKJACK.md](BLACKJACK.md).

- [ ] Claim dealer at stand; logout clears; walk-away does not
- [ ] Min/max/open/close; illegal bet restores chips
- [ ] Deal order, hit/stand, S17, even money settle
- [ ] 3:2 natural, double, split, DAS
- [ ] Auto: 10s after first min bet, spawn pays
- [ ] Voice via RPCharacters `dispatch`, not `/rp` command
- [ ] With TLibs 2.6.0 and a compatible RPCharacters provider, table labels and game messages show the current mask/alias; changing it or switching characters updates the next rendered name without revealing a canonical name
- [ ] An online player with no active character shows the RPCharacters no-character label (`Unknown` by default), matching chat
- [ ] Without the character provider, online labels use account names and offline names use the last known account name or `-`; missing identity still refuses current owner authority, new character-bound sessions and unsafe wagers

---

## Guild house

See [GUILD_TABLES.md](GUILD_TABLES.md).

- [ ] BJ options GUI persists auto / mint / min-max / boxes / shuffle; chunk reload keeps them
- [ ] Guild auto consumes expansion cap; staff mint does not; no SF → guild auto refused
- [ ] Cap drop freezes new rounds on all counted tables; live rounds finish
- [ ] Guild cover withdraws shortfall only; empty bank restores the chip; pickup deposits tray
- [ ] Dealer: guild member set/unset; no mid-round; takeover auto frees slot; no takeover of staff mint
- [ ] Shuffle `ROUND` vs `SHOE` matches policy after a full round

## Ledger and identity failure checks

- [ ] While installed SimpleFactions is waiting, new rounds and guild migration stay closed; readiness permits them without restarting Games.
- [ ] Switching characters on one account cannot collect or edit the other character's guild table/stakes; a later settled round can bind the new character.
- [ ] A deleted guild's namesake cannot claim the old table or bank, including after restarting migration.
- [ ] A bank-funded win and its actual withheld chip tax produce one balanced Denars posting; refused posting changes no items, float or casino profit.
- [ ] After a posting, interrupt table save or profit bookkeeping; restart retains a frozen table and intent without delivering money/items again.
- [ ] Missing winning character, mid-round tax failure and partial payout retain the remaining obligation and prevent round clear/pickup.

Run automated checks with `tfmc-mvn -o -B --no-transfer-progress clean verify`. Journal tests inject posting, storage and bookkeeping failures; they do not prove atomic Minecraft inventory persistence or replace server integration checks.

## Private ownership and estates

See [OWNERSHIP.md](OWNERSHIP.md) for source paths, compatibility probes and the conservative rollback procedure.

- [ ] Character A owns a private table; same-account B cannot edit, deal, host or confirm A's old menu/placement arm, including a missed session-end event and an A-to-B-to-A session renewal.
- [ ] A's synchronous session-end cleanup refunds its captured stakes and idle private float into A's outgoing body, preserving total value and producing no world drops. A different recorded character, an active successor, a dead body or insufficient space holds all value for review; matching partial stacks count as available room.
- [ ] Ending-session authority cannot fund a new source leg or survive into a deferred payout. Ordinary quit cleanup followed by the end event does not pay twice. A captured taxed payout retains the full wager and tax envelope and conserves inventory plus ledger value.
- [ ] Staff edits opened before a table changes owner cannot apply or restore the old owner, including queued chat and an owner changing back.
- [ ] Guild-plus-mint, nonguild mint, human private and automatic private tables follow their separate authority and inheritance classification.
- [ ] Legacy missing/null mode fields and explicit mint/non-mint values use the same raw/runtime classification; frozen mode survives layout changes, loading and publication interruption without recapturing owner or changing money.
- [ ] An unready reviewed-heir service makes no migration or empty estate receipt; later readiness resolves raw unloaded rows without discarding settings or unknown nulls.
- [ ] Duplicate JSON fields/IDs and invalid owner/guild/float UUIDs stay untouched and held. External file replacement or deletion is detected before money effects, pickup or a save/estate publication and during deferred loading, including matching size and modification time; a held table refuses new money.
- [ ] A live private table receives a durable pending estate intent: new activity is refused, captured work can settle, and only idle ownership moves without touching floats, wagers or unknown fields.
- [ ] Restart resumes the exact current decision; changed historical envelope/receipt IDs, partial stale transfers and a restored completed source block every later recipient mode.
- [ ] Empty CHARACTER/WAITING/FROZEN completions record exact revision evidence; same-revision new ownership or changed decisions block, newer guarded revisions can consider untouched new property, and retained completions preserve cumulative moved IDs.
- [ ] Confirmed revival releases untouched pending plans; missing provider evidence and partial publication retain the hold.
- [ ] Rollback preview accepts only the exact migrated source; progress, active/recovery marker and estate history refuse apply. Successful apply preserves current bytes and restores the immutable original.
