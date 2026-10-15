# Behaviour, configuration and operations

[BreedingBuddies documentation](README.md) · [All projects](../../README.md)

Source paths below are relative to
[`src/main/java/net/tfminecraft/breedingbuddies/`](https://github.com/TF-Minecraft/BreedingBuddies/tree/main/src/main/java/net/tfminecraft/breedingbuddies).

## System model

BreedingBuddies keeps a record for each tracked animal: entity UUID, name,
owners, friendship and genetic points, state, today's fed and cared flags, the
last day's stable, water and space results, days out, and the times of the last
bundle collection and last daily update. Apart from its name, the Minecraft
entity carries only the neutered and nerfed flags.

### Farm animal types

An entity type is a farm animal when it is a top-level key in `bundles.yaml`.
The defaults are `HORSE` and `COW`. Only configured farm animals can be tamed.
Types added or removed by `/breedingbuddies reload` take effect at once; known
stored animals retain their ownership guards after a type is removed.

### Ownership and taming

Each owner slot belongs to a character, with its account retained for routing.
Another character on the same account has no care, roster, mount, rename, sharing
or removal rights until explicitly granted its own slot. Tame/share/menu actions
require a current session matching that account. Missing identity, stale sessions
and held animal records refuse actions; staff permission retains its existing
inspection/interaction privileges with a ready session, without a riding bypass.
Known stored animals and specific held records retain interaction and mount
protection if their species is removed from configuration. Unrelated entities
are outside these ownership guards.


1. Rename the taming item in an anvil. The plugin stores the rename text on the
   anvil result; taming needs both that stored text and a display name.
2. Right-click an unowned farm animal with it. Animals that vanilla can tame,
   such as horses, must be tamed in vanilla first.
3. The animal takes the item's display name (hidden name tag), one item is
   used, the player becomes its owner and its state is `HAPPY`.

Using a named taming item on your own animal renames it. Other players are told
they are not the owner.

A new wild animal starts with random genetics below `initialGeneticMax`. Bred,
released and escaped animals keep their recorded genetics; animals made with
`spawnanimal` or `spawnmount` also keep their friendship. Mount genetics are
recalculated from health, speed and jump when tamed (see [Mounts](#mounts)).

### Co-ownership

1. An owner right-clicks their animal with the co-ownership item. This links the
   item to the animal and, for a named animal, sets the lore
   `This token is linked to <name> the <type>.`
2. Then either the owner right-clicks another player with the linked item, or
   whoever holds the linked item right-clicks the air or a block. That player's
   selected character is added as an owner and one item is used. The receiving
   player must have a ready current character.

A linked item works for any holder with a ready character; the player using it
does not need to be an owner. Held legacy slots block bearer-token acquisitions. All owners have the same rights. An owner leaves by opening the animal's
menu and clicking **Remove ownership**. When the last resolved owner leaves and no held slot remains, the animal
becomes `UNOWNED` and anyone with a ready character can tame it again; its genetics are kept and its
friendship restarts at 0.

### Protection

- A player who is not an owner and lacks `breedingbuddies.use` cannot
  right-click an owned animal; every such interaction is cancelled.
- Only owners can ride an owned animal. There is no permission bypass.
- Breeding is cancelled when both parents have owners but the breeding player
  does not own both.
- A tracked animal's record is deleted when the animal dies.

### Daily care and friendship

Owners right-click with the universal feed item to feed (one item used) and with
the caring item to care (item kept). Each adds `friendshipByFeeding` or
`friendshipByCaring` once per day; a repeat gets the `alreadyFed` or
`alreadyCared` message.

Each daily change removes `friendshipLostNotFeeding + friendshipLostNotCaring`
points per day from every animal, whether or not it was fed and cared for.
Friendship never goes below 0 and has no upper limit;
`maxFriendshipAndGenetics` caps only child genetics and sets the scale of the
menus and bundle tiers.

### Animal states

| State | Set when |
| --- | --- |
| `HAPPY` | Tamed, or the last daily change found it fed, cared for, slept in a stable, with water and space. `/breedingbuddies fix` also sets it. |
| `SAD` | The last daily change found any of those conditions unmet. |
| `UNOWNED` | Bred, or its last owner left. |
| `SPAWNED` | Created by `spawnanimal` or `spawnmount` and not yet tamed. |
| `ESCAPED` | Spent too many daily changes outside a stable. |

`SICK` and `ABANDONED` exist in `AnimalStates.java` but are never set. Only
`HAPPY` animals give bundles.

### Stable chunks and checks

Right-clicking with the stable chunk item makes the player's current chunk a
stable chunk and uses one item. Stable chunks that share an edge merge into one
chunk area. `/breedingbuddies stablechunk` reports whether the current chunk is
one. There is no command to remove a stable chunk.

During each daily change, for each chunk area:

- **Water:** the area has water if any of its chunks contains a water block or
  a water cauldron.
- **Space:** the area lacks space when it holds more than
  `maxAnimalsPerChunk` × its chunk count of animals, counting every animal
  entity, owned or not.
- **Abandonment:** an area with no owned animal in it gains one abandoned day.
  Scheduled and `changeday` changes remove areas with more than
  `maxIrlDaysChunkAbandoned` abandoned days. The count is never reset, so days need not be consecutive.

Chunks are force-loaded while they are checked.

### Days out and escape

Owned animals found inside a chunk area have their days out reset to 0. Mounts
(any horse-like entity) need no stable and always count as having slept in one.
Any other owned animal not found in an area counts as having slept outside and
gains one day out. When days out exceed `maxIrlDaysOut`, the animal becomes
`ESCAPED`, loses its resolved character owners and joins the unowned list.
Without held slots, anyone can tame it again. Unresolved legacy owner slots and
raw extension metadata remain; an unresolved escaped animal still refuses token
claims until staff review.

### The daily change

`DayChangeScheduler` checks the UTC clock every 60 seconds and fires the daily
change at `startingDayHour`:`startingDayMin` UTC. `/breedingbuddies changeday`
fires it at once. Either way the change counts as one day, then:

1. Every owned animal in a chunk area is updated with its area's water and
   space results, and every other owned animal as described above.
2. Each update sets `HAPPY` or `SAD` from the day just ended, clears fed and
   cared, removes friendship and records the update time. An animal updated
   less than 24 whole hours earlier is skipped.
3. Escapes are processed, all data is saved, and `lastDayChangeDate` in
   `config.yaml` is set to the current time.

The pass runs on the server thread on the next tick, and only one pass runs at
a time. The
scheduled change and `changeday` also remove abandoned chunk areas; catch-up
passes do not.

### Catch-up

When at least one whole day has passed since `lastDayChangeDate`, the plugin
catches up:

- Right-clicking an owned animal first updates that animal for the missed days,
  then starts a full pass for the same number of days.
- Using the farm report item runs the full pass straight away before the
  report is shown.

Friendship loss is multiplied by the number of missed days. Days out and
abandoned days still grow by one per pass.

### Genetics and breeding

When a player breeds two animals they own, the child is added to the unowned
list as `UNOWNED`. The owner, or any other player, then tames it with a named
taming item. For non-mounts:

- child genetics = average parent genetics + random value from 0 to *variance*
  + friendship influence, capped at `maxFriendshipAndGenetics`;
- *variance* = max(100, `geneticVarianceMultiplier` × (1000 − average genetics
  ÷ (10 × `geneticDivisorMultiplierToRetardProgression`)));
- friendship influence = average parent friendship × 0.05 ×
  `friendshipInfluenceMultiplier`.

Breeding between animals that are not both owned follows vanilla rules and the
child is not tracked.

### Bundles and the collector item

An owner right-clicks an animal with the collector item to receive a bundle.
The type must have `bundlesEnabled: true`, the animal must be `HAPPY`, and
`hoursBetweenRewards` must have passed since the last collection. The first
collection is available at once. A failed attempt plays an angry sound.

The bundle tier depends on how high and how even the animal's points are:

- score = max(0, (friendship + genetics) ÷ 2 − |friendship − genetics|);
- tier index = score ÷ (`maxFriendshipAndGenetics` ÷ number of tiers), using
  the order of tiers under `bundles` and capped at the last tier.

The collector needs an empty storage slot; armour and off-hand slots do not
count. Without one, the player gets `lacksSpace`, no bundle is given and the
cooldown does not start.

Right-clicking with a bundle opens it: one bundle is used and one prize is
picked from the tier's `prizes` by `weight`. Bundles are matched by their stored
entity type and their item ID. The prize is added with the normal inventory
rules; anything that does not fit is lost. Check item IDs: a vanilla ID that
matches no Material can give dirt, and a missing MMOItem raises an error.

### Farm report

Right-clicking with the farm report item runs any catch-up, then lists the
player's animals fed and cared for today and their total. It warns when any
animal slept outside a stable, needs more space or lacks water at the last
daily change.

### Animal and mount menus

- Sneak and right-click with an empty hand, or right-click with the mount
  stats item, on a tracked non-mount animal to open the animal menu: name, time
  to next bundle, state, five friendship and five genetics markers (one per
  fifth of `maxFriendshipAndGenetics`) and, for owners, **Remove ownership**.
- Right-click a mount with the mount stats item to open the mount menu, which
  adds neutered status, health in hearts, speed in blocks per second and jump
  height in blocks. Untracked mounts show a placeholder record.

The menus open for owners, unowned tracked animals and holders of
`breedingbuddies.use`; the mount menu also opens for untracked mounts. Both use
the `inventoryName` title. Each menu captures the opening session and refuses
removal after switching. Outgoing session cleanup closes its captured menu and
dismounts the outgoing player even when that session is already noncurrent.
Session start only ejects a player from a configured or known animal they cannot
ride; unavailable animal data does not eject them from unrelated boats or
minecarts. Session end retains its existing dismount behavior for every vehicle.

### Anvil renaming

`AnvilRenameListener` stores the anvil rename text on taming item results. The
animal itself is named from the item's display name.

### Mounts

Mounts are horse-like entities (`AbstractHorse`: horses, donkeys, mules,
llamas, camels and the undead horses). Health, speed and jump ranges come from
the type's `mountStats` in `bundles.yaml`, then `defaultMountStats` in
`config.yaml`. The lookup uses the entity type name, such as `HORSE` or
`SKELETON_HORSE`, so a custom name does not change the range.

- **Genetics:** the average of health, speed and jump, each scaled to its range,
  times `maxFriendshipAndGenetics`.
- **Breeding:** when the player owns both parents, one tick after the birth
  each of the foal's stats is set to a random value between slightly below the
  weaker parent and slightly above the stronger parent, kept within the range.
  The callback retains the initiating session and rechecks ownership; switching
  characters cancels it. Parent values above the range maximum are capped first. The foal is tamed in
  vanilla and recorded as unowned.

### Mount nerfing

When `nerfMountStats` is true, every horse-like entity's health, speed and jump
are divided by `mountNerfDivisor` once, and the entity is flagged so it is not
divided again. This happens when it spawns naturally or from a spawn egg, and
when a chunk loads containing a horse-like entity without the flag. Bred foals
are not flagged at birth, so they are divided the next time their chunk loads.
Command-spawned mounts and `spawnmount` mounts are flagged without dividing.
There is no minimum value.

### Neutering

An owner right-clicks an owned foal with the neuter item to neuter it. Holders
of `breedingbuddies.use` can also neuter adults they own. Breeding is
cancelled when either parent is neutered; for two mounts, love mode is cleared
and `neuteredHorse` is shown. The scoreboard tag `ho.isNeutered` also counts as
neutered.

## Configuration files

On first start the plugin writes `bundles.yaml`, `items.yaml`, `messages.yaml`
and `config.yaml` to `plugins/BreedingBuddies/` from defaults in
[`BreedingBuddies.java`](https://github.com/TF-Minecraft/BreedingBuddies/blob/main/src/main/java/net/tfminecraft/breedingbuddies/BreedingBuddies.java).
Existing files are kept; the plugin only updates `lastDayChangeDate`.

| File | Purpose |
| --- | --- |
| `config.yaml` | Balance, limits, breeding, reward timing, daily change time, mount ranges and nerfing. |
| `items.yaml` | Item IDs for each action. |
| `bundles.yaml` | Farm animal types, mount stat ranges per type, and bundle tiers and prizes. |
| `messages.yaml` | Player messages and the menu title. `%s` is the animal's name or a count. |

### `config.yaml`

| Key | Default | Effect |
| --- | --- | --- |
| `maxFriendshipAndGenetics` | `10000` | Child genetics cap and scale for menus, bundle tiers and mount genetics. |
| `initialGeneticMax` | `200` | Exclusive upper bound for a new wild animal's random genetics. |
| `friendshipByFeeding`, `friendshipByCaring` | `200`, `200` | Friendship gained from each daily action. |
| `friendshipLostNotFeeding`, `friendshipLostNotCaring` | `50`, `50` | Summed and removed per day from every animal. |
| `maxAnimalsPerChunk` | `20` | Animals per chunk before an area lacks space. |
| `maxIrlDaysOut` | `3` | Escape once days out exceed this. |
| `maxIrlDaysChunkAbandoned` | `5` | Remove a chunk area once its abandoned days exceed this. |
| `geneticVarianceMultiplier` | `0.4` | Scales the random part of child genetics. |
| `friendshipInfluenceMultiplier` | `0.4` | Scales the friendship bonus to child genetics. |
| `geneticDivisorMultiplierToRetardProgression` | `0.4` | Divides the variance lost as parent genetics rise; larger values keep more variance. |
| `hoursBetweenRewards` | `8` | Hours between bundle collections. |
| `lastDayChangeDate` | first start time | Epoch seconds of the last daily change, written by the plugin. |
| `startingDayHour`, `startingDayMin` | `21`, `1` | UTC time of the daily change. |
| `defaultMountStats` | horse ranges | `minHealth`, `maxHealth`, `minSpeed`, `maxSpeed`, `minJump`, `maxJump` fallback. |
| `nerfMountStats` | `false` | Enables mount nerfing. |
| `mountNerfDivisor` | `2.0` | Divisor for nerfed health, speed and jump. |

Missing numeric keys read as 0. Keep every key; for example,
`initialGeneticMax: 0` makes taming wild animals fail.

### `items.yaml`

Each value under `items` is compared, ignoring case, with the held item's
MMOItems ID, or with the Material name for vanilla items. The MMOItems type is
not checked. Keep every key: the built-in fallbacks use `minecraft:` IDs, which
never match.

| Key | Default | Use |
| --- | --- | --- |
| `tamingItem` | `TAMING_ITEM` | Tame or rename after an anvil rename. |
| `coownershipItem` | `COOWNERSHIP_ITEM` | Link and share ownership. |
| `universalFeed` | `UNIVERSAL_FEED` | Daily feeding. |
| `caringItem` | `CARING_ITEM` | Daily care. |
| `farmReportItem` | `FARMREPORT_ITEM` | Farm report. |
| `stableChunkItem` | `STABLECHUNK_ITEM` | Make a stable chunk. |
| `collectorsItem` | `COLLECTOR_ITEM` | Collect bundles. |
| `mountStatsItem` | `CARROT_ON_A_STICK` | Mount and animal menus. |
| `neuterItem` | `SHEARS` | Neutering. |

### `bundles.yaml`

```yaml
COW:                          # Entity type; makes COW a farm animal
  bundlesEnabled: true
  bundles:
    common:                   # Tiers, lowest first
      bundleItem:
        type: "mmoitem"       # or "vanilla" with itemID
        mmoitemType: "PETS"
        mmoitemID: "COMMON_ANIMAL_BUNDLE"
      prizes:
        prize1:
          type: "vanilla"
          itemID: "BEEF"
          amount: 4
          weight: 50
```

The defaults define `HORSE`, with `mountStats` ranges (`minHealth` to
`maxJump`) and no bundles, and `COW`, with `common` and `rare` tiers. A type with `bundlesEnabled: true` needs a `bundles` section, and
each tier needs at least one prize with a positive weight.

## Commands and permissions

`/breedingbuddies <subcommand>` requires `breedingbuddies.use`. `plugin.yml`
declares no permission defaults, so the node is operator-only unless granted.

| Subcommand | Effect |
| --- | --- |
| `reload` | Re-reads the four YAML files, creating any that are missing, and restarts the daily change scheduler. Saved animal and chunk data is not re-read. |
| `stablechunk` | Reports whether the player's chunk is a stable chunk. |
| `changeday` | Runs a one-day daily change now. |
| `spawnanimal <type> <friendship> <genetics>` | Spawns a farm animal type at the player as `SPAWNED` with those points. |
| `spawnmount <type> <friendship> <health> <speed> <jump>` | Spawns a mount with those base stats; health is a whole number. It is flagged as already nerfed. |
| `savedata` | Saves data now. |
| `loaddata` | Re-reads the JSON data files. |
| `fix` | Sets every owned animal to `HAPPY`. |

`breedingbuddies.use` also lets a player interact with others' animals, open any
tracked animal's menu and neuter adult mounts they own.

`spawnanimal` completion offers spawnable animal types configured in the loaded
`bundles.yaml`, including changes after reload. Numeric presets for `spawnanimal`
and `spawnmount` match the current prefix; other valid numbers can be typed.

## Persistence

Data is written as JSON beneath `plugins/BreedingBuddies/Data/`:

| Path | Contents |
| --- | --- |
| `CharacterData/<character UUID>.json` | Explicit account/character `owner` envelope and raw `animals` fanout for each current owner slot. |
| `character-unowned.json` | Agreed animals without resolved character slots, including held legacy slots. |
| `PlayerData/<account UUID>.json`, `unownedanimals.json` | Untouched legacy source; never loaded as character files. |
| `ownership/source.json` | Fixed archive of every original legacy document, including top-level and nested unknown/null fields. |
| `ownership/legacy-heirs.json` | Fixed reviewed account-to-character/null mapping, written before the migration intent and reused after failure. |
| `ownership/migration.json` | Versioned canonical agreed animal rows, fixed character slots, held conflicts and original documents. |
| `ownership/journals/*.json` | Full expected-before/desired-after documents, canonical rows and durable completion. Plain gameplay journals are removed after durable completion; migration, estate and token-linked journals are kept. A crash before removal can leave an inert completed gameplay journal. |
| `ownership/token-effects/*.json` | Stable operation IDs, captured sessions/refs, exact token bytes, animal before/after and owner journal, with prepared/debit-prepared/done status. |
| `stablechunks.json` | Array of chunk areas with `daysAbandoned` and `chunks` (`world`, `x`, `z`). |

Animal entries retain `uuid`, `name`, legacy `ownersUuids`, `stableNeeded`,
`friendshipPoints`, `geneticPoints`, `state`, `fed`, `cared`, `sleptInStable`,
`spaceNeeded`, `waterNeeded`, `daysOut`, and millisecond timestamps. The explicit
`characterOwners` slots grant authority; `heldOwners` record unresolved legacy
accounts. Legacy `ownersUuids` remain historical metadata. A co-owned animal
appears in each character file with an identical raw row, and loads into one
runtime object only after agreement. Normal saves patch recognized fields while
retaining unknown fields, explicit nulls and held/unloadable rows across repeated
saves and restarts. Raw per-file envelopes remain with their own copies.

Configuration loads before animal data. Boot recovers or holds incomplete
fanout before runtime/day updates, then waits for reviewed legacy heirs. The
plugin saves every 10 minutes, after each daily change and on disable, including
offline characters. Every fanout plan includes existing recipient and emptied
former-owner files; it durably writes the intent first and forces each atomically
replaced file and directory before acknowledging completion. Each output must
still match its captured before state or the desired after state. A conflicting
post-plan edit stays held instead of being overwritten. Changed routine saves use
the same journal so a crash cannot make the next boot choose an arbitrary copy.
Unchanged saves without active or unfinished token effects write nothing after
checking the archived source, exact output keys, current file inventory and
bytes, token receipts and held-record evidence.
Only a ready store can save; pending publication must recover before readiness.
An unfinished token effect still requires checked publication. A publish call
removes only its own plain gameplay journal after its completion is durable;
migration, estate and token-linked journals and all token receipts remain.
Removal failures can leave an inert completed journal and do not undo publication.
Kept journals are full snapshots, so the folder grows with token acquisitions
and estate transfers; boot and the hourly estate check read them all.
Version 1 journals bind their kind to their envelope and validate every desired document against captured source bytes and canonical rows before publishing. Unsupported paths/versions, extra or omitted animals, changed unrelated estate state, inconsistent slots and duplicate JSON keys at any nesting depth stay BLOCKED without rewriting their bytes. Held IDs require independent preservation evidence; a changed hold map cannot hide an ordinary source row. Journals freeze full unfinished token-effect snapshots and validate their fixed identity/session/item/animal-before fields. A later reviewed completion can release that animal without invalidating a historical estate receipt. Keep the original fixed effect fields and any captured owner-publication evidence when recording that resolution. Every destination is checked again immediately before its write.

Autosave and `savedata` are skipped while a daily change is queued; disable saves
run when the ownership store is ready.

### Reviewed migration and estates

Inventory includes every row in `PlayerData` and `unownedanimals.json`. The
account filename contributes its old effective ownership; ownership arrays are
compared as sets. Disagreements in effective owners, known state or unknown
fields hold the complete animal, with every original copy retained. No first
file, latest file or synthesized union wins. An unreadable inventory file holds
the migration because completeness cannot be established. Logs name held causes.

Mapping uses only fixed reviewed `Characters.legacyHeir` answers after
`legacyHeirsReady`; missing/wrong-account heirs stay held. A dead reviewed heir
still receives its legacy slot. Optional heir and estate bridges load only after
capability probes. Older providers retain ownership in place rather than assign
an active character.

The `breedingbuddies-animals` estate participant moves only the deceased
character's slot. Other owners remain, and an already-owning recipient merges to
one slot. Physiology, genetics, friendship and reward/care timestamps are retained;
no animal is copied or respawned. Existing chunk occupancy limits remain global;
there is no per-account animal-acquisition cap in this plugin.

Before planning a new estate movement, validate all source/recipient slots and
flush every runtime animal’s buffered physiology through the checked gameplay
journal; pending/held fanout refuses that flush. Recheck the estate decision after
flush. This retains unrelated care in shared files when runtime records reload.

Estate intents retain exact decision text, revision, death ID, from/to account
and character refs, canonical rows and all expected fanout documents. Exact
`Estates.guardHolds` checks precede each publication and completion. Replaying the
same revision returns cumulative IDs without another transfer; later frozen or
waiting revisions retain earlier receipts. Completed receipts are semantically validated before their IDs are counted, including their full captured decision and source/destination snapshots. New revisions can move only untouched still-testator slots; restoring an already-moved animal to the testator while its receipt remains is BLOCKED rather than transferred again.
A stale partially published plan is BLOCKED for reviewed recovery, never completed
to an obsolete recipient or restored over newer progress. I/O failures RETRY;
conflicting state or metadata stays held. Boot/hourly reconciliation reports each
death/revision independently. Resolve recorded conflicts through the normal
estate staff retry/waive workflow; do not clear a journal to force a new recipient.

### Offline rollback

This prepares legacy account files for the pre-character build in the `d6fa922`
source lineage; that lineage has no published JAR. It does not switch builds or
make a character-ownership build use legacy data. Character data, journals,
receipts and the migration manifest remain authoritative and are not moved,
renamed or deleted. Starting a character-ownership build again resumes the
existing character store and does not migrate again.
Use normal deployment downtime before preview/apply. From the source checkout:

```sh
python3 tools/animal-ownership-rollback.py /path/to/plugins/BreedingBuddies/Data
python3 tools/animal-ownership-rollback.py /path/to/plugins/BreedingBuddies/Data --apply --backup /path/to/new-breedingbuddies-recovery
```

Preview is read-only. Automatic apply requires complete journals, unchanged
legacy files and exact agreement with the fixed migrated canonical rows. New
animals, deaths, care updates, ownership grants/removals and estates are reported
as conflicts and refuse automatic restoration; they require staff reconciliation.
This avoids resurrecting animals or silently discarding subsequent progress.

A permitted apply refuses an existing/overlapping backup path, copies the entire
data directory, verifies every file's SHA-256 and forces the recovery image before
restoring the unchanged account source documents as exact UTF-8 bytes, including
original line endings. Character data, unknown fields
and journals remain available. The old JAR reads account files; reinstalling it
alone can expose obsolete ownership/progress. Keep the recovery image and review
any old-version writes before upgrading again. After any writes by the
pre-character build, the character store refuses to open until staff review.
Source/archive contraction is a separate later migration.

New tame/co-own acquisitions write token evidence before checked ownership
publication, then arm the debit before touching the item/entity. The receipt’s
`ownerJournal` names its own kept token-linked journal. An unavailable store or
a publication unbound to that token holds the animal before debit. A known failure
before ownership publication leaves the token and entity name intact. Receipt
failure after a debit, changed captured session/payload, or an unfinished receipt
on restart holds that animal for staff; no token is automatically replayed or
refunded. The compatibility naming helper remains separate.

Ownership files and Minecraft inventory/entity saves are sequential, not one
transaction. A crash after the done receipt but before Minecraft persists the
body can still retain a token; a crash after debit but before receipt completion
is explicitly held. Arbitrary-crash exactly-once token/bundle effects are not
proved. Preserve receipt, player body and store for manual reconciliation rather
than trusting an old stack or clearing the hold. Existing bundle overflow remains
as described above.

### Verification

Run Java 21 `tfmc-mvn -o -B clean verify` and
`python3 -m unittest discover -s tools -p 'test_*.py'` from the source worktree.
Tests cover same-account characters, stale/wrong-account sessions and menus,
switching before deferred mount inheritance, resolved/held co-owner rights,
all legacy copy representations, raw/null preservation through normal saves and
restart, failure after individual fanout publications and edits to later destinations,
idle-save byte preservation, same-call gameplay pruning and interrupted replay,
inert done journals, removal failures, token publication binding, configured-species
removal with persisted ownership/held guards, registered event dispatch for
unrelated entity interactions and session-start vehicles, unavailable-store
breeding scope and escape raw/held-slot preservation, pre-publication token I/O refusal
and post-debit receipt holds, strict estate guards,
co-owner merges, cumulative replay, completed-receipt/source restoration conflicts, valid-JSON journal tampering, nested duplicate keys and conservative rollback conflicts. The
existing zero-missed production-line gate remains enabled. Actual older TLibs
classloader probes check optional API isolation. Synthetic real Paper checks
should exercise mounted A-to-B isolation, stale menu refusal and resolved
co-owner access with a held sibling, using current production classes and the
same farm-type configuration initialization as normal startup. Retain per-class
byte comparisons; fixture results do not carry forward to changed bytecode.
A controlled entrypoint/provider checks those hooks, not full plugin startup
or RPCharacters selection/body flow.

### Operational caveats

- The JSON paths are relative to the server's working directory, not the plugin
  data folder. They match only when the server runs from the directory that
  holds `plugins/`.
- `loaddata` rebuilds runtime records from the recovered store; unsaved changes
  are lost. Held records stay raw and inert.
- The daily change writes the in-memory `config.yaml` back to disk. Run
  `reload` straight after editing `config.yaml`, or the next change overwrites
  the edit.
- Every stable chunk is loaded at startup; chunks in a missing world are
  dropped. Each daily change force-loads every stable chunk on the server thread
  while it checks it, so large stable areas can cause a brief tick spike at
  that time.
- A failure in one chunk is logged as `Error processing chunk <x>,<z>` and its
  animals are treated as outside a stable; a failure in the water or space check
  aborts the pass with `Error on DayChange` on standard output.
- Because of the 24-hour skip, `changeday` does not update animals already
  updated that day, but stabled animals that are not found still gain a day out
  and empty areas still gain an abandoned day. Repeated use can make animals
  escape and remove stable chunks.

Back up the whole `plugins/BreedingBuddies/` directory before changing
configuration or moving data, and stop the server cleanly before copying it.
