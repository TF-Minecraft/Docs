# Professions

RPCharacters provides account-wide profession levels and lifetime points with per-character upgrade loadouts. LuckPerms profession nodes follow the active character.

## Data model

| Data | Owner | Storage |
|------|-------|---------|
| MMOCore profession XP/levels | Account: each character's progress file, raised on activation to the best of the account's characters | `data/progress/<account>/characters/<char-id>.yml` (`mmo.professions`) |
| Trait profession XP % | Per character | `RPCharacter` / `AttributeData` |
| Lifetime points earned | Account: raised on activation to the most any character holds | `pools.profession-points` in the progress file (`PlayerData.accountProfessionPoints` while bodies are off) |
| Owned upgrades | Per character | `RPCharacter.professionUpgrades` — ordered upgrade id list |
| Free points | Derived | `lifetime[prof] − characterSpentOnProf` |
| LuckPerms `professions.*` | Active character | apply on `activate()`, strip on `deactivate()` |

**Example:** Character A reached Herborist 11, so the account has 10 lifetime herborist points. A spent 7 on perks → 3 free. Character B (new, or after A's death) plays Herborist 11 with 10 free points and zero perks. Each character builds its upgrades independently up to the account lifetime cap; levels gained on any character reach the others when they are next played.

**Remove upgrade (no refund):** drop upgrade id from character list, strip LP nodes — lifetime unchanged, free increases.

---

## JSON fields

**Account** (`data/playerdata/<uuid>.json`):

```json
"account-profession-points": {
  "agriculturist": 10,
  "smith": 5
}
```

**Character** (`data/characterdata/<uuid>/<char-id>.json`):

```json
"profession-upgrades": ["iron_weaponsmith", "chef_1"]
```

---

## Config layout

| File | Contents |
|------|----------|
| `plugins/RPCharacters/professions.yml` | Global: `max_spending_points`, `types`, `breeding_exp`, `lock_breeding`, `perm_context`, `admin-debug-messages` |
| `plugins/RPCharacters/professions/<id>.yml` | Per profession: `name`, `item`, `upgrades` |

**Separate:** `config.yml` `professions:` list is for **trait XP modifier keys only** — not perk definitions.

---

## Commands

| Command | Access | Purpose |
|---------|--------|---------|
| `/profession` | All | Open profession GUI |
| `/profession reload` | `professions.admin` | Reload profession configs |
| `/profession top <prof>` | All | Online MMOCore level leaderboard |
| `/profession givepoints <prof> <player> <amt>` | Admin | Grant lifetime points |
| `/profession removeupgrade <player> <id>` | Admin | Strip upgrade from active character |
| `/profession reset <player>` | Admin | Clear character upgrades |
| `/profession restoreall` | Admin | Re-grant LP for online active characters |
| `/profession refund <player>` | Admin | Clear upgrades + bootstrap lifetime from MMOCore |
| `/profession fixperms` | Admin | Strip and re-apply `professions.*` for active character |
| `/profession confirm` | Player | Confirm upgrade removal |

---

## Permissions

- `professions.admin` — admin subcommands

---

## Upgrade types

Supported upgrade types: `permission`, `breeding`, `station_enchant`, `add_stats`.

---


See [verification](RUNBOOK.md) for release checks.
