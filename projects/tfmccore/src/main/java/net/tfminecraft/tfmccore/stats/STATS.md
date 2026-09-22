# Stats registry

Living reference for all TFMCCore stat categories. Update this file when adding or changing tracked stats.

See also: [ARCHITECTURE.md](ARCHITECTURE.md)

## How to view

- **Command:** `/tfmc stats <category> [player]`
- **Self:** omit the player argument
- **Other players / server totals:** requires `tfmccore.admin`
- **Global toggle:** `plugins/TFMCCore/stats.yml` (`enabled: true`)

## Categories

| Category | Source plugin | Command |
|----------|---------------|---------|
| `vehicles` | VehicleFramework | `/tfmc stats vehicles` |
| `rpcharacters` | RPCharacters | `/tfmc stats rpcharacters` |
| `advancedcrafting` | AdvancedCrafting | `/tfmc stats advancedcrafting` |
| `skills` | MythicLib (MMOCore skills) | `/tfmc stats skills` |
| `factions` | SimpleFactions | `/tfmc stats factions` |

---

## vehicles

**Source:** VehicleFramework `VehicleRemoveEvent` (death only)

**Attributed player:** captain seat occupant at removal

| Stat key | Display label | Trigger |
|----------|---------------|---------|
| `planes_crashed` | Planes crashed | Plane vehicle death with cause `crash` |
| `ships_crashed` | Ships crashed | Ship vehicle death with cause `crash` |
| `ships_sunk` | Ships sunk | Ship vehicle death with cause `sink` |

Labels and vehicle-to-group mapping: `vehiclestats.yml`

---

## rpcharacters

**Source:** RPCharacters lifecycle, permakill, and chat events

### Counters

| Stat key | Display label | Trigger | Attributed player |
|----------|---------------|---------|-------------------|
| `characters_created` | Characters created | `CharacterCreatedEvent` | Character owner UUID |
| `characters_killed` | Characters killed | `CharacterPermakillEvent` (killer only; not menu permakill) | Killer player UUID |

### Class spread (`class_<id>`)

| Stat key pattern | Display label | Trigger | Attributed player |
|------------------|---------------|---------|-------------------|
| `class_<id>` | `class_labels.<id>` or formatter | Create (+1), class change (adjust), permakill (-1) | Character owner UUID |

### Race spread (`race_<id>`)

| Stat key pattern | Display label | Trigger | Attributed player |
|------------------|---------------|---------|-------------------|
| `race_<id>` | `race_labels.<id>` or formatter | Create (+1), race change (adjust), permakill (-1) | Character owner UUID |

### Chat (`messages_<channel>`)

| Stat key pattern | Display label | Trigger | Attributed player |
|------------------|---------------|---------|-------------------|
| `messages_<channel>` | `labels.messages_<channel>` or formatter | `CharacterChatEvent` | Message sender UUID |

Known channels in default yaml: `rp`, `ooc`, `looc`, `whisper`, `shout`, `yell`, `action`, `admin`, `helper`, `dm`, `scene`

Labels: `rpcharactersstats.yml`

---

## advancedcrafting

**Source:** AdvancedCrafting lifecycle events (`AlloyDiscoveredEvent`, `AlloyCraftedEvent`, `ItemCraftedEvent`, `SmithingHitEvent`)

**Attributed player:** crafting player UUID on every event

| Stat key | Display label | Trigger |
|----------|---------------|---------|
| `alloys_discovered` | Alloys discovered | First-time alloy discovery per player |
| `alloys_crafted` | Alloys crafted | Alloy forged (known alloy at drop; new alloy after naming) |
| `items_crafted` | Items crafted | Non-admin item finished at crafting station |
| `items_crafted_<category>` | `category_labels.<category>` or formatter | Same; category from `ItemCraftedEvent.getCategoryId()` (`armor`, `weapons`, `bows`) |
| `hits_<hitId>` | `hit_labels.<hitId>` or formatter | `SmithingHitEvent` (`hit`, `small_hit`, `whittle`, `etch`, `engrave`, `sew`, ...) |

Admin forced crafts (`forcedQualityPercent` set) do not fire `ItemCraftedEvent`.

Labels: `advancedcraftingstats.yml`

---

## skills

**Source:** MythicLib `SkillCastEvent` (after successful cast)

**Attributed player:** casting player UUID (`event.getPlayer()`)

**Trigger filter:** `TriggerType.CAST` and `TriggerType.API` only (active / deliberate casts; not passives, on-hit, or item-click triggers)

| Stat key pattern | Display label | Trigger |
|------------------|---------------|---------|
| `skill_<id>` | `labels.skill_<id>`, `skill_labels.<id>`, or formatter | Successful skill cast with matching trigger |

There is no separate total-casts stat key. Total casts for a player or server = sum of all `skill_*` values in this category.

Skill id resolution: MMOCore `RegisteredSkill.getName()` when cast is a `CastableSkill`; otherwise MythicLib handler `getLowerCaseId()`.

Labels: `skillsstats.yml`

---

## factions

**Source:** SimpleFactions `BattleEndedEvent` (system battle end with winner)

**Attributed player:** each UUID in `event.getParticipantIds()` (warband roster snapshot from both sides at end time; dummy members excluded by SimpleFactions)

**Count when:** `event.hasWinner()` (campaign and manual practice battles)

**Do not count:** staff GUI battle cancel (no event); system end with no winner; military walkovers/forfeits (no live battle event)

| Stat key | Display label | Trigger |
|----------|---------------|---------|
| `battles_joined` | Battles joined | +1 per participant UUID when a battle ends with a system winner |

Labels: `factionsstats.yml`

---

## Changelog

| Date | Change |
|------|--------|
| 2026-08-24 | Added `factions` category (battle participation via `BattleEndedEvent`) |
| 2026-08-24 | Added `skills` category (active skill casts via MythicLib) |
| 2026-08-24 | Added `advancedcrafting` category (alloys, items, smithing hits) |
| 2026-08-24 | Initial registry for `vehicles`, `rpcharacters`, `advancedcrafting` |
