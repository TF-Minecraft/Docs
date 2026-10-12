# Magic - System Overview

Magic provides elemental resonance, Surge and Flow casting modes, artifacts, meditation and [mage gear](MAGE_GEAR.md).

## Config folder layout

All paths under `plugins/Magic/` on the server.

| Path | Purpose |
|------|---------|
| `config.yml` | `debug`, `default_cast_mode`, equilibrium rates, tick interval |
| `gui.yml` | Title, slot map, filler icons, cast mode definitions, bar templates, hex color tokens |
| `messages.yml` | Player-facing chat strings |
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

Config rates are **per hour**; `MagicTickService` applies `rate / 3600` each second.

The character head shows **Corruption** or **Tranquility** (colored label) plus bar and absolute magnitude, live drift spell percents when not zero, and previews at 60 corruption and 100 tranquility.

Element resonance values are also `double` (default `0.0`, max `100.0` per element).

Each element has a passive drift rate in **per hour** (`resonance.decay_per_hour` in `config.yml`, optional `decay_per_hour` override per element). Negative declines resonance; positive gains it. The element icon lore shows the bar plus a drift line (`-0.02/h`, same style as equilibrium), live combined mana/damage/cooldown percents, and an At 100 resonance preview.

Bound skills in `skills.yml` get MythicLib RELATIVE skill modifiers (`mana`, `cooldown`, `damage`) synced from the Resonance session so mana and cooldown checks match GUI Now.

Open Resonance GUIs refresh every second while viewed (same pattern as SimpleFactions `InventoryUpdater`).

## Meditation

Sit with GSit on the circle center (must be in a vehicle). Eight InteractibleFurniture `pedestal` pieces are required:

- Cardinals: three empty blocks then pedestal (`C---P`, offset 4)
- Diagonals: two empty steps then pedestal (offset 3)

No chat or action bar. A white starter orb appears in front of you; left-click hitscan (VehicleFramework-style) begins the orbit field. White orbs are Flow, red are Surge. Mix follows Equilibrium (`whiteChance = 0.5 * (1 + eq/max)`). Hitting red starts a 10s all-Surge lock; another red hit refreshes it.

Each hit costs 1 Focus (RPCharacters, character-keyed). Flow nudges Equilibrium up; Surge nudges it down. Resonance toward cap `sum(element power on sockets) / 8`. Charged artifacts supply usable aura, adjusted by their care state. Empty artifacts do not start a session; missing furniture means no session.

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

- **TLibs** (required, 2.3.0 or newer) - shared identity/session API, item refs, formatHex, inventory scanning
- **ItemsAdder** (required) - `ia.` icons in gui.yml / elements
- **RPCharacters** (required, 2.16.0 or newer) - identity provider, character Focus pool, character head, injury and permadeath APIs
- **InteractibleFurniture** (required) - pedestals

## Commands

| Command | Permission | Behavior |
|---------|------------|-------|
| `/resonance` | `magic.use` | Opens resonance profile GUI |
| `/magic reload` | `magic.admin` | Reload configs |
| `/magic open` | `magic.admin` | Open GUI (bypasses character check) |
