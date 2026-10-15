# GeigerCounter

**A Minecraft server plugin that turns exploration into a treasure hunt — track a hidden radioactive source by particle signal and claim tiered loot.**

![Java](https://img.shields.io/badge/Java-21-orange?logo=openjdk&logoColor=white)
![Paper](https://img.shields.io/badge/Paper-1.21.10-blue)
![Maven](https://img.shields.io/badge/Build-Maven-red?logo=apachemaven&logoColor=white)

Built for the [TFMC](https://www.patreon.com/c/TFMCRP) roleplay server, where each character hunts their own source near them.

---

## What It Does

Hold a **Geiger Counter** item and the world starts talking back. Each character has their own hidden radioactive source, placed 150–500 blocks from where they first hold a live counter. A signal bar at the top of the screen fills as they close in and peaks when they face the source, while particle rings and clicks track the distance. Walk it down, collect the source, and a weighted loot table decides the prize, anywhere from common food to mythical skin scrolls. The counter burns out, and the next live counter places a new source near wherever the character is then.

| | |
|---|---|
| **A source per character** | Each character hunts their own source near them; RPCharacters supplies the character, and without it each account has one |
| **Signal bar** | A boss bar that fills with closeness and peaks when the player faces the source, so turning on the spot shows the way |
| **Signal tracking** | Particle rings guide players toward their source — more rings and brighter colors mean closer |
| **Tiered rewards** | 6 rarity levels (Common → Mythical) with fully weighted drop chances |
| **Self-resetting hunt** | After a collection the next live counter places a new source near the character |
| **Consumable gameplay** | The Geiger Counter "runs out of charge" on success, becoming a **Dead Geiger Counter** |
| **Geiger clicking** | The counter clicks faster the closer the source gets — audible signal, not just visual |
| **Per-player drop limits** | A player may claim at most *x* drops per *y* time window, so loot stays scarce |
| **Config-driven design** | Search area, detection ranges, particle colors, and reward pools all live in `config.yml` |

## How It Works

A repeating task checks every online player in the source world. For each player holding a Geiger Counter while playing a character:

1. If the character has no source, one is placed at a random spot between `source.min-distance` and `source.max-distance` from them, inside the configured area and passing the spawn filters. The same happens when the character is more than `source.reroll-distance` from their source, for example after travelling or teleporting away. A character so far outside the area that no part of that ring lies inside it gets no new source and keeps any old one.
2. The horizontal distance to the source is calculated (Y is ignored, so the signal works across terrain height).
3. That distance is mapped to a particle configuration — ring count (1–3) from distance thresholds, and a color interpolated along a two-stage gradient (dark purple → purple far away, purple → white up close).
4. The rings spawn around the player, and the signal bar is updated.
5. Within collection distance (20 blocks by default), the source is collected automatically: a tier is rolled by weight, a random item from that tier is granted, and the counter is swapped for its dead version. The character has no source until they next hold a live counter.

Sources are stored in `plugins/geiger_counter/sources.yml`, keyed by character ID, so a restart keeps every hunt where it was. A player in the character selection room has no character and gets no reading.

### Signal bar

The bar's fill is closeness times a facing factor. Closeness falls from 1 at the source to 0 at `bar.range` blocks. The facing factor is 1 when the player looks straight at the source and drops to `1 - bar.facing-weight` when they face directly away, so a player can turn on the spot, find the peak and walk that way. Only yaw counts. MMOCore uses the action bar for health and mana, so this is a boss bar at the top of the screen.

### Sound

The counter clicks. Distance controls the click **rate**, not the pitch — that is what a real Geiger–Müller tube does, and it keeps the audio readable as a signal on its own. Clicks are rolled per tick against a probability rather than fired on a fixed interval, so their spacing is irregular the way decay events are; evenly spaced clicks just sound like a metronome.

Default is `block.note_block.hat` at 0.5 clicks/sec on the edge of detection range, ramping to 18/sec at the source. Only the holder hears it. Any sound event ID works — preview them at [minecraftsounds.com](https://minecraftsounds.com).

### Drop limits

`limits` caps how often a single player may claim the source: `drops` collections per `time` window. The window slides — each collection frees up again exactly `time` after it happened, so `drops: 3` with `time: 12h` works out to 6 per day.

Limits count per account, so switching character does not add collections. Collection stamps are stored in `plugins/geiger_counter/drop-limits.yml`, so a restart cannot be used to wipe the limit. A limited player still tracks and sees the signal, but collecting does nothing: the source stays where it is, and the player is told when their next slot opens.

Players with `geiger.limit.bypass` are never limited.

### Commands

| Command | Description |
|---|---|
| `/geiger locate [player]` | Print the source of the player's current character, or your own |
| `/geiger move <player> [x z]` | Clear the source so a new one is placed near them on their next hold, or move it to specific coordinates (coords tab-complete to your position and the area corners) |
| `/geiger limits <player>` | Show the player's remaining drops and time until the next one |
| `/geiger resetlimits <player>` | Clear the player's drop history |
| `/geiger droplist [name]` | Show available lists, or switch and save the active list |
| `/geiger reload` | Reload `config.yml` |

| Permission | Default | Grants |
|---|---|---|
| `geiger.admin` | op | Access to `/geiger` |
| `geiger.limit.bypass` | op | Exemption from the per-player drop limit |

## Architecture

Small, deliberate footprint — each class has one job:

```
src/main/java/net/tfminecraft/geigercounters/
├── geiger_counter.java                # Entry point: wiring, lifecycle
├── config/
│   ├── ConfigMigrator.java            # Adds new keys to existing configs, splits out messages.yml
│   ├── Messages.java                   # messages.yml lookup + placeholder filling
│   └── GeigerConfiguration.java       # config.yml loading: area, ranges, colors, rewards
├── handlers/
│   ├── GeigerClickPlayer.java         # Distance → click rate, rolled per tick
│   ├── ParticleRenderer.java          # Distance → ring count + color gradient rendering
│   ├── SignalBar.java                 # Closeness × facing → boss bar
│   └── SourceHandler.java             # Per-character sources: placement, sources.yml, collection, rewards
├── hooks/
│   └── WorldGuardHook.java            # Optional WorldGuard region lookups
├── managers/
│   ├── GeigerManager.java             # Periodic player checks, component coordination
│   └── DropLimitManager.java          # Per-player drop limits + on-disk history
├── models/
│   ├── TierReward.java                # Reward tier: weight + item pool
│   └── ItemReward.java                # Single reward: item path + amount
├── utils/
│   ├── Hunters.java                   # Player → current character ID (account without RPCharacters)
│   └── Utils.java                     # Shared helpers
└── validators/
    ├── GeigerValidator.java           # Is this item a Geiger Counter? (TLibs paths)
    └── SpawnLocationFilter.java       # Is this a legal spot for the source?
```

```mermaid
classDiagram
    class geiger_counter {
        +onEnable() void
        +onDisable() void
    }

    class GeigerManager {
        +initialize() void
        -checkAllPlayers() void
        -handlePlayerWithGeiger(player, hunter, slot) boolean
    }

    class GeigerConfiguration {
        +load() void
        +getTierRewards() List~TierReward~
    }

    class ParticleRenderer {
        +showParticleEffect(player, distance) void
        -calculateRingCount(distance) int
        -interpolateColor(start, end, progress) int
    }

    class SourceHandler {
        +placeNear(hunter, origin) CompletableFuture
        +tryCollectSource(player, hunter, distance, slot) void
        -giveReward(player) void
    }

    class GeigerValidator {
        +isGeigerCounter(item: ItemStack) boolean
    }

    geiger_counter --> GeigerManager : initializes
    GeigerManager --> GeigerConfiguration : creates
    GeigerManager --> GeigerValidator : creates
    GeigerManager --> ParticleRenderer : creates
    GeigerManager --> SourceHandler : creates
    GeigerConfiguration --> TierReward : contains
    TierReward --> ItemReward : contains
```

### Design decisions

- **Configuration over code** — the entire hunt is data: search area, thresholds, gradient colors, messages, and every reward pool are YAML edits, not releases.
- **One scheduler task, not per-player listeners** — a single periodic check scans players and short-circuits for anyone not holding a counter, keeping the hot path cheap.
- **Abstraction over item plugins** — items and rewards resolve through the TLibs `ItemAPI`, so one config format covers MMOItems, ItemsAdder, and vanilla items with a one-character prefix.

## Installation

1. Drop `geigercounters-<version>.jar` into your server's `plugins/` folder
2. Install **TLibs** (required). **MMOItems** / **ItemsAdder** are optional item sources
3. Restart the server
4. Configure `plugins/geiger_counter/config.yml` and `messages.yml` — sources are placed near each character inside the configured area

### Requirements

| Dependency | Required |
|---|---|
| [Paper](https://papermc.io/) 1.21.10 (TFMC baseline) | Yes |
| Java | See the [shared baseline](../../PLATFORM.md); compiler release is 21 |
| [TLibs](../TLibs/README.md) 2.6.1+ | Yes |
| [RPCharacters](../RPCharacters/README.md) | Optional — without it each account has one source |
| [MMOItems](https://www.spigotmc.org/resources/mmoitems-premium.39267/) | Optional |
| [ItemsAdder](https://itemsadder.com/) | Optional |
| [WorldGuard](https://enginehub.org/worldguard) 7.0+ | Optional — needed only for the region blacklist |

## Usage

1. Obtain a **Geiger Counter** item (via TLibs/MMOItems/ItemsAdder)
2. Hold it — your source is placed 150–500 blocks away, and the signal bar and particle rings appear
3. Turn until the bar peaks, then walk that way; the bar and the rings grow as you close in
4. Get within **20 blocks** (default) to collect the source automatically
5. Receive a reward rolled from the tiered loot pool; the counter becomes a **Dead Geiger Counter**, and your next live counter starts a new hunt near you

### Reading the signal

| Signal | Meaning |
|---|---|
| **3 rings** | Within 100 blocks — very close |
| **2 rings** | Within 300 blocks — close |
| **1 ring** | Beyond 300 blocks — far |
| **White** | Very close (0–200 blocks) |
| **Purple → dark purple** | Far away (200–1000 blocks) |
| **Fuller bar** | Closer, or facing more squarely towards the source |
| **Fast clicking** | Rate rises from 0.5/sec at the edge of range to 18/sec at the source |

## Configuration

```yaml
# Source location settings
source:
  world: world            # World where sources spawn; counters only read here
  top-left:               # Sources stay inside this area, corner 1
    x: -1000.0
    z: -1000.0
  bottom-right:           # Corner 2
    x: 1000.0
    z: 1000.0
  min-distance: 150.0     # New sources sit this far from the character...
  max-distance: 500.0     # ...up to this far
  reroll-distance: 1000.0 # Further than this, the source is placed again near them
  spawn-filters:                    # Where the source may NOT spawn
    max-attempts: 50                # Re-rolls (async chunk loads) before falling back
    reject-liquid: true             # No water / lava / waterlogged ground
    reject-void: true               # No empty columns
    blocked-blocks: []              # Extra banned ground materials, e.g. MAGMA_BLOCK
    min-distance-from-spawn: 250.0  # Horizontal blocks from world spawn (0 = off)
    worldguard:
      enabled: true
      blacklisted-regions: []       # Region IDs the source may not spawn inside

# Detection settings
detection:
  collection-distance: 20.0           # Distance to collect source (blocks)
  max-detection-distance: 1000.0      # Maximum detection range
  close-range-threshold: 200.0        # Distance threshold for color shift
  ring-thresholds:
    three-rings: 100.0    # 3 rings when closer than this
    two-rings: 300.0      # 2 rings when closer than this (else 1)

# Signal bar
bar:
  enabled: true
  range: 750.0            # Distance at which the bar reads empty
  facing-weight: 0.6      # 0 = distance only, 1 = facing only

# Geiger clicking sound
sound:
  enabled: true
  sound: block.note_block.hat   # Any sound event ID
  volume: 0.35
  pitch: 1.7
  pitch-variance: 0.15          # Jitter so repeats do not sound looped
  min-rate: 0.5                 # Clicks/sec at max detection distance
  max-rate: 18.0                # Clicks/sec at the source (20 = one per tick)
  curve: 2.0                    # Higher = ramps up harder near the source

# Per-player drop limits
limits:
  enabled: true
  drops: 3      # Max collections per window
  time: 12h     # Window length - accepts s, m, h, d

# Particle effect colors (RGB: 0-255)
colors:
  close-range:
    start: { red: 255, green: 255, blue: 255 }  # White (closest)
    end: { red: 255, green: 0, blue: 255 }      # Purple (threshold)
  far-range:
    start: { red: 255, green: 0, blue: 255 }    # Purple (threshold)
    end: { red: 17, green: 0, blue: 17 }        # Dark Purple (farthest)

# Reward tiers with weighted chances
drops:
  tier-weights:
    common: 45      # 45%
    uncommon: 30    # 30%
    rare: 15        # 15%
    epic: 7         # 7%
    legendary: 2.5  # 2.5%
    mythical: 0.5   # 0.5%

  active-list: default
  lists:
    default:
      tiers:
        common:
          - "m.FOODS.SAUSAGE:32"
          - "v.raw_iron_block:32"
          - "ia.tfmc:mythril_ingot"
        # ... (see config.yml for full reward lists)

```

Named reward pools live under `drops.lists.<name>.tiers`. `/geiger droplist <name>` saves `drops.active-list` and reloads the configuration.

All chat text lives in a separate **`messages.yml`**, split into what players see and what only `/geiger` operators see:

```yaml
# PLAYER - seen by anyone hunting a source
player:
  found-source: "&#AA00FFYou have found the source of Arcane Radiation!"
  signal-bar: "&#AA00FFArcane signal"
  dead-geiger: "&7Your Arcane Trace Detector has run out of fuel."
  limit-reached: "&cYou have already collected %max% sources in %window%. Try again in %time%."

# ADMIN - only ever seen by whoever runs /geiger
admin:
  usage: "&eUsage: /geiger <locate [player]|move <player> [x z]|...>"
  source-located: "&a%player%'s source is at X = %x% Z = %z% (world: %world%)"
  move-success: "&a%player%'s source moved to X = %x% Z = %z%"
  limits-status: "&a%player% has %remaining%/%max% drops left per %window%."
  # ... 12 more, each documenting its own placeholders
```

Console log lines stay hardcoded in English, so logs and bug reports remain readable whatever this file is translated to.

Upgrading? Messages are migrated automatically — out of `config.yml` and into the `player:`/`admin:` split, customisations preserved. `config-version` in `config.yml` tracks which migrations have run. Version 6 adds the source distances and the `bar` section, and lowers `detection.max-detection-distance` to `source.reroll-distance` if it was higher. Customised messages are kept as they are, so on servers that edited them, `player.found-source` (if it says the source has moved) and `admin.usage`, `source-located`, `move-usage`, `move-invalid-coords` and `move-success` need updating by hand to the new wording and the `%player%` placeholder.

**Item path formats**

| Source | Format | Example |
|---|---|---|
| MMOItems | `m.category.item_id` | `m.FOODS.SAUSAGE` |
| ItemsAdder | `ia.namespace:item_id` | `ia.tfmc:mythril_ingot` |
| Vanilla | `v.material` | `v.raw_iron_block` |

**Reward tiers**

| Tier | Weight | Typical Rewards |
|---|---|---|
| **Common** | 45% | Food, basic materials, raw iron |
| **Uncommon** | 30% | Rare fragments, repair kits, research items |
| **Rare** | 15% | Advanced fragments, medium repair kits |
| **Epic** | 7% | Runestones, trial keys, strong repair kits |
| **Legendary** | 2.5% | Legendary materials, magic repair kits, gemstone pouches |
| **Mythical** | 0.5% | Item skin scrolls, mythical pouches, rare currency |

## Building from Source

```bash
git clone --branch main https://github.com/TF-Minecraft/TLibs.git tlibs
git clone https://github.com/TF-Minecraft/GeigerCounters.git geiger-counters
cd geiger-counters
python3 ../tlibs/tools/install-plugins.py --pom pom.xml --mode pinned
mvn clean verify
```

Use JDK 21, Maven and Python 3. The shared installer verifies the pinned release checksum; see [TLibs dependency setup](../TLibs/README.md). Install the matching `me.plugins:tlibs:2.6.1` artifact as described in the [shared baseline](../../PLATFORM.md), then run `mvn clean verify`. Paper API, WorldGuard API and bStats resolve from Maven; MMOItems is not a direct build dependency. The artifact is written to `target/`.

## Source build metadata

- **Java 21** · **Paper API 1.21.10 (provided)** · **Maven**
- Bukkit event system, scheduler, and YAML configuration API
- TLibs ItemAPI for cross-plugin item resolution

## Author

**Justinas Launikonis** — [GitHub](https://github.com/JustinasLa) · [Support TFMC](https://www.patreon.com/c/TFMCRP)
