# Persona validation and operations

Run these checks against the source and dependency set being released. Back up configuration and player data before replacing jars. Avoid duplicate chat and roll handlers.

## Staging — RPCharacters configs

Ensure these exist under `plugins/RPCharacters/` (copy from jar resources on first run or merge manually):

- [ ] `persona.yml` — `no-character-fallback` (bundled default `'#ffffff§oUnknown'`; `createConfigs()` does not overwrite existing files)
- [ ] `chat.yml` — ensure `no-character-message` and per-channel `require-character: false` on OOC/staff channels (`ooc`, `admin`, `helper`, `dm`); IC channels default to requiring a character
- [ ] `masks.yml`
- [ ] `rolls.yml`
- [ ] `profile-view.yml`
- [ ] `permission-groups.yml` — donor/default perks (name-colour stops, character-switch cooldown days)
- [ ] `calendar.yml` — set `base-irl-year` to the IRL year when the season started; `age.minimum` is the global minimum character age
- [ ] `races.yml` — per-race `age-max`

Reload or restart after config changes.

---

## Staging — LuckPerms

Check permissions against the current commands and configuration:

- [ ] `rpchar.persona.set` — `/rpcharacter alias`, gender, description
- [ ] `rpchar.group.noble` / `rpchar.group.gilded` / `rpchar.group.ascended` — name-colour stops and shorter switch cooldown (see `permission-groups.yml`)
- [ ] `rpchar.profile` — shift-right-click profile
- [ ] `rpchar.chat.use` (+ channel-specific perms from `chat.yml`)
- [ ] `rpchar.roll` (+ `rpchar.roll.alt` if using 1–200 `/roll`)
- [ ] Admin: `rpchar.persona.override`, `rpchar.chat.admin`, etc. as needed
- [ ] Staff: `rpchar.tempalias` (session IC chat override), `rpchar.character.hidden` (hide char from TAB via slug)


---

## Staging — TAB / PlaceholderAPI

- [ ] Tab list name: **`%rpcharacters_display_safe%`** only (never `%rpcharacters_display%` on TAB)
- [ ] `%rpcharacters_display_tab%` is the **real active** character (profiles, character menus) — not TAB when hidden chars are used
- [ ] Chat/profile placeholders: `%rpcharacters_name%`, `%rpcharacters_display%`, `%rpcharacters_display_safe%`, `%rpcharacters_age%`, `%rpcharacters_birthday%`, `%rpcharacters_race%`, `%rpcharacters_gender%`, `%rpcharacters_description%`

---

## Staging smoke test

### Chat

- [ ] Channels: `rp`, `shout`, `yell`, `whisper`, `looc`, `ooc`, `action`, `admin`, `helper`, `dm`
- [ ] Plain chat (no command) → default `rp` channel
- [ ] No active character: plain chat and IC channels blocked; TAB shows **Unknown** (`%rpcharacters_display_safe%`); `/ooc` works with IGN
- [ ] Channel commands registered from `chat.yml` on load/reload (no jar rebuild for new channels)
- [ ] Colour codes gated by `rpchar.chat.colors`
- [ ] Channel cooldowns work
- [ ] **No duplicate messages** (only RPCharacters handling chat)

### Masks

- [ ] Wearing mask: `{display}` channels show plain **Masked** (no colour on label)
- [ ] Plain chat (no command) works while masked — shows **Masked** on default RP channel (no `/rp` required)
- [ ] TAB name unchanged when mask worn (`display_safe` ignores mask; chat `{display}` shows **Masked**)
- [ ] LOOC/OOC still use account `{player}` — mask does not rename those channels

### Profile

- [ ] Shift-sneak, empty hand, right-click player → profile lines from `profile-view.yml`
- [ ] **Denied** when target is masked
- [ ] `/rpcharacter profile [player]` works with `rpchar.profile`

### Persona

- [ ] `/rpcharacter alias`, `namecolour`, `gender`, `description`
- [ ] `/rpcharacter tempalias <name>|clear` — session IC chat override (below mask); cleared on quit
- [ ] `/rpcharacter sethidden <slug>` toggle; `/rpcharacter sethidden <slug> clear` to unhide; TAB uses `%rpcharacters_display_safe%`
- [ ] Name colour: tier limits from `permission-groups.yml` (0 default, 1 noble, 2 gilded, 20 ascended); multi-hex gradient supported
- [ ] Admin `/rpcharacter override ... namecolour` bypasses tier limits and persists through rank changes (`name-colour-staff`)
- [ ] Default description template with `{continent}` — vowel races produce **An** (not **Aan**)
- [ ] Character Info GUI (ender pearl) shows display, gender, age, and description

### Character switch cooldown

- [ ] Stored as `last-character-switch-ms` timestamp (wall-clock; no online-only tick)
- [ ] Default **14** days; noble **10**, gilded **7**, ascended **5** (`permission-groups.yml`)
- [ ] Cooldown length resolved from **current** rank at check time (upgrade mid-cooldown can unlock sooner)
- [ ] Legacy `cooldown` minutes in player JSON migrated on first load
- [ ] `/rpcharacter skipcooldown <player>` clears switch timestamp

### Rolls

- [ ] `/roll` → 1–100 (or 1–200 with `rpchar.roll.alt`)
- [ ] `/roll 20` and `/roll 20 +3` (display-only modifier)
- [ ] `/roll strength` (or other attribute) with MMOCore modifier

### Age

- [ ] Character creation: age stage after race selection; birthday saved in character JSON
- [ ] Minimum age **18** for all races (`calendar.yml` `age.minimum`); maximum per race (`age-max` in `races.yml`)
- [ ] `%rpcharacters_age%` and profile `{age}` show computed age; `Unset` when no birthday

### Conversations

- [ ] `ConversationManager` counts via `CharacterChatEvent` only
- [ ] Plain chat counts as `rp`; LOOC excluded; masked speakers skipped for conversation tracking

---
