# Character creator

Web + RPCharacters character creation, kits, lore customise, and wardrobe.

**Repos:** `rpcharacters/` · `ProvinceSystem` · `tfmcweb/` · `frontend` · (kits) `armourshop/`

**Depends on:** TFMCWeb identity + `/token create profile` ([identity/tfmcweb.md](../identity/tfmcweb.md)).

## Why

Donators (and later all players) create and manage RP characters on the website with the **same rules as in-game** `/rpcharacter create` / menu. Creation stages sync from the server so YAML edits update the site after reload. Auth stays **in-game tokens** (no website accounts).

## Character creation

### Auth

| Decision | Choice |
|----------|--------|
| Proof of account | In-game `/token create profile` (UUID-bound, Discord-eligible); redeem at `/profile` |
| Code lifetime | Consumed **on redeem** |
| After redeem | API **session** Bearer - **8h** (the site offers no Remember me) |
| Storage | sessionStorage |
| Website accounts | **None** |

### Attribute point-buy

| Rule | Value |
|------|-------|
| Attributes | strength, dexterity, constitution, intelligence, wisdom, charisma |
| Pool | **12** points - must spend exactly 12 |
| Max rank per attribute at creation | **4** in `stages.yml`; rank 4 alone costs 15, so 12 points buy at most rank **3** |
| Cost for *n*-th rank in one attribute | **2^(n-1)** points (1, 2, 4, 8) |
| Sync | Formula + caps exported in creation catalog |
| Character view | Each attribute bar has five segments split across that attribute's ceiling: the best race, affordable rank and trait picks the catalogue allows, honouring mutual exclusions across stages |

Personality / physical / celestial / story traits stay **selection** stages.

### Creation catalog sync

RPCharacters on enable/reload **PUT**s a full-replace snapshot to ProvinceSystem (stage order, options, validation rules, slot limits, attribute formula). Web **GET**s snapshot for the wizard.

The character view reads the synced `background`, which holds the in-game lore of the character's
`background-trait-types` choices, and matches it line by line against catalogue trait descriptions.
Homeland, cataclysm, reclamation and motivation show as cards under Story; the other choices join the
trait tags, with their lore on hover. A `<Race>:` line in a trait's lore starts that race's version, which
only characters of that race see. Lines no trait matches show as prose under Background.

### Characters API + ownership

| Concern | Owner |
|---------|--------|
| Source of truth for living characters | **RPCharacters** |
| Web sessions / create requests | **ProvinceSystem** Characters API |
| Apply web creates into RPC | RPCharacters pull/ingest |
| Identity + mint | TFMCWeb + Discord link |

### Applying web creates

RPCharacters checks each pending create against the in-game creation rules before it writes the
character ([CreationRules](https://github.com/TF-Minecraft/RPCharacters/blob/main/src/main/java/net/tfminecraft/rpcharacters/creation/CreationRules.java)).
A create that fails is rejected, and the Profile shows the reason on the rejected card.

| Check | Rule |
|-------|------|
| Name | Starts with a letter in any alphabet, then letters, spaces, apostrophes, hyphens and full stops; `persona.yml` display-name length; no colour codes |
| Race | Offered by a web race stage |
| Age and birthday | From `calendar.yml` `age.minimum` to the race's `age-max` |
| Class | A displayed MMOCore base class |
| Description | `config.yml` description length |
| Traits | Each trait exists and belongs to a web stage that opens for this character (stage dependency and account age). Per stage: pick count, points and the `permanent-only` filter. Attribute ranks run in order up to the max rank and spend the whole pool. No mutually exclusive pair, and each trait's requirements and account-age playtime are met |
| Clues | At least the character's required count, at most `max-clues`, clue length from `config.yml`, no repeats (ignoring case) |
| Slots | Online owner: their rank limit. Offline owner: their rank limit read from LuckPerms with this server's contexts. When LuckPerms cannot be read, the create stays pending for the next pull |

Gender and name colours are not checked when applying. ProvinceSystem checks name uniqueness on submit,
and RPCharacters trims name colours to the rank's limit at login.

### Product / UI

| Decision | Choice |
|----------|--------|
| Nav | **Character** tab beside Map and Skins |
| Landing | Session → list characters (alive + dead); CTA to create if free slot |
| Create | Multi-step wizard from synced stages |
| Slots | Enforce synced limits (default 3; Gilded 4; Ascended/Legacy 5; hard cap 10) |
| Dual path | In-game `/rpcharacter create` remains; RPCharacters checks web creates against the in-game rules before applying them |

## kits (summary)

Configurable kits in `plugins/RPCharacters/kits.yml`:

| Rule | Choice |
|------|--------|
| Claim command | `/rpcharacter kit <kitId>` with that character **active** |
| Cooldown | **Per kit** (player UUID × kit id) |
| Once per character | Per kit `once-per-character: true|false` |
| Sync | All kit defs + per-character status → ProvinceSystem |

## kit item customise (summary)

Customise **editable** kit lines on the website (character detail → Kits → Edit). Texture via player skins pipeline → `ps_items`; lore via RPCharacters. Block claim while skin pending approval or slug missing on ArmourShop.

**Kit uploads:** new textures (or book covers / 3D model) on editable kit items use **character login only** — no skin mint token. Picking an already-**applied** skin from your account pick list also does not consume a mint token. Standalone skins from Profile's [Skins tab](../cosmetics/skins.md#profile-wardrobe) still need a skin code (**New skin** or `/token create skin`).

Applied skins appear in the kit editor pick list and can be attached to any character with the same `base_set`.

Editable templates: `2d-template` (required), optional `3d-template`. Book journals use kind `book` (unsigned + signed PNGs).

## wardrobe (summary)

| Concern | Choice |
|---------|--------|
| Slots | `base` + `masked` + up to 2 extras by rank |
| PNG | **64×64 only**; MineSkin v2 sign |
| Apply | Join, character switch and a 45s refresh while online; `/rpcharacter wardrobe` in-game |
| Web | Standing frames; modal preview. New uploads can be equipped and edited at once; a **Syncing** chip shows until RPCharacters applies them |
| Profile | The list's portraits come from `GET /characters/{id}/face` and the character view's 16×32 front view from `GET /characters/{id}/figure` (arms follow the slot's saved model). `GET /profile` gives each living or pending character `worn_skin`, the worn slot's name or null, shown on the Wardrobe link. All three read the worn slot without enforcing slot limits; `GET /characters/{id}/wardrobe` does enforce them, deleting skins in locked slots, so Profile never calls it |

Separate from item skins and RP identity masks.

## Architecture

```mermaid
flowchart LR
  subgraph mc [Minecraft]
    TW[TFMCWeb]
    RPC[RPCharacters]
    TW -->|mint profile code| API
    RPC -->|PUT catalog + kits| API
    RPC -->|pull / apply creates| API
  end
  subgraph web [ProvinceSystem]
    API[Characters + kits + sessions]
    FE["/profile, /character"]
    FE -->|Bearer session| API
  end
  Player -->|/token create profile| TW
  Player -->|redeem| FE
```

## Out of scope

- Website passwords / OAuth
- Rewriting non-attribute selection stages into sheets (unless redesigned later)

Operator checklist: [STAGING.md](../../STAGING.md).
