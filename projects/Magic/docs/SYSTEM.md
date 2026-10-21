# Magic - System Overview

Magic provides elemental resonance, Surge and Flow casting modes, artifacts, meditation and [mage gear](MAGE_GEAR.md).

## Config folder layout

All paths under `plugins/Magic/` on the server.

| Path | Purpose |
|------|---------|
| `config.yml` | `debug`, `default_cast_mode`, equilibrium rates, tick interval |
| `gui.yml` | Title, slot map, filler icons, cast mode definitions, bar templates, hex color tokens |
| `messages.yml` | Player-facing chat strings |
| `artifacts/sealed.yml` | Sealed-item paths, school selection, rarity weights and opening sound |
| `elements/*.yml` | Element catalog (name, icon, color, skills) |
| `data/characters/<characterId>.json` | Per-character MagicProfile (cast mode, equilibrium, resonance) |

## Resonance GUI layout (54 slots)

The head and cast-mode slots come from `gui.yml`; element positions come from
individual element definitions through `ElementRegistry`.

| Zone | Bundled slot(s) |
| --- | --- |
| Character head | 4 |
| Surge / Flow | 12 / 14 |
| Spirit / Arcanum / Illusion | 20 / 22 / 24 |
| Cerrith / Seithr / Oseni / Mitlan | 28 / 30 / 32 / 34 |
| Necromancy / Shadowmancy / Bloodmagic | 38 / 40 / 42 |

Unreserved slots use the configured border or inner filler.

## Color tokens (gui.yml)

| Token | Hex | Use |
|-------|-----|-----|
| `title` | `#c9a0ff` | Inventory title |
| `label_muted` | `#8b7fa8` | Secondary lore |
| `label_body` | `#d4c8e8` | Body text |
| `label_accent` | `#e8d4ff` | Highlights |
| `mode_surge` | `#e85d4a` | Surge cast mode |
| `mode_flow` | `#5bc4d4` | Flow cast mode |
| `corruption` | `#c45749` | Corruption side of equilibrium bar |
| `tranquility` | `#6ec9a0` | Tranquility side of equilibrium bar |
| `resonance_low` | `#575150` | Low resonance |
| `resonance_high` | `#82d461` | High resonance |

Applied via TLibs `StringFormatter.formatHex` through `GuiText`.

## Cast modes

Stable config IDs (do not rename without migration):

| ID | GUI position | Role |
|----|--------------|------|
| `surge` | Left (slot 12) | Fast power, pushes corruption |
| `flow` | Right (slot 14) | Slow ramp, builds tranquility |

Display names and lore live in `gui.yml` only.

## Equilibrium (session)

Single axis from **-100** (corruption) to **+100** (tranquility). Stored as `double` with 2 decimal precision; display trims trailing zeros (`23.5`, not `23.50`).

| Value | Behavior |
|-------|----------|
| `< 0` | Compounding passive drift deeper into corruption (`passive_corrupt_per_hour` in config) |
| `0` | Stable (no passive drift) |
| `> 0` | Linear decay toward `0` (`tranquility_decay_per_hour`); stops at `0` |

Config rates are **per hour**; `MagicTickService` applies `rate / 3600` each second. Values keep two decimals, so each character's session carries the per-second remainder and applies it in whole hundredths (0.03/h moves 0.01 every 20 minutes). Drift only runs while the character is online; offline time does not count.

The character head shows **Corruption** or **Tranquility** (colored label) plus bar and absolute magnitude, live drift spell percents when not zero, and previews at 60 corruption and 100 tranquility.

Element resonance values are also `double` (default `0.0`, max `100.0` per element).

Each element has a passive drift rate in **per hour** (`resonance.decay_per_hour` in `config.yml`, optional `decay_per_hour` override per element). Negative declines resonance; positive gains it. Like equilibrium, it is applied in whole hundredths while the character is online (-0.02/h is 0.01 every 30 minutes), and the profile is saved when the value moves. The element icon lore shows the bar plus a drift line (`-0.02/h`, same style as equilibrium), live combined mana/damage/cooldown percents, and an At 100 resonance preview.

Bound skills in `skills.yml` get MythicLib RELATIVE skill modifiers (`mana`, `cooldown`, `damage`) synced from the Resonance session so mana and cooldown checks match GUI Now.

Open Resonance GUIs refresh every second while viewed (same pattern as SimpleFactions `InventoryUpdater`).

## Meditation

Sit with GSit on the circle center (must be in a vehicle). Eight InteractibleFurniture `pedestal` pieces are required:

- Cardinals: three empty blocks then pedestal (`C---P`, offset 4)
- Diagonals: two empty steps then pedestal (offset 3)

No chat or action bar. A white starter orb appears in front of you; left-click hitscan (VehicleFramework-style) begins the orbit field. White orbs are Flow, red are Surge. Mix follows Equilibrium (`whiteChance = 0.5 * (1 + eq/max)`). Hitting red starts a 10s all-Surge lock; another red hit refreshes it.

Each hit costs 1 Focus (RPCharacters, character-keyed). Flow nudges Equilibrium up; Surge nudges it down. Charged artifacts supply usable aura, adjusted by their care state. Empty artifacts do not start a session; missing furniture means no session.

Artifacts are shared. Each artifact records the characters that meditated with it in the last `attunement.users.ttl_days` (7). With `n` such users:

- A hit gives `resonance_per_hit / n`, and one sit draws at most `usable aura / n` from each artifact.
- Meditation cannot raise an element above the sitter's **share**: every artifact on the ring adds its usable aura in that element divided by its own `n`. Two characters sharing a 100-aura artifact top out at 50 each; adding a second 100-aura artifact of that element raises both to 100.
- The share is taken when the sit starts. Standing up and sitting again gains nothing past it, and a sit at or above the share shows `meditation.nothing`.
- Nobody loses resonance when someone joins. A character already above their share keeps it until decay brings it down, but cannot gain more there.

## Artifact wear

Every point of resonance an artifact grants in meditation wears it, whoever
receives it. An artifact can grant `artifacts.wear.budget_multiplier` (default
`1.0`) times its highest aura cap in total. With `1.0` a 20-cap common can raise
one character from 0 to 20 once, or two sharers to 10 each. `0` turns wear off. Wear is stored on the item (`magic:artifact_wear`); its lore shows
`Integrity: N%` once it has been worn.

At the budget the artifact crumbles in place into a spent husk:

- Aura, care state, users, wear and the artifact id are removed. Rarity, primary
  element and sacrifice history stay. `magic:artifact_spent` holds the old id.
- The name becomes `Spent <name>`, the glint goes and the aura block is replaced
  by the husk line (`artifact.husk.*` in `messages.yml`).
- No Magic system treats it as an artifact again. The Recycler takes it for a
  share of its rarity's dust (`artifact_returns.husk_fraction`).
- The meditator sees `meditation.crumbled`, the pedestal is saved at once and
  that artifact gives nothing more this sit. Resonance already gained stays.
  Anyone else sitting at the ring treats it as spent, so their sit can still
  complete.

Worn pedestals are saved at most every 5 seconds during a sit and again when it
ends. Shrines, sacrifice, care and
charges do not wear an artifact; only resonance it grants does.

## Artifact rarities

Common, Uncommon, Rare and Legendary. Magic 0.9.0 removed Epic: Rare covers the
low part of Epic's old cap range and Legendary the high part (planar schools
46-75 and 76-150), Epic's random-roll weight went 2/2 to them, its adjectives
moved to Legendary and its models became Legendary-only. Existing Epic
artifacts keep working; their lore shows the raw id `epic`.

## Sealed artifact crafting

Magic 0.11.0 supports sealed artifacts crafted at the MMOItems Rune Crafting
Station. The station recipes and sealed LOOT items are supplied by ServerAssets;
Magic handles opening them.

| Recipe | Enchanted Dust | Result when opened |
| --- | --- | --- |
| Sealed Artifact | 18 | A random planar-school artifact |
| Sealed Oseni Artifact | 28 | An Oseni artifact |
| Sealed Seithr Artifact | 28 | A Seithr artifact |
| Sealed Cerrith Artifact | 28 | A Cerrith artifact |
| Sealed Mitlan Artifact | 28 | A Mitlan artifact |

Hold the sealed item in the main hand and right-click to open it. A normal
right-click on an interactive block, such as a chest, uses that block instead;
sneak-right-click opens the seal. The server's off-hand equipment rules can
prevent holding a seal in that hand.

Each successful opening consumes one sealed item and gives one empty artifact.
If the inventory cannot hold the result, it drops at the player's feet. A failed
roll leaves the seal intact. School-specific crafts retain the normal chance of
secondary schools; choosing a school fixes the primary school only. Opened
artifacts use the same aura, care, meditation wear, husks and
[rarity-based recycling](../../Recycler/docs/SYSTEM.md#magic-artifacts) as node
artifacts. They still need charging before meditation.

`artifacts/sealed.yml` is created from the jar when missing and is loaded again
by `/magic reload`. The `sealed` entries map TLibs `item` paths to an `element`
selection. `random` selects from the generator's configured random pool; an
entry may override the shared rarity weights. Invalid entries are skipped with
warnings, and an unreadable file disables seal opening. Existing files are not
overwritten. The supplied item paths are `m.loot.sealed_artifact` and
`m.loot.sealed_<school>_artifact` for the four named recipes above.

Successful openings are recorded in the server log as `Sealed artifact opened`,
including player, seal, school, rarity and artifact ID. They are not recorded in
`aura.log`.

## Persistence (MagicProfile)

Profiles are keyed by the character UUID from the
[shared identity API](../../TLibs/character-identity.md) and stored in
`plugins/Magic/data/characters/<characterId>.json`. A file whose name differs only in
letter case is reused. If several such files exist and none has the exact name,
loading refuses and leaves them all. An unreadable profile is moved to
`<characterId>.json.rejected-<uuid>`; if that move fails, saves for it stay blocked.

| Event | Action |
|-------|--------|
| Character session starts | Load the character's profile, or create defaults |
| Character session ends (switch, quit or permanent death) | Stop the outgoing character's activities, then save its profile |
| Magic disables | Save every remaining profile; later shutdown steps still run if one fails |

Each live profile belongs to one session. A callback left over from an earlier session
cannot change a later one, even when the player returns to the same character.
`/resonance` refuses with `open.no_character` until the player has an active character
with a loaded profile. Admin `/magic open` without one shows a layout preview that is
never saved; the next session start closes it. Without a provider, resonance state
stays in memory only.

Session end cancels the outgoing character's meditation and sacrifice rites, clears its
spell modifiers and pending menu actions, and closes Magic menus. Old meditation orbs
cannot spend the incoming character's Focus or grant it resonance. Weapon refreshes
and vessel lore updates run on the next tick, and are skipped if the player started,
ended or switched character in between; players with no character still get them.
Charging a station weapon or starting a sacrifice without an active character is
refused with a message, as is a sacrifice whose victim has none. A permanent sacrifice
only fills its vessel after RPCharacters accepts the death.

The resonance screen shows the character's real name in its name colour, never a mask
or alias. Sacrifice lore keeps the victim's character name from the moment of the kill.

## Dependencies

- **TLibs** (required; 2.3.0 or newer to load, 2.6.0 for character-owned mage gear and estates) - shared identity/session API, item refs, formatHex, inventory scanning
- **ItemsAdder** (required) - `ia.` icons in gui.yml / elements
- **RPCharacters** (required, 2.16.0 or newer) - identity provider, character Focus pool, character head, injury and permadeath APIs
- **InteractibleFurniture** (required) - pedestals

## Commands

| Command | Permission | Behavior |
|---------|------------|-------|
| `/resonance` | `magic.use` | Opens resonance profile GUI |
| `/magic reload` | `magic.admin` | Reload configs |
| `/magic open` | `magic.admin` | Open GUI (bypasses character check) |

`/resonance` (alias `/res`) has no argument suggestions. `/magic` completion
follows sender context; console sees only executable branches. Weapon giving
offers chargeable elements and missing open part categories for the selected
core. Artifact roll/give rarity choices follow the selected type's brackets and
the configured random pool. Artifact path completion covers finite single-token
grammar and registered values while preserving earlier text; numeric caps remain
manual input.
