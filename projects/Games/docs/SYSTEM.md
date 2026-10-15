# Games - System Overview

Tabletop plugin. Engines are dumb: they cannot tell poker from blackjack. Games only call engines.

Games provides blackjack, [Tenceur Hold'em](HOLDEM.md) (`poker`) and [Five-Draw](FIVEDRAW.md) (`draw`). Tables persist locations and house settings; stopping or restarting resets settled sessions to idle; unresolved money operations retain frozen tables for review.


## Config folder layout

All paths under `plugins/Games/` on the server.

| Path | Purpose |
|------|---------|
| `config.yml` | `debug`, stack visual max, card scale, interpolation ticks, table Y offset |
| `messages.yml` | Player-facing chat strings |
| `cards.yml` | Card catalog and named sets (`french_54`, `french_52`). |
| `games.yml` | Per-game rules, layout, blackjack min/max / auto-dealer defaults, [hand card limits](#hand-card-limits). Live auto/mint/shuffle live on the table ([GUILD_TABLES.md](GUILD_TABLES.md)) |
| `help.yml` | The rule books `/games help` opens, one section per book, pages written by hand |
| `Data/tables/` | Gson for placed tables |
| `migrations/table-ownership/` | Immutable original bytes and reviewed legacy-owner plans |
| `estates/tables/` | Guarded private-table transfer intents and receipts |
| `ownership-active` | Running/recovery marker; clean, unheld shutdown removes it |

### Hand card limits

`hand-card-limit` under a game in `games.yml` caps how many cards one player can hold at that game's tables. The count includes cards still being dealt and every Blackjack split group. The bundled file sets 2 for `poker` and 5 for `draw`; `blackjack` and `freeplay` omit it. An omitted, zero or negative value leaves the hand unrestricted. Games copies `games.yml` only when it is missing, so an existing server must add the key to its own file.

ItemsAdder pack lives in the repo at `games/ItemsAdder/tfmc_games/`. Namespace: `tfmc_games`.

## Source layout

Game rules use the shared deck, display and wagering engines.

```
games/
  ItemsAdder/tfmc_games/
  src/main/java/net/tfminecraft/games/
    card/                         # CardId, composition
    deck/                         # shoe shuffle draw
    display/                      # ProtocolLib ItemDisplay + motion
    layout/                       # stack, fan, pot offsets
    ownership/                    # character authority, raw migration and estates
    table/                        # placed deck, seats, persist
    select/                       # closest token on look ray
    wager/                        # denar and item transactions
    game/                         # Game interface and game-specific rules
    command/ loader/ cache/ database/ utils/
    Games.java
```

## Engines vs poker

| Piece | Owns | Must not own |
|-------|------|----------------|
| Card model | id, suit, rank, joker flag | Poker Ace-high ranking |
| Deck | composition, shuffle, draw, discard, recycle | ItemDisplays, who holds a card |
| Display | packet ItemDisplays, per-viewer item, transform interpolation | Poker, seats, pot math |
| Layout | stack / fan / pot transforms from named anchors | Packets, DenarEconomy |
| Table | placed deck, yaw, who is in range, persist | Hand ranking |
| Selector | ray to closest token | Discard vs play meaning |
| Wager | piles tagged by owner (null = communal) and street; refund/payout filters; manual shoe flush | Blinds, 21, house vs pot |
| Poker (Hold'em, id `poker`) | blinds display, streets, showdown, side pots | Packets, IA ids, ray math |
| Five-Draw (id `draw`) | five-card draw, discard round, showdown | Packets, IA ids, ray math |
| Blackjack | claim, bet window, 21, double/split, house pay | Packets, shuffle |

A class is an engine if it cannot tell whether the game is poker or blackjack.

## Display: packet ItemDisplays

Same spawn / metadata / destroy idea as RPCharacters speech bubbles and clues (`FakeTextDisplayPackets`), but `EntityType.ITEM_DISPLAY`.

- Shared **token id** maps to one fake entity id spawned to every nearby viewer.
- Server-facing item for hidden cards is `card_back`. Owner (and showdown) get face item via metadata only.
- Table origin `Location` stays fixed. Deals and slides use Display **interpolation duration** plus translation / rotation / scale. Do not teleport fake entities for card motion.
- Fake entities are not clickable. Spawn a real **Interaction** on the deck for right-click draw.
- Table title is a real **TextDisplay** (everyone should see "Poker"). Do not reuse packet speech bubbles for that.

Validate ItemDisplay metadata indices against the deployed **Minecraft 1.21.10** server and ProtocolLib build when changing display code. The POM compiles against Paper API 1.21.10; a successful compile does not verify packet metadata. Scale uses `org.joml.Vector3f` with ProtocolLib `Registry.get(Vector3f.class)`.

Display API (dumb): `spawn(token)`, `despawn`, `setItem`, `setItemFor(player, item)`, `setTransform(token, transform, durationTicks)`, plus join / chunk refresh.

## 3x3 table anchors

Named offsets in config (tweaked later). Default intent: deck on an edge or corner, pot at center, hands along the rim at table Y. Cards stay small (`card-scale`).

| Anchor | Role |
|--------|------|
| `deck` | Shoe stack (at most `stack-visible-max` backs) |
| `discard` | Face-down pile beside the shoe (`table.discard-offset`). Auto-recycles into the shoe when the shoe is empty or the table has no hands. No click shuffle. |
| `pot` | Wager pile |
| `hand` | Derived from player position vs deck, Y locked to table |

Visible stack layers: `visible = ceil(remaining / full * stack-visible-max)`, never 52 displays.

## Deck composition

The IA pack can include 54 cards (52 + 2 jokers). Poker uses set `french_52` so `draw()` never returns a joker. Unused jokers can sit in the box as layout-only tokens later.

Ace file and IA id is `_1` or `1`, not 14. Ace-high ranking is a poker flag, not a filename.

## Commands

| Command | Permission | Behavior |
|---------|------------|-------|
| `/games help [game]` | `games.help` (default true) | Opens a rule book from `help.yml`. No game id opens the index |
| `/games reload` | `games.admin` and `games.admin.reload` | Reload configuration |
| `/games place` | `games.admin` | Place a table without a deck item |
| `/games bet ...` | `games.bet` | Blackjack betting; `check`, `call`, `fold`, `raise` and `allin` for poker |
| `/games poker ...` | `games.bet` | Poker [tournament](HOLDEM.md#tournaments) settings and actions |

`/games poker kick` completes online tournament registrants when the player can
edit the nearby poker table and its enabled tournament is neither live nor paying.
`/games deal table board|dealer` completes `back` directly after the pile or after
a positive card count. Suggestions match the current prefix without regard to
case. `reload` is omitted when its dedicated permission is denied.

## Dependencies

`TLibs`, `ItemsAdder`, `ProtocolLib` and `DenarEconomy` are required. RPCharacters softdepend (character names and voice). SimpleFactions softdepend (guild auto cap + bank; [GUILD_TABLES.md](GUILD_TABLES.md)). SF does not depend on Games.

The build pins TLibs **2.6.0**, DenarEconomy **0.3.0**, SimpleFactions **4.0.0** and RPCharacters **2.16.0**. Names use the shared
character identity service; voice still uses RPCharacters' chat API. Deploy the
pinned dependencies and compatible character/estate providers with Games and restart to activate them. Private table authority, migration and property settlement are described in [OWNERSHIP.md](OWNERSHIP.md).

## Displayed names

Table labels and game messages resolve online names through
`Characters.displayName`, preserving masks and temporary aliases. Each lookup
reads the provider again, so switching characters or changing an alias is visible
on the next label/message update. Games does not substitute a canonical character
name or query offline character records.

An online player with no active character shows RPCharacters' no-character
label, `no-character-fallback` in its `persona.yml` (`Unknown` by default), the
same label chat uses. Without a provider, online names fall back to the account
name. A null or blank display, an incompatible identity API, or a failing
provider also falls back to the account name; only integration failures log a
warning, once per server start. Offline players use their last known account
name, or `-` when unavailable. Names are presentation only: player UUIDs, wagers,
payouts and table ownership do not depend on displayed names. Private owners and wagers use separate recorded character references.
