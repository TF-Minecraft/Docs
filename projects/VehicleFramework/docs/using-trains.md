# Trains

A train is a vehicle whose `behaviour` section contains `train`. Locomotives and cars are separate vehicle ids. They couple at bones and follow a spline track, not vanilla rails. The spline layout and the display entities are described in [Spline tracks](trains.md). This page is how to lay track and drive.

## Marking a vehicle as a train

```yaml
behaviour:
  rotator: body_controller
  vector: move.movealign
  train:
    front-connector: connector_front
    back-connector: connector_back
    fuel-cars:
      - coal_car
```

`front-connector` and `back-connector` are optional. A locomotive often has only a back coupler. A car has the coupler that faces the locomotive. `fuel-cars` lists vehicle ids whose fuel the locomotive may burn.

Drive keybinds belong on the `ground` state. `A` and `D` should be `JUNCTION_LEFT` and `JUNCTION_RIGHT` when the locomotive should throw switches. Throttle still uses `THROTTLE_UP` and `THROTTLE_DOWN`. Negative engine `min` is reverse.

Sneak and right-click a car, then sneak and right-click the locomotive, to couple them. Spacing along the track is the distance between the coupler bones.

## Track items

`trains.yml` names the items. The shipped file uses ItemsAdder and MMOItems paths. Point them at your own items.

| Key | Use |
| --- | --- |
| `item-layer` | Lay track |
| `item-remover` | Dig track |
| `item-junction` | Start a turnout |
| `item-switch` | The lever model placed at a frog |
| `item-small`, `item-medium`, `item-large` | Rail models. Straights merge into the longer pieces |
| `item-track` | Item consumed from the inventory while laying in survival |
| `item-recorder` | Record a throttle tape |

`/vf reload` reloads `trains.yml` and respawns switch levers in loaded chunks. Rail models already placed keep their old style until `/vf track resync`. That command copies the current rail items onto loaded track. Unloaded chunks pick up the new style the next time they load. Console may run `resync`.

## Laying track

Left-click with the layer item to set the start. Right-click to set the end. The path is straight in X and Z from start to end. Look direction is ignored. Click solid ground. Grass and plants are refused.

- Click an existing end to extend that track, or to join two tracks into one when the start and end are on different tracks.
- Ends within `join-distance` (default 1.5) can join. A join that turns more than `max-turn-degrees` (default 35) is refused.
- A new stroke shorter than `min-lay-distance` (default 8) is refused. Loops are exempt.
- Grade stays flat, then climbs at `desired-grade-degrees` (default 6) and never steeper than `max-grade-degrees` (default 10).
- The corridor is 3 blocks wide and 3 tall. Solids and overlapping track refuse the lay. Plants do not.
- Survival and adventure place one sample every `build.interval-ticks` (default 4) and consume `item-track`. Creative and spectator place the whole stroke at once. `interval-ticks: 0` always places at once.

Right-click existing track with the junction item to start a turnout, then right-click with the layer to lay one branch. Left-click with the layer cancels the pending junction. One branch per junction. Branches cannot be longer than `max-junction-length` (default 32). Junctions along the same track must be at least `min-junction-spacing` (default 16) apart.

The remover digs a sample. Digging the middle splits the track. Digging the initial turnout lay removes that turnout. Track past that first lay stays. You cannot dig track under a train; move the train first. Trains elsewhere on the track stay where they are.

## Driving

Bind a locomotive by driving it onto the track, or with `/vf track bind` while seated or standing within 8 blocks. `/vf track unbind` releases it.

Hold `A` or `D` within `junction-arm-distance` (default 16) of the next frog to arm that side. The arm stays until the frog. The matching side diverges. The other side stays on the through route. Chat reports which way you armed. Reverse clears the arm. Backing off a branch returns to the stem.

A broken segment stops the train. The train stays on the spline.

Tickets and the whitelist use the locomotive while cars are coupled.

## Admin track commands

All of these need `vf.admin`. Except for `resync`, they must be run by a player.

| Command | Effect |
| --- | --- |
| `/vf track start` | Set the start at your feet |
| `/vf track end` | Lay from the start to your feet |
| `/vf track list` | List tracks in this world |
| `/vf track info [uuid]` | Samples, length, and loop. With no id, uses the track within 8 blocks |
| `/vf track particles [uuid]` | Shows the samples |
| `/vf track delete <uuid>` | Deletes that spline |
| `/vf track bind [uuid]` | Bind the nearby train |
| `/vf track unbind` | Unbind it |
| `/vf track dump` | Writes `logs/track.log` when `debug-logging` is true |
| `/vf track resync` | Rebuilds loaded rail displays from `trains.yml` |

Track JSON is stored under `data/tracks/`.
