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
The defaults are `HORSE` and `COW`. Only farm animals can be tamed. Types added
by `/breedingbuddies reload` take effect at once; removed types stay active
until the server restarts.

### Ownership and taming

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
   whoever holds the linked item right-clicks the air or a block. That player is
   added as an owner and one item is used.

A linked item works for any holder; the player using it does not need to be an
owner. All owners have the same rights. An owner leaves by opening the animal's
menu and clicking **Remove ownership**. When the last owner leaves, the animal
becomes `UNOWNED` and anyone can tame it again; its genetics are kept and its
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
`ESCAPED`, loses all owners and joins the unowned list, where anyone can tame
it.

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

The pass runs in an asynchronous task, and only one pass runs at a time. The
scheduled change and `changeday` also remove abandoned chunk areas; catch-up
passes do not.

### Catch-up

When at least one whole day has passed since `lastDayChangeDate`, the plugin
catches up:

- Right-clicking an owned animal first updates that animal for the missed days,
  then starts a full pass for the same number of days.
- Using the farm report item runs the full pass on the main thread before the
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

The collector needs an empty inventory slot. Without one, the player gets
`lacksSpace`, but the collection time is still recorded and no bundle is given.
Empty armour and off-hand slots also count, so a bundle can be lost when only
those are free.

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
the `inventoryName` title.

### Anvil renaming

`AnvilRenameListener` stores the anvil rename text on taming item results. The
animal itself is named from the item's display name.

### Mounts

Mounts are horse-like entities (`AbstractHorse`: horses, donkeys, mules,
llamas, camels and the undead horses). Health, speed and jump ranges come from
the type's `mountStats` in `bundles.yaml`, then `defaultMountStats` in
`config.yaml`. The lookup matches the entity's display name, so named mounts and
multi-word types fall back to `defaultMountStats`.

- **Genetics:** the average of health, speed and jump, each scaled to its range,
  times `maxFriendshipAndGenetics`.
- **Breeding:** when the player owns both parents, one tick after the birth
  each of the foal's stats is set to a random value between slightly below the
  weaker parent and slightly above the stronger parent, kept within the range.
  Parent values above the range maximum are capped first. The foal is tamed in
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

## Persistence

Data is written as JSON beneath `plugins/BreedingBuddies/Data/`:

| Path | Contents |
| --- | --- |
| `PlayerData/<player UUID>.json` | `animals`: every animal the player owns or co-owns. |
| `unownedanimals.json` | `animals`: bred, spawned, released and escaped animals not yet tamed. |
| `stablechunks.json` | Array of chunk areas with `daysAbandoned` and `chunks` (`world`, `x`, `z`). |

Animal entries store `uuid`, `name`, `ownersUuids`, `stableNeeded`,
`friendshipPoints`, `geneticPoints`, `state`, `fed`, `cared`, `sleptInStable`,
`spaceNeeded`, `waterNeeded`, `daysOut`, and `lastRewardCollected` and
`lastUpdated` in epoch milliseconds. A co-owned animal appears in each owner's
file, and loading merges them into one record.

Data loads on enable, before the configuration. The plugin saves every
10 minutes, after each daily change and on disable. Autosave, `savedata` and
the save on disable are skipped while a daily change is running.

### Operational caveats

- The JSON paths are relative to the server's working directory, not the plugin
  data folder. They match only when the server runs from the directory that
  holds `plugins/`.
- Player files are written only for players online at save time. Changes to an
  offline owner's animals, including friendship loss, escapes and deaths, stay
  in memory and are lost on restart unless that owner logs in before the next
  save.
- `loaddata` replaces in-memory records with the saved ones without clearing
  others, so unsaved changes are lost.
- The daily change writes the in-memory `config.yaml` back to disk. Run
  `reload` straight after editing `config.yaml`, or the next change overwrites
  the edit.
- Every stable chunk is loaded at startup; chunks in a missing world are
  dropped.
  Each daily change force-loads every stable chunk while it checks it, so large
  stable areas add chunk loading at that time.
- The water check stops at the first chunk with water without restoring that
  chunk's force-load setting, so it can stay force-loaded.
- The scheduled and interaction-triggered passes read chunks and entities from
  an asynchronous task. A failure in one chunk is logged as
  `Error processing chunk <x>,<z>` and its animals are treated as outside a
  stable; a failure in the water or space check aborts the pass with
  `Error on DayChange` on standard output.
- Catch-up counts days from `lastDayChangeDate` (UTC) to the server's local
  time, so the count is exact only when the JVM's time zone is UTC.
- Because of the 24-hour skip, `changeday` does not update animals already
  updated that day, but stabled animals that are not found still gain a day out
  and empty areas still gain an abandoned day. Repeated use can make animals
  escape and remove stable chunks.
- Animals made with `spawnanimal` or `spawnmount` keep the name `???` after
  taming.

Back up the whole `plugins/BreedingBuddies/` directory before changing
configuration or moving data, and stop the server cleanly before copying it.
