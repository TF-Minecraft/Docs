# Trains: spline tracks

Trains follow spline tracks. Ground vehicles use the separate terrain-follow system.

The spline data defines the track path. Vanilla `Rail` blocks are not used for trains.

## Behavior

- Scenic routes with **gentle turns** (35 degrees maximum by default), not only Minecraft 90-degree rail shapes.
- Passenger consists use locomotive ticket and whitelist settings.
- Tracks can be **damaged** (bomb, break). Motion and unloaded logic read **data**, not whether a display entity exists.

Vehicles use `SpawnManager` and SQLite payloads; spline paths persist separately.
Track displays spawn and despawn with their chunks.

## Core rule: spline is the object

```
Spline (JSON, always loaded or loaded per world)
  samples     motion + bake source
  segments    health / broken (bombs write here)
  visuals     ItemDisplay entities, chunk-local
Consist       ordered cars + splineId + arc length s + body orientation + occupied junctions
```

- **Anything that touches the rail** (explosion, break, admin repair) updates **segment flags** on the spline. Displays are rebuilt from that, or hidden if the chunk is unloaded.
- A missing or unloaded display **must not** change the path. Motion advances loaded vehicles using this data.
- Cars **do not** physics-ride the mesh. Their positions follow coupler spacing along the selected route. Each car changes spline when it reaches the frog; coupled cars can span multiple junctions.

### Motion (1D)

- Signed movement along a spline is panel speed × body `orientation`. Orientation is +1 when the nose faces +s and −1 when it faces −s; it is independent of forward/reverse throttle. `travelSign` follows actual motion, including braking and coasting.
- `TrainRoute` walks connections in the body's frame and preserves leftover movement across a junction. Crossing between a stem and branch multiplies orientation by the junction's `facing` sign.
- Each carriage follows its parent's rear coupler. Wheel and bogie offsets use that car's body orientation, so reversing never swaps the carriage order or spins a model.
- Position: teleport the armor stand **XYZ** only. Heading follows the rail tangent in the saved body orientation; the body bone supplies yaw and pitch.
- **Circuit:** loop tracks wrap at their seam. A real branch tip remains an open end.
- **Junctions:** captain holds **A** or **D** within `junction-arm-distance` (default 16) of the leading wheels. Left/right are viewed towards actual travel. Matching the turnout side selects the branch; the other key selects through. Reverse works too. At rest, nonzero throttle chooses the approach direction; otherwise the last direction is retained.
- **Whole-train route:** choose before the first wheels enter. The switch is locked while occupied, including when the rear carriage leads. Each occupied junction keeps its own decision until the whole consist clears, so reversing midway retraces the same route. Leaving a branch follows its connection back to the stem.
- **Broken segment:** stop or clamp before the break; remain bound to the track.

#### Reverse example

For an engine with three carriages backing into a siding, carriage 3 enters first,
then 2, then 1, then the engine. Select the siding before carriage 3's leading
wheels reach the junction. The switch stays locked until the engine clears.
Stopping halfway and pulling forward again follows the same rails.

### Spacing

Reuse `behaviour.train` front/back connector bones ([`Connector`](https://github.com/TF-Minecraft/VehicleFramework/blob/main/src/main/java/net/tfminecraft/vehicleframework/vehicles/handlers/train/Connector.java)). Spacing is bone distance along the spline.

## Visuals

- **Source of truth:** samples. **Meshes:** anchored to the spline at bake intervals.
- **Meshes:** ItemDisplays use the `item-small`, `item-medium` and `item-large` ItemsAdder paths in `trains.yml`. Small pieces are 1x3 (one plank, rails on either side), about **one per block** on curves and slopes.
- Collinear unbroken runs merge into medium and large pieces up to 3x3; motion samples remain dense.
- Spawn displays when the **chunk loads**; remove when it unloads.
- Bake is **cached** on the spline (`visuals()`). Chunk spawn iterates that list; it does not rebake per chunk. `replace` invalidates the cache.
- `/vf reload` reloads spline JSON and vehicle configs, then **respawns railroad switches** in loaded chunks from live `trains.yml`. Rail ItemDisplays keep the last **applied** style (`item-small` / `medium` / `large`, `display-y-offset`) until `/vf track resync`.
- `/vf track resync` copies live rail style to applied, invalidates bake caches, and respawns **rails only** in currently loaded chunks (`resync-chunks-per-tick`, default 2). Unloaded track is not spawned; it uses the new applied style the next time that chunk loads. Console can run this command.
- Lay, join, dig, and break still rebake loaded pieces using the **applied** rail style. Preview new rail models with reload then resync.
- Target: a player at max render distance might see a few hundred 1x3 displays. If that hitchs, merge straights before changing spawn rules.

## Authoring

Track items, lay rules, and train debug logging live in [`trains.yml`](https://github.com/TF-Minecraft/VehicleFramework/blob/main/src/main/resources/trains.yml) (`plugins/VehicleFramework/trains.yml`). `debug-logging: true` writes `logs/track.log` and `logs/recorder.log`. Vehicle save, spawn, unload, and mount lines go to `logs/persistence.log` when `persistence-logging: true` in `config.yml`. Persistence pose lines are entity location only. Recorder `POSE` / `SAMPLE` / `JUNCTION` include `eyaw` (stand), `dyaw` (bone `driveYaw`), and on `POSE` also `myaw`/`mpitch` (move `fromDirection`) and `pyaw`/`ppitch` (sample). `POSE` is rate-limited (~250 ms) so it logs without the tape item.

One spline per track (no stored sections). A **stroke** is one lay with the configured layer item (`item-layer`, default `m.utils.train_track_layer`):

- Left-click: **start location** (block or existing track). Click an existing end to join that track.
- Right-click: **end location**. New track is a straight line in XZ from start to end (player look is ignored); extending an end curves from the track heading as described in [Curves](using-trains.md#curves). Click within `join-distance` of an existing **end** to join: same track extends, or **two tracks link into one** if start is on one end and end is on another. Join curves from the **track** heading. Ending a stroke from a free end within `join-distance` of the **middle** of another track joins it there at a new junction: the stroke runs into that track along it (refused if it cannot curve that far) and must be affordable in full. Starting on the middle of a track still needs the junction item. Joins keep the direction (`+s`) of any track a train is on, so each train keeps its saved orientation: closing a loop never reverses the track, and linking two tracks reverses at most one track that has no train, preferring one that is not a branch. Linking two occupied tracks start to start, or end to end, is refused. Trains saved in unloaded chunks count as occupying their track.
- **Creative / spectator:** the spline is saved, then displays rebake in one step. One place sound + particles at the last sample (`build` in `trains.yml`).
- **Survival / adventure:** same save, but displays grow along the new stroke one sample every `build.interval-ticks` (default 4, five per second). Prefix rebakes so collinear runs become medium then large. Each step plays `build.sound` and particles at the new sample, and swings the main hand if `build.swing` is true. Set `build.interval-ticks` to `0` to always place instantly. Connecting two tracks or closing a loop is still instant plus one burst.
- Remover item (`item-remover`, default `m.utils.train_track_remover`): left-click **digs** a sample (interior dig **splits** into two tracks). On a branch, digging any part of the **initial turnout lay** (stored as `turnoutS` on the junction) removes the whole turnout (junction, switch, and that stub). Digging past that initial lay uses normal dig/split rules; a longer branch extension is kept as plain track. The through stem stays. The remover refuses to dig track that a bound consist occupies, measured from each car out to its couplers. That includes a branch turnout the dig would drop because its frog ends up on a piece shorter than `min-lay-distance`. When a dig or lay rebuilds a spline, trains on it keep their world position on the new spline or pieces. A train in an unloaded chunk checks its saved spline and `s` against where it respawns, and re-finds the track under it (or unbinds if the track is gone).
- Junction item (`item-junction`, default `m.utils.train_track_junction`): right-click **existing track** (interior allowed) to start a junction (nothing is saved yet). Then layer **right-click** lays **one** turnout from that frog. The junction is saved only if that branch lays. Ending the turnout on another track's free end joins that track; ending it part way along a track (including the stem) joins it at a second junction, so a branch can rejoin its line or cross over to another. Through stays the original spline. Layer **left-click** while a junction is pending cancels it and marks a normal start. The stem must be at least `min-lay-distance` (default 8) long; loops are exempt. After a split, a junction rehomed onto a piece shorter than that is dropped with its branch.
- `min-junction-spacing` (default 16) along stem arc `s` (loop wrap). One branch per junction (no 3-way). A branch can meet a junction at each end; an end that meets a frog is not a free end and cannot be laid from or joined.
- `max-junction-length` (default 32): the turnout from frog to click cannot be longer than that (straight-line or along the laid curve).
- `junction-arm-distance` (default 16): press A/D this far before the leading wheels reach the frog (a facing approach in either forward or reverse). A = LEFT, D = RIGHT viewed towards travel. Matching the turnout side throws diverge; the other key throws through. Occupied points refuse changes. Every train, including unmanned trains, takes the switch position when its leading wheels arrive and retains that choice until clear. Tape controls throttle only.
- `item-switch` (default `ia.tfmc:railroad_switch`) plus `switch.offset-along` / `offset-out` / `offset-y` / `yaw-inward` / `throw-degrees` / `throw-degrees-per-second` place and animate the ItemDisplay on the through side of the frog. Chunk load respawns it at the saved pose; the entity is not persistent.
- A junction branch still needs a 3-wide by 3-tall corridor of passable blocks. It may cross existing track (including the stem); overlapping tracks do not refuse a turnout.
- `max-turn-degrees` (default 35) and `min-lay-distance` (default 8): refuse if the stroke is too short, or if a **join** turn (heading change from the existing end) is too sharp.
- `curve-radius` (default 32, at least 1): bend radius for extensions and joins ([`TrackCurve`](https://github.com/TF-Minecraft/VehicleFramework/blob/main/src/main/java/net/tfminecraft/vehicleframework/tracks/TrackCurve.java)). Strokes too short for it bend tighter, down to `min-lay-distance / (2 sin(max-turn-degrees / 2))`.
- Grade: stay **flat** as long as possible, then climb at `desired-grade-degrees` (default 6), never steeper than `max-grade-degrees` (default 10). Chat says **slope is too steep** if the end is too high for the run.
- Clearance: a 3-wide by 3-tall corridor must be passable (air and plants are fine; solids and overlapping tracks are not).
- Punching track in survival or adventure, and explosions (TNT, creepers, VF ammunition), mark edges broken and drop one `item-track` per newly broken edge. Creative punch and the remover dig do not drop.
- `place-keepout-radius` (default 1.5): cannot place blocks or empty buckets within that XZ distance of a sample in the train's headroom: the rail's block Y and the two blocks above it. Blocks below that Y (new ground under the rails) and three or more blocks above it (bridges, roofs, tunnel ceilings) are allowed.
- Moving trains spawn `fx` gravel `BLOCK_CRACK` crumbs on that 3-wide ballast (rotated with the rail yaw). `fx.sound` is a string (vanilla `minecraft:block.stone.break` or a custom namespaced sound).
- `/vf track delete <uuid>` removes the whole track. `/vf track start` and `/vf track end` use your current position.
- `/vf track resync` applies rail item paths and `display-y-offset` from `trains.yml` to loaded chunks (throttled). Switches follow `/vf reload` and chunk load without this command.
- `/vf track dump` appends a network snapshot to `logs/track.log` (`DUMP`, `SPLINE`, `PT` every 32 along `s`, then `JUNCTION` frogs including `thrown`). The same dump runs on plugin load. `JUNCTION_DROP` is written if a junction JSON is skipped (`no-stem` / `no-branch`) or cancelled as incomplete. On load and after lay/dig/delete, non-loop splines up to 16 blocks long that lie entirely on a longer spline in the same world are removed automatically (duplicate overlays and stray stubs).

## Persistence

### Spline

`plugins/VehicleFramework/data/tracks/<world>/<splineUuid>.json`

Stored path fields: `id`, `world`, `loop`, `samples[]` (`x,y,z,yaw,pitch,s`), `segments[]` (`fromIndex`, `broken`, `health`). `loop` is **true** for a circuit: `closeLoop`, or when first and last samples are within `tracks.join-distance` after extend / load. Optional `visuals[]` in JSON is regenerable; runtime bake lives on the spline object.

Index which chunks a spline touches so `ChunkLoadEvent` can spawn only local displays.

Junctions are **not** nested in spline JSON:

`plugins/VehicleFramework/data/tracks/<world>/junctions/<junctionUuid>.json`

Fields: `id`, `stem`, `s`, `facing`, `side`, `thrown` (diverge lever; missing = through), optional `branch`, optional `turnoutS` (branch arc length of the turnout lay, measured from the frog; set when the branch is laid), optional `branchEnd` (`true` when the branch meets this frog at its last sample, as when it rejoins a line; missing = its first sample). Prepend, split, and connect remap `s`, and keep each branch's junctions on whichever track still meets the frog. Deleting a stem drops its junctions; deleting a branch spline clears `branch`.

### Consist (still chunk-spawned cars)

On save, write at least:

- `splineId`, `s` (loco origin along the path)
- `child` UUID (and `parent` on trailing cars)
- `orientation` when −1; absent means +1. Legacy `travelSign = -1` remains last movement direction, not body facing.
- `junctions`: occupied junction IDs mapped to branch/through decisions. The locomotive also writes legacy `junction` and `diverge` fields.

On load, cars use the normal vehicle spawning path. When both ends of a link exist in memory, `setChild` / `setParent` again. If the child chunk loads first, the car waits; it does not need a special global spawn.

Do **not** require spawning the whole consist when one chunk loads. Accept temporary split until the other chunks load; retain occupied routes until missing links resolve. Old saves remain readable. Before downgrading below 2.9.0 (the first release with body orientation), restore matching vehicle-data backups: an older reader cannot place a train saved facing −s correctly. See [Upgrading](using-trains.md#upgrading).

## Cargo, recorder and tickets

- container `allow-items` (TLibs paths).
- loco YAML `fuel-cars` (vehicle ids). Each engine slow-tick, the loco drains one matching fuel item from containers on the car directly behind if that car's id is on the list. Empty list = no auto-drain. Cargo GUIs share one inventory so every viewer sees the take.
- recorder item (`tracks.item-recorder`) stores throttle vs spline `s`, travel sign, and **hold ticks** at a stop (engine off still counts). Circuits only: recording runs until one full lap of the **origin** loop (or you cancel). Time on a siding is recorded but does not finish the lap. Samples may include `splineId`, `junction`, and body `orientation` (legacy default +1). Playback converts each sample from its recorded body orientation to the current train orientation; braking throttle can have the opposite sign to actual travel. Playback ramps throttle one step per tick (autopilot). Captain seat is manual (A/D still choose the frog); leaving resumes the tape from current `s`. Junction choice follows the physical switch and the consist’s occupied-route decisions; the tape does not throw switches.
- Same-spline collision: if a locomotive dummy hitbox overlaps another train piece that is not on the same consist, those **two** vehicles explode. The rest of each consist stays and uncouples. Through vs branch at the frog does **not** explode (no frog AABB). [Collision warnings](using-trains.md#collision-warnings) give riders at least 30 seconds' notice while speeds stay as they are. [`TrainCollisionWarning`](https://github.com/TF-Minecraft/VehicleFramework/blob/main/src/main/java/net/tfminecraft/vehicleframework/tracks/TrainCollisionWarning.java) traces each moving train's route with `TrainRoute.trace`, one check further than `seconds`. [`CollisionForecast`](https://github.com/TF-Minecraft/VehicleFramework/blob/main/src/main/java/net/tfminecraft/vehicleframework/tracks/CollisionForecast.java) then steps each pair forward in 0.1-second steps, checking each train's head against the other's body as `TrainCollision` does. Each moving train's steps are worked out once per check, and the search stops at the soonest contact found so far. Unloaded cars come from the vehicle repository's in-memory index of saved track positions. Each car is re-found by its saved world position when its spline has gone or no longer runs under it, and counts as a head. Railroad switches use the configured `item-switch` ItemDisplay at each frog.
- generic vehicle tickets (planes too). Owner toggles in the ownership GUI. Passenger seats need a matching ticket; captain, gunner, mechanic, owner, and whitelist skip. Consist uses the loco ticket id. On coupled trains, whitelist and ticket settings use the locomotive (`ticketSource`); a loco ticket opens passenger seats on any connected car. Tickets are not consumed.

## Validation

Check lay/join/dig/split, loop seams, broken segments, forward and reverse
consists, both turnout directions, three-carriage reverse entry/exit, reversal midway,
adjacent occupied junctions, chunk unload/reload, persistence, rail resync,
recorder stops, coal transfer and passenger ticket access against the current
source and configuration. Record the tested commit and results with the run.

## Code pointers

- Train YAML: `behaviour.train` in [`BehaviourHandler`](https://github.com/TF-Minecraft/VehicleFramework/blob/main/src/main/java/net/tfminecraft/vehicleframework/vehicles/handlers/BehaviourHandler.java)
- Movement entry: [`VehicleMovementController`](https://github.com/TF-Minecraft/VehicleFramework/blob/main/src/main/java/net/tfminecraft/vehicleframework/vehicles/controller/VehicleMovementController.java) `v.isTrain()` -> `splineTick`
- Vehicle persist: [`VehiclePersistence`](https://github.com/TF-Minecraft/VehicleFramework/blob/main/src/main/java/net/tfminecraft/vehicleframework/database/VehiclePersistence.java) (`saveLive`)
- Chunk spawn: [`SpawnManager`](https://github.com/TF-Minecraft/VehicleFramework/blob/main/src/main/java/net/tfminecraft/vehicleframework/managers/SpawnManager.java)
- Junctions: [`TrackJunction`](https://github.com/TF-Minecraft/VehicleFramework/blob/main/src/main/java/net/tfminecraft/vehicleframework/tracks/TrackJunction.java), [`TrackRegistry`](https://github.com/TF-Minecraft/VehicleFramework/blob/main/src/main/java/net/tfminecraft/vehicleframework/tracks/TrackRegistry.java), [`TrainRoute`](https://github.com/TF-Minecraft/VehicleFramework/blob/main/src/main/java/net/tfminecraft/vehicleframework/tracks/TrainRoute.java)
