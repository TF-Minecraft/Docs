# Cooking — Animal husbandry

Livestock lives inside **Cooking**, not a second plugin.

Keep this guide aligned with the implementation and configuration on `main`.

## Responsibilities

| Stat | What it is | What it is not |
|------|------------|----------------|
| **Genetics** | 0-1k, from breeding (wild roll up to `initial-genetic-max`). Mount health/speed/jump use genetics and care. An animal's stored genes do not drift from its own care. Parent **care** and the **stars of the breeding food** scale the offspring gene bonus. | Not a food-quality field on the animal. Universal feed does not reduce the bonus. |
| **Care** | 0-200. Loaded happy time raises it. Neglect lowers it. Neglected parents produce weaker babies. | Does not rewrite this animal's genes. Does not pick star quality. |
| **Hungry / Dirty** | Negative states. Stop care-up. After grace, cause decay. Block breeding. | Not friendship. Not “slept outside.” |
| **Yield** | `care / care-max` (default care/200). Multiplies **amount** (roast cuts, wool count). | Does not change star quality. |
| **Stars** | Cooking `food_quality` 1–5 from **raw genetics** via a YAML table. | Not averaged with care. |

**Effective genetics (amounts only):** `genetics * (care / care-max)`. Care 0 → 0% amount (honour `min-roast-cuts`). Care 100 / 200 → 50%. Care 200 → 100%. Roast amount is meat portions before the bone. Poultry never goes below two legs and one filet (`min-food-cuts` on the poultry sequence).

**Breeding roll:** parent average + variance + slowdown at high parent genetics, scaled to **0-1k** (`max-genetics: 1000`). Variance base is `max/10`, min variance is `max/100`. Defaults: `genetic-variance-multiplier` `0.2`, `genetic-slowdown-divisor` `0.6`. Parent **care** scales the bonus (`care-influence`, default `0.02`).

## Persistence

**SQLite is the source of truth.** Main thread only. WAL mode with FULL synchronous ownership commits. Write on ownership change, tick flush, death, chunk unload, plugin disable.

Entity **PDC is persistent** in Paper (saved with the entity on unload). We still do **not** treat PDC as the database. Genetics, owners, care, states, and cooldowns live in SQLite.

Never delete an **owned** animal row because the entity is unloaded. Unloaded ≠ dead. Unowned listed types **are** deleted on chunk **load** (explicit despawn), including any orphan UNTAMED row.

Owned/managed entities must `setPersistent(true)` and `setRemoveWhenFarAway(false)`.

### SQLite schema

`animals`

- `uuid` PK
- `type`, `name`
- `genetics`, `care`
- `stats_revision` (text; null on old rows)
- `hungry_since`, `dirty_since` (epoch millis, null if clear)
- `last_processed_at`
- `unloaded_at` (set on unload / disable; null while loaded)
- `affliction_elapsed` (loaded hours toward next state)
- `affliction_at` (this cycle’s threshold, hours)
- `last_milk_at`, `wool_ready_at`, `shed_ready_at`, `egg_ready_at`
- `mature_at` (baby growth; null = adult)
- `neutered`
- `world`, `x`, `y`, `z` (last block the animal was seen at; null until it loads once)

`character_owners`

- `animal_uuid`, `account_uuid`, `character_uuid`, `role` (`owner` / `coowner`)
- primary key `(animal_uuid, character_uuid)`; several characters on one account may co-own the same animal
- capacity counts distinct animal UUIDs per account, including unresolved legacy slots

`owners` remains the legacy account table. Its resolved rows never grant gameplay rights.
`husbandry_owner_archive` is an immutable SQLite copy of every legacy owner column,
without cascading foreign keys. `husbandry_owner_plan` records the fixed reviewed
character or a held reason for each original account slot; `husbandry_owner_meta`
records completion. Character ownership uses its own expansion tables, separately
from `PRAGMA user_version`.

### Entity PDC flags

Stored on the entity, not in SQLite:

- `managed` - husbandry entity; used with chunk-load wipe logic
- `tame_name`, `linked_animal` - tame and co-own item state

### Database migrations

Migrations run once when the plugin opens `husbandry.db` (`PRAGMA user_version`). They do **not** re-run on `/cooking reload` (the DB connection stays open).

| `user_version` | Change |
|----------------|--------|
| 0 → 2 | Existing `genetics` divided by 10, capped at 1000 |
| 2 → 3 | Add `mature_at` column (null on existing rows = adult) |
| 3 → 4 | Add `shed_ready_at` column |
| 4 → 5 | Add `egg_ready_at` column |
| 5 → 6 | Add `care_up_remainder` and `care_down_remainder` |
| 6 → 7 | Add `stats_revision` |
| 7 → 8 | Add `world`, `x`, `y`, `z` (null on existing rows until the animal next loads) |

### Stats revision

YAML `stats-revision` (string, default `"1"`). Blank skips the wipe. On plugin enable (after the DB opens) and on `/cooking reload`, every row whose `stats_revision` is null, blank, or not equal to the config id is reset: wild genetics (`0 … initial-genetic-max`), care 0, care remainders 0, then stamp the current id. Keep owners, name, state, neuter, `mature_at`, harvest timers, hungry/dirty, and last location. New tame/breed/spawn rows stamp the current id. Bump the id in config when gene rules change so live stock is wild-reset.

Bred-but-not-tamed animals get an UNTAMED row in the **same loaded visit** so tame uses parent genetics. They are **not** protected across chunk load: no owner → despawn.

Tame on a world / spawn-egg animal with **no row** inserts one (wild genetics `0 … initial-genetic-max`, care 0) then claims. Admin `/cooking husbandry spawn` is optional (staff genetics/care); it is not required to tame.

On death: delete animal + owner rows. Unowned listed types drop nothing.

Persist `name` in SQLite and `setCustomName` on the entity.

## Lifecycle and timing

Care simulation runs on chunk load (`HusbandrySimulator.catchUp`) and on a **1-minute tick** while the entity chunk is loaded. Egg and shed harvest run on the **1-minute tick only** (not on chunk load). Maturity is applied on load and on tick.

On chunk unload (or plugin disable), `unloaded_at` is stamped and the row is upserted. Simulation does **not** advance into the future while unloaded.

```
elapsed = now - last_processed_at
unloaded = (unloaded_at != null) ? min(elapsed, now - unloaded_at) : 0
loaded_part = elapsed - unloaded
```

**Care simulation order** (same on load catch-up and tick):

1. **Decay first, full elapsed, no cap.** If Hungry and/or Dirty already existed: after `min(since) + decay-grace`, apply `floor(decay_seconds / care.down.interval) × care.down.amount` care loss. Keep original `*_since`.
2. **Unloaded care gain** only if they were happy at unload: cap elapsed by `offline-care`, then `floor(capped_seconds / care.up.interval) × care.up.amount`. If they already had a negative, **zero** unloaded gain.
3. **Long-unload force** if `unloaded > long-unload-force`: if still no negatives, apply Hungry or Dirty 50/50 with `since = now` (grace starts on return). If they already had one, add the **other**. Do not move the old `since`. Reset affliction cycle after a force.
4. **Loaded affliction.** Only `loaded_part` (and live ticks, after `min-loaded`) add to `affliction_elapsed`. When `>= affliction_at`, apply a missing state (50/50 if neither, else the missing one). If both set, skip. Reroll `affliction_at` in `[affliction.min, affliction.max]` (default 4h–8h, mean 6h). After both states are cleared by the player, roll a new cycle so they are not instantly re-dirtied.
5. **Loaded care gain** while happy: `floor(loaded_seconds / care.up.interval) × care.up.amount`, no cap.
6. Set `last_processed_at = now`. While loaded, `unloaded_at = null`. On unload/disable, set `unloaded_at = now`.

**Tick task** (every ~1 minute, loaded animals only): after `min-loaded` visit time, run care simulation; apply maturity; run shed and egg harvest if gates pass; sync state displays; upsert row.

Chunk loaders / another player at the pen = **loaded**. The 6h affliction loop is the anti-AFK.

## Ownership

- Ownership belongs to the selected character. Another character on the same account has no owner/co-owner rights.
- `max-animals` default **15** stays account-wide. Count each distinct animal once per account across every character and held legacy slot. Co-ownership counts toward each owning account; a second character's slot on the same animal does not consume another place.
- Reject voluntary tame/co-own acquisitions at cap (`cooking.admin` bypasses cap). Inheritance keeps every animal, including overflow; overflow prevents further acquisitions.
- A resolved co-owner retains access when another legacy owner slot is held. Held slots prevent unowned claims and bearer-token self-claims. Staff can inspect `husbandry_owner_plan`; unknown roles or identities remain held.
- Tame/co-own actions require an exact current character session belonging to that account; stale or misrouted provider sessions are refused. Native vanilla taming, sitting and tameable inventory interactions do not override existing Cooking ownership.
- Chickens and llamas count. Bees are **vanilla** (not in the 15, not wiped).
- Tameable vanilla types (horses, etc.) must be vanilla-tamed before plugin-own.
- Tame token (anvil-named) claims the animal. No SQLite row yet: insert then claim. Existing UNTAMED row: keep genetics, then claim. Token name is applied only after a successful claim. First tame plays spore blossom particles and the enchantment-table sound; renames are silent.
- Feed and glove require ownership (or staff).
- Items: TLibs paths in `husbandry.yml` (glove, universal feed, tame, co-own). Not MMOItems.

## Character migration and estates

Cooking pins TLibs **2.6.0**. Identity-dependent ownership fails closed without a
ready character. New heir/estate entry points are capability-probed before their
bridge classes load: an older provider retains legacy slots or dead characters'
property instead of guessing a current character.

The boot task waits for `Characters.legacyHeirsReady()` and retries pending
migration every minute. Identical pending warnings are suppressed; after
publication, immutable held plans are checked and reported hourly.
Each original account slot maps only through its reviewed `legacyHeir`; a dead
reviewed heir remains the migration recipient. One SQLite transaction copies all
legacy owner columns into the immutable archive, verifies its count, writes the
fixed plan, inserts resolved character slots and writes completion. The archive
includes committed WAL content through SQLite itself and cannot cascade away
when an animal dies. TLibs **2.6.1** rolls back the archive, plan and ownership
publication together on any transaction body failure, including a JVM `Error`.
An uncertain rollback discards the connection; a clean server restart reopens
husbandry storage.
Verify that TLibs 2.6.1 is loaded before running ownership migrations; Cooking's
compilation pin remains 2.6.0, with the same public API. Under TLibs **2.6.0 and
earlier**, a JVM `Error` inside the transaction can commit partial rows instead.
An unfinished migration written under those providers still requires staff repair
using the preserved archive and legacy rows; upgrading TLibs does not repair it.
Missing heirs, malformed identities, unknown roles and
conflicting slots remain recorded for staff; another character never claims them
by opening a menu. Animal rows, snapshots, care, genes, timers and unknown columns
are retained. Normal animal updates patch known fields rather than rebuilding rows.

The `cooking-animals` estate participant moves only the deceased character's slot
to the decided property recipient. WAITING/FROZEN slots stay with the testator;
other co-owners keep their own rights. A recipient already sharing the animal
merges to one slot, retaining the stronger recognized role (`owner` over
`coowner`). Unknown/conflicting role metadata blocks settlement for staff.
Capacity does not reject inheritance. No animals are copied or respawned by an
ownership transfer.

All slots, recipient merges and receipts for one estate revision commit in one
SQLite transaction. `husbandry_estate_intents` records the full decision identity,
revision and from/to refs; `husbandry_estate_slots` records IDs and before/after
roles. The decision text is Cooking's fixed rendering of all twelve TLibs 2.6.0 fields,
independent of runtime record text. Future fields require an explicit versioned
encoding upgrade that continues validating these captured receipts; unknown
recipient kinds block without writing ownership or receipt rows.

Exact `Estates.guardHolds` checks before mutation and before commit reject
revival, re-death, changed recipients and newer revisions. Repeated settlement
reports the cumulative moved IDs without moving them again, including later WAITING/FROZEN revisions. Raw source/recipient
rows, including unknown nullable or BLOB fields, remain in
`husbandry_estate_owner_archive` independently of the live slot's deletion.

If a previously transferred animal reappears in the testator's owner rows while
its completed receipt remains, settlement is BLOCKED across all revisions.
Preserve both rows and receipts for staff reconciliation. A completed revision
with newly resolved, untouched testator holdings also blocks that revision;
a reviewed new revision may transfer those untouched holdings. Receipt account
and character references must agree with the recorded decision.
Completed IDs must also agree with the preserved source archive for that
death/revision; missing or changed receipt IDs cannot authorize another transfer.

TLibs **2.6.1** rolls back transaction body failures, including a JVM `Error`;
process interruption rolls back uncommitted SQLite work. An uncertain rollback
also requires a clean server restart. Under TLibs **2.6.0 and earlier**,
a JVM `Error` can leave partial estate rows; upgrading the provider does not
repair those existing rows.
A retained incomplete intent
or conflicting same-revision receipt is BLOCKED for review; affected ownership
writers refuse changes while resolved co-owners can still care for or ride their
animal. Transient database failures report RETRY. Use the estate staff retry/waive
workflow after resolving the recorded cause; never clear a held intent merely to
force another recipient. Reconciliation runs at boot and hourly, independently
per death/revision.

Ownership and token use are sequential checked operations, not one transaction
with Minecraft inventory or entity saves. An arbitrary crash after a slot commit
and before token consumption is not proved exactly-once; preserve the database
and player body for staff reconciliation rather than blindly repeating effects.
Public milk/shear/egg/shed harvesting and existing animal care clocks retain their
rules.

### Offline rollback

Stop the Minecraft application through its normal deployment procedure before
using these commands. From the Cooking checkout, preview against the plugin's
`Data/husbandry.db`:

```sh
python3 tools/husbandry-ownership-rollback.py /path/to/plugins/Cooking/Data/husbandry.db
```

The JSON preview reports archived/restorable slots, held slots, current character
slots and changed resolved slots. Review ownership grants, removals and estates
since migration. To restore the original account slots for an old Cooking JAR:

```sh
python3 tools/husbandry-ownership-rollback.py /path/to/plugins/Cooking/Data/husbandry.db --apply --backup /path/to/husbandry-before-rollback.db
```

The tool creates its new recovery file exclusively with mode `0600`, refuses to
overwrite a backup, makes a verified SQLite backup including
committed WAL pages, and restores only archived account slots whose animal still
exists. It never resurrects a deleted animal. Current animal progress/snapshots
and the character tables/journals remain preserved; old Cooking ignores the
character tables. Account authority after rollback discards post-migration
character grants/removals/estate transfers from gameplay, so reconcile those
changes using the recovery image before proceeding. Keep that image and do not
re-upgrade after old-version ownership writes without reviewing both sets.
Deleting expansion tables or immutable archives is a separate later migration.

### Verification

Run Java 21 `tfmc-mvn -o -B clean verify` from the Cooking worktree. The zero-missed
production-line gate covers two characters on one account, stale menus, session
end/start mounts, held co-owners/token refusal, account capacity, immutable archive
and unknown-column preservation, injected SQLite publication faults, estate role
merges, replay and strict revival/re-death/revision guards. SQLite rollback tests
use isolated databases; they do not touch a running server.

Native Paper testing must additionally exercise an owned horse: mount as A,
end A's already-noncurrent session, verify dismount, start B on the same account,
verify B cannot remount, then return to A. Include missing identity and held legacy
ownership while preserving ordinary unowned riding. A controlled identity-provider
fixture proves the husbandry hooks on real Paper; it does not prove RPCharacters'
complete select-screen/body flow or arbitrary-crash inventory delivery.

## Care and states

Happy = no Hungry and no Dirty.

Feed (universal feed) clears Hungry (consumes 1). Glove clears Dirty (not consumed). Clearing a state does **not** add care; it only allows care-up again once both are gone.

Entity name tag while afflicted: `{name} (Hungry)`, `(Dirty)`, or `(Hungry, Dirty)` — always visible. When happy, only the base name is set and the tag is hidden (hover only). Base name stays in SQLite; suffix is applied at sync time. Legacy TextDisplay passengers are removed on sync. Neuter (`m.pets.neutering_item`) costs 1 durability per use (one item if it has no durability). Feed/glove play firework sparkle particles and a pickup sound.

### Two clocks

Owner online/offline does not matter. What matters is whether the **entity chunk is loaded**.

| | Chunk loaded | Chunk unloaded |
|---|---|---|
| Care up | +`care.up.amount` every `care.up.interval` (default +1 / 1m) while happy, **no cap** | At most `offline-care` (default 8h), then stop |
| New Hungry/Dirty | Mean every `affliction.mean` (default 6h) of **loaded** time | Frozen, except unload **> `long-unload-force`** (default 8h) forces a state on next load |
| Decay | After `decay-grace` (24h) with a negative, −`care.down.amount` every `care.down.interval` | **Same wall-clock.** Catch-up can dump care to 0 |

### Anti-game (locked)

- You cannot max care in spawn: unload > 8h → care gain stops after `offline-care` and you come back Hungry or Dirty.
- You cannot max care AFK at the pen: ~6h later a state appears, gain stops, then decay after 24h.
- You cannot freeze decay by unloading: decay uses wall-clock from original `*_since`.
- Pulse-loading (touch the chunk for one tick): `loaded_part` under `min-loaded` (default 60s) counts as **still unloaded**. Care-up and affliction elapsed only apply after the animal has been loaded for that long this visit.

## Breeding

- Child genes from parent average plus a random bonus. Parent care and breeding-food stars scale that bonus:

```
avg = (mother + father) / 2
boost = (int)(bonus * careRatio) + careExtra
feedScale = average of the two parents' feed scales
child = clamp(avg + (int)(boost * feedScale), 0, maxGenetics)
```

  `careRatio` is average parent care / `care-max`. Care 0: child stays at the average (no climb). Care max: full bump plus `care-influence * maxGenetics` (default +20 at cap 1000). Baby's own care is 0 at birth.
  Each feed scale is `stars / 5`. 5★ is `1` and matches the roll from before feed quality applied. 1★ keeps one fifth of `boost`. The two parents are averaged, so 1★ wheat and 5★ wheat (or universal feed) is a 3★ scale. Universal feed (`items.feed`) and any item with no cooking `food_quality` always use scale `1`. Stars are read from the item in hand when each parent enters love mode.
- Cancel if either parent is Hungry, Dirty, neutered, or **still growing up**. Hungry/dirty block breed; they do not replace the care ratio.
- Offspring get an UNTAMED SQLite row with rolled genetics for **same-session** tame. If the chunk unloads/loads before anyone owns them, they despawn and the row is deleted.
- **Baby growth:** global `grow-up` (default `1h`); optional per-species override (e.g. `CHICKEN: 45m`). Stored as `mature_at` in SQLite; `NULL` = adult. Immature animals can be tamed but cannot breed, milk, shear, lay eggs, or drop Cooking roast on death. While `mature_at` is still in the future, the entity stays on the baby model with its age locked, so vanilla growth and breeding food cannot switch it to the adult model early. When maturity is reached, the lock is cleared and the entity is set adult if loaded.
- Neutering: all husbandry species, owner (or staff). Neutered animals cannot breed.

## Harvest

No custom slaughter tool. If an **owned** animal **dies**, it drops configured Cooking goods. Killer does not matter (subject to damage config). Listed types with **no owner** drop nothing (no vanilla loot, no XP, no Cooking roast).

| Action | Rule |
|--------|------|
| Death | Owned mature: Cooking roast from `slaughter.meat` + extras from `slaughter.drops`. Immature: no Cooking roast or extras. Unowned `remove-unowned` types: no drops. |
| Quality (stars) | From **raw genetics** via YAML table → 1–5. Apply with `ItemBuilder` / existing quality PDC. Stars gate drop tiers: common always, rare 3★+, epic 4★+, legendary 5★ only. |
| Amount | From **effective genetics** (care yield). That many meat cuts from the start of the carve sequence, then the bone. The roast model starts whole (stage 1) and moves toward the bone stage as those cuts are taken. Poultry floor is two legs and one filet, then bone. Other roasts floor at one meat cut, then bone. Counted drop tables use hide/wool yield. Honour `min-roast-cuts` and the sequence `min-food-cuts`. |
| Sheep | Vanilla wool **always** on shear. If `wool_ready_at <= now`, also roll `shear.drops`, then reset the wool timer. |
| Milk | `milk: true` on the species. Per-animal cooldown (`milk-timer`, default 20m). Mature only. Empty bucket interact; hand becomes cooking `milk_bucket` with quality from the **animal** (Cow/Goat origin from entity type). |
| Eggs | Chickens with `egg:` set: when loaded, mature, and happy, drop one egg after `egg-timer` (default 1h) on the 1-minute tick. Item from `egg` (`vanilla` → `Material.EGG`; `food(...)` or TLibs path otherwise). The chicken config uses `food(type=egg;...)`, so the drop is a raw cooking egg whose stars come from that chicken's genetics. It is not edible until fried. Vanilla egg drops from managed chickens are cancelled (`EntityDropItemEvent`), including the blue and brown eggs laid by cold and warm variants. Unmanaged chickens keep vanilla eggs; `conversions.yml` maps `v.egg`, `v.blue_egg`, and `v.brown_egg` to the same raw cooking egg on pickup. Cooking only writes `conversions.yml` when it is missing, so existing installs must add the `v.blue_egg` and `v.brown_egg` lines by hand. Bees: vanilla, not husbandry. |
| Shed | Species with `shed.drops`: when loaded, mature, and happy, roll `shed-chance` after `shed-timer` (default 4h) on the 1-minute tick. Success rolls `shed.drops` at the animal's feet and resets the timer. |

Genetics → stars **and** amount tables both live in YAML (`husbandry.yml`). Do not hardcode thresholds.

`MilkBucketConverter` must not ignore the cow when the fill is from a husbandry animal.

## World cleanup

On chunk **load**, for each entity type in `remove-unowned` (cows, pigs, sheep, chickens, goats, horses, camels, llamas, … — **not bees**): if there is **no owner**, `remove()` and delete any orphan SQLite row — **except** horse/donkey/mule/camel that already have a SQLite row (first-interact enroll; they stay unowned until tamed). Spawn-egg and natural animals can be tamed only while that chunk stays loaded, unless they were enrolled.

Never delete a row on unload just because `Bukkit.getEntity` is null. Unowned wipe on load is an explicit despawn.

### Lost animals

A forced stop can kill the server before it saves chunks, so an owned animal that moved since the last save can be missing from every saved chunk. Cooking guards against this with snapshots:

- Every minute, on chunk unload and on disable, each loaded **owned** animal is serialized into the `snapshots` table (one row per animal, cascading from `animals`).
- At start, after the saved-chunk scan, an owned animal found in no saved chunk of its world and under no logged-out rider (`playerdata` `RootVehicle` of `<uuid>.dat` files) is lost. If it has a snapshot, Cooking spawns it again at the captured position with its UUID, name, coat, gear, owners and stats, and logs `Restored lost animal …`. If the entity turns up with its chunk first, nothing is spawned. If the spawn is refused, it stays `Missing` and is retried at the next start.
- Without a snapshot, the row and owners are deleted and `Dropped ghost animal …` is logged. An incomplete estate intent prevents ghost deletion: the record stays `Missing` for staff review, retaining existing animal, owner and snapshot rows and account capacity. The scan continues with other animals and counts these records as held.
- A scan that could not read some chunk or player file restores and drops nothing. Its lost animals show `Missing`, the summary line ends `kept N missing animals because some files could not be read`, and a warning names the first 10 unreadable files or chunks with the reason. Only `<uuid>.dat` player files are read: the `<uuid>-<number>.dat` temp file a crash mid-save leaves behind, `.dat_old` backups and `_corrupted_` copies are skipped.
- Death deletes the snapshot with the row. Any other removal except a chunk unload or a rider logging out (plugin removal, discard) deletes the snapshot too, so a deliberately removed animal is not brought back.
- `restore-lost-animals: false` turns restoring off; lost animals are then dropped as ghosts.

## Mounts

Mount types in code: all `AbstractHorse` (horse, donkey, mule, camel, llama). Attributes use Paper names (`MAX_HEALTH`, `MOVEMENT_SPEED`, jump strength API).

**Configured in `husbandry.yml` `mounts:` today:** HORSE, DONKEY, MULE, CAMEL. **LLAMA has no stat block yet** - enroll and genetics-to-stats fall back to no override until `mounts.LLAMA` is added.

- Per-type min/max health, speed, jump in YAML
- Wild/spawn-egg mounts keep vanilla stats until first interact, tame, or inspect enrolls a row (`0 … initial-genetic-max`, care 0)
- Health, speed, and jump are then written from genetics and care: `max * (min-pct + genetics-pct * genetics/max-genetics + care-pct * care/care-max)`, floored at the type min
- Bred foals roll genetics from parents, then the same formula is applied one tick after birth (vanilla breed stats are overwritten)
- The current owner/co-owner character (or staff) may ride owned mounts. Unowned mounts stay rideable with a ready character session. Missing records or identity refuse mounting. Session end dismounts the outgoing body before the next character starts; session start also rejects any retained unauthorized mount.

## Damage

```yaml
damage:
  other-players: true    # anyone can hurt/kill; death still drops goods
  owner: true
  mobs: true
  environment: true      # fall, fire, cactus, drowning, cramming, etc.
```

Applies to entities with a SQLite row. If `other-players` is false, cancel player melee/projectiles unless the attacker is an owner/co-owner (or staff).

## GUI

Sneak empty-hand (or configured `items.inspect` TLibs path; blank = sneak-only) on a managed animal, including mounts.

**54-slot** double-chest inventory for all animals (livestock and mounts). The menu
captures the opening character session; a stale remove-ownership click closes the
menu without changing a slot. Owner labels use character names, with an explicit
staff-review label for held slots.

Layout uses **gray/green concrete bars** (5 centered segments each). One empty row separates the two bars. Each segment shows title (`Care` / `Genetics`) and current/max only.

- **Row 1 (header):** status, neutered, owners, **products** (slot 3, if the species has harvest), name, remove-ownership (slot 8, owners only)
- **Row 2:** empty
- **Row 3:** **Care bar** (slots 20–24): fill = `care / care-max`; lore is `care/care-max`
- **Row 4:** empty separator
- **Row 5:** **Genetics bar** (slots 38–42): fill = `genetics / max-genetics`; lore is `genetics/max-genetics`
- **Row 6 (mounts only):** health, speed, jump (slots 46, 49, 52)

**Products** (chest, slot 3) only if the species has `slaughter`, `shear`, `shed`, `milk: true`, or `egg`. Lore is `Yield X%` then mode lines (`On slaughter`, `Shear`, `Shed`, `Milk`, `Eggs`) - no stars or amounts. Pets with no harvest config have no icon.

**Yield X%** is `round(100 × effectiveGenetics / max-genetics)` where `effectiveGenetics = floor(genetics × care / care-max)`.

Horse, donkey, and mule slaughter extras are counted leather (same table as cow). Camel is roast only (no extra drop table).

Also shows: status (Happy / Hungry+Dirty + decay line), neutered, owners, growing-up timer on babies, mount stats when relevant, remove-ownership for owners.

Stars are **not** shown in the GUI (visible on slaughter quality instead). No affliction/chore timer item.

## Commands

Players (no permission node):

- `/animals` (alias `/livestock`) — list every animal the selected character owns or co-owns. Each line is name, species, co-owner when shared, growing when immature, Happy / Hungry / Dirty, then the world and block coordinates last recorded for that animal. Click the coordinates to copy them. Animals in unloaded chunks are listed too. When the server starts, Cooking reads the saved entity chunks to fill in or correct where each unloaded animal is. An owned animal lost from the save is restored or dropped at that scan (see [Lost animals](#lost-animals)). One that could not be restored, or that a scan could not confirm because some files were unreadable, shows `Missing` (with `last seen` coordinates if any were recorded) until it loads again. `location not recorded yet` only appears when neither a recorded spot nor a saved chunk is available, for example when some chunks could not be read. The header counts the selected character's animals; a separate `Account animal places: used/max` line shows capacity across all its characters and held slots.

Staff with `cooking.admin`, including the console, can run `/animals <player>` for someone who has joined. This read-only account view aggregates distinct animals across that account's resolved character slots. A player without that permission cannot list another player's animals.

Staff target completion includes online players and known offline names still in
Bukkit's cache. Saved names load at registration and update on joins; expired
cache names are omitted. Husbandry numeric presets match the current prefix.

The last location is written when the animal loads, on the one-minute tick while loaded, on unload, and on plugin disable if the entity is still present. Listing refreshes a loaded animal from the live entity before printing.

Requires `cooking.admin`:

- `/cooking husbandry spawn <type> [genetics] [care]` — spawn untamed animal with SQLite row
- `/cooking husbandry save` — upsert all currently loaded animals and checkpoint WAL

Reload config (including `husbandry.yml`) via `/cooking reload`. This reloads YAML only; it does **not** reopen the SQLite database.

Unowned admin-spawned livestock still despawn on chunk load until tamed. Enrolled or spawned horse/donkey/mule/camel keep their SQLite row without an owner.

## Architecture

Package: `net.tfminecraft.cooking.husbandry`. Config: `husbandry.yml`. Items via TLibs paths in that file.

No async entity or SQLite access. All husbandry logic runs on the main thread.

| Area | Primary classes |
|------|-----------------|
| DB | `HusbandryRepository`, `HusbandryAnimal` |
| Lifecycle | `HusbandryLifecycleListener`, `HusbandryTickTask` |
| Care | `HusbandrySimulator`, `HusbandryCareListener`, `HusbandryStateDisplay` (entity name + visibility sync) |
| Ownership | `HusbandryOwnershipService`, `HusbandryTamingListener`, `HusbandryAnimalsCommand`, `HusbandryRoster` |
| Location | `HusbandryLocation` (last block, stored on the animal row) |
| Breed / growth | `HusbandryBreedListener`, `HusbandryNeuterListener`, `HusbandryGrowth`, `HusbandryGenetics` |
| Harvest | `HusbandryDeathListener`, `HusbandryHarvestListener`, `HusbandryHarvest`, `HusbandryShed`, `HusbandryEggs`, `HusbandryDropRoller` |
| Mounts / damage | `HusbandryMounts`, `HusbandryMountListener`, `HusbandryDamageListener` |
| GUI | `HusbandryInspectGui`, `HusbandryInspectListener`, `HusbandryGuiBars` |

## Configuration

Global defaults in `husbandry.yml`:

```yaml
max-animals: 15
care-max: 200

min-loaded: 60s
decay-grace: 24h
offline-care: 8h
long-unload-force: 8h
milk-timer: 20m
wool-timer: 4h
shed-timer: 4h
shed-chance: 0.15
egg-timer: 1h

affliction:
  mean: 6h
  min: 4h
  max: 8h

care:
  up:
    interval: 1m
    amount: 1
  down:
    interval: 10h
    amount: 1

grow-up: 1h

items:
  tame: m.pets.taming_item
  co-own: m.pets.coownership_item
  feed: m.pets.universal_feed
  glove: m.pets.caring_item
  neuter: m.pets.neutering_item
  inspect: ""
  mount-stats: ""

initial-genetic-max: 20
max-genetics: 1000
min-roast-cuts: 1
stats-revision: "1"
restore-lost-animals: true

breeding:
  genetic-variance-multiplier: 0.2
  genetic-slowdown-divisor: 0.6
  care-influence: 0.02

# Per-species grow-up override example:
# species:
#   CHICKEN:
#     grow-up: 45m
```

Durations use TLibs strings (`8h`, `20m`, `60s`). Legacy `*-hours` / `*-minutes` / `care-*-per-hour` keys still load with a one-time warning.

### Per-species keys

Under `species.<TYPE>` (presence defines capability; no `harvest` list):

| Key | Purpose |
|-----|---------|
| `milk` | `true` enables bucket milking (quality from animal; Cow/Goat origin) |
| `slaughter.meat` | `food(...)` roast string for death drop |
| `slaughter.drops` | Star-gated extras on slaughter (`common`, `rare`, `epic`, `legendary`; optional `mode: counted`) |
| `shear.drops` | Star-gated items given on shear (after wool timer) |
| `shed.drops` | Star-gated items dropped on successful shed tick |
| `egg` | `vanilla`, `food(...)`, or TLibs path for timed egg lay. Chickens use `food(type=egg;origin=Egg;tags=freshness.0:cooked.0)` so quality follows the chicken's genetics |
| `grow-up` | Optional per-species baby duration override |
| `wool-timer` | Optional per-species shear cooldown override |

Also configured: `remove-unowned` (wipe list), `quality-from-genetics`, `amount-from-genetics`, `breeding.*`, `damage.*`, `mounts.*`.
