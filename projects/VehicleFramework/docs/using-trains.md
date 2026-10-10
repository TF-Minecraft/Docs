# Trains

A train is a vehicle whose `behaviour` section contains `train`. Locomotives and cars are separate vehicle ids. They couple at bones and follow a spline track, not vanilla rails. The spline layout and the display entities are described in [Spline tracks](trains.md). This page is how to set up train vehicles, lay track and drive.

## Marking a vehicle as a train

```yaml
behaviour:
  rotator: body_controller
  vector: move.movealign
  train:
    locomotive: true
    wheel-diameter: 1.875
    wheel-bones:
      - front_axle
      - rear_axle
    front-connector: connector_front
    back-connector: connector_back
    fuel-cars:
      - coal_car
```

| Key | Meaning |
| --- | --- |
| `front-connector`, `back-connector` | Coupler bones. Optional. A locomotive often has only a back coupler. A car has the coupler that faces the locomotive |
| `fuel-cars` | Vehicle ids whose fuel the locomotive may burn |
| `locomotive` | `true` for a locomotive. See [Locomotive overdrive](#locomotive-overdrive). Default `false` |
| `wheel-diameter` | Blocks across the wheels. See [Wheel animations](#wheel-animations). Default `0` (off) |
| `wheel-bones` | Bones at the frontmost and rearmost axle pivots. See [Track ends](#track-ends) |
| `bogies` | Two bogie bones the car rests on. See [Bogies](#bogies) |
| `walkable` | A deck players can stand on. See [Walkable decks](#walkable-decks) |

Drive keybinds belong on the `ground` state. `A` and `D` should be `JUNCTION_LEFT` and `JUNCTION_RIGHT` when the locomotive should throw switches. Throttle still uses `THROTTLE_UP` and `THROTTLE_DOWN`. Negative engine `min` is reverse.

Sneak and right-click a car, then sneak and right-click the locomotive, to couple them. Spacing along the track is the distance between the coupler bones.

The plugin does not copy the example vehicles. Copy the train YAML you want (`simple_locomotive`, `coal_car`, `passenger_car`, `flat_car`) from [`src/main/resources/vehicles`](https://github.com/TF-Minecraft/VehicleFramework/tree/main/src/main/resources/vehicles) into `plugins/VehicleFramework/vehicles/`, or use the server's own config set. The TFMC configs and models are kept in ServerAssets; there the locomotive, coal car, passenger car and flat car also set `wheel-bones`.

## Wheel animations

With `wheel-diameter` set, the `forward` and `backward` animations of the `ground` state turn the wheels at the speed the train is travelling. Without it, they play as normal move animations.

The two animation lists pair by order: the first `forward` animation with the first `backward` animation, and so on. Each pair must be mirrored looping animations of one full wheel turn. The wheels hold their pose while the train is stopped, and keep it when the train changes direction.

## Bogies

`bogies` names two bogie bones. The car rests on the rail under each, so the body lies along the line between them, and each bogie turns and tilts to follow the rail under it. Each bogie bone must pivot at the bogie's centre, and the body rotator must pivot at the model's origin. The two bones must be at least a quarter of a block apart along the car.

A vehicle's skins share its `bogies` setting, so each skin's model is checked for the bones. A skin built without them is placed as a rigid car. Changing skin sets the bogies up again for the new model; if both models have the bogie bones, the bogies keep their angles.

## Walkable decks

A car with `walkable` has a deck that players can walk on, and players standing on it ride along with the train. The shipped `flat_car` is an open deck with no seats, for riders to stand on. The deck is set in the model's blocks from its origin:

```yaml
walkable:
    x: [-1.5, 1.5]      # across the car
    z: [-4.5, 4.5]      # along it; +z faces the front
    top: 1.3125         # height of the deck
    box-size: 1.5       # optional; default and maximum 3
```

`x`, `z` and `top` are required, and each span must be at least a quarter of a block; otherwise the plugin logs a warning and ignores the deck. `box-size` is also limited to the narrower span.

The deck is made of invisible shulkers, which players can stand on. Minecraft does not rotate their boxes, so on bends they overhang the car's corners a little; smaller boxes overhang less. Clicks and hits on the deck go to the car. Shots pass through the boxes to the car, and explosions do not damage them.

Players are carried up to `walkable.carry-max-speed` in `trains.yml`, 1.0 blocks a tick by default (`0` carries nobody). Faster than that, the deck slides out from under them. The simple locomotive runs at 0.72 blocks a tick, or 0.864 at full overdrive. The boxes are never saved. Any left behind when a car unloads are removed when their chunk loads again.

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

Left-click with the layer item to set the start. Right-click to set the end. A new track is straight in X and Z from start to end. Look direction is ignored. Click solid ground. Grass and plants are refused.

- Click an existing end to extend that track, or to join two tracks into one when the start and end are on different tracks. An extension leaves the end along the track's heading; see [Curves](#curves).
- Ends within `join-distance` (default 1.5) can join. A join that turns more than `max-turn-degrees` (default 35) is refused.
- Joining never turns a train round. If both tracks have trains on them and one would have to run the other way, the join is refused; move a train first.
- A new stroke shorter than `min-lay-distance` (default 8) is refused. Loops are exempt.
- Grade stays flat, then climbs at `desired-grade-degrees` (default 6) and never steeper than `max-grade-degrees` (default 10).
- The corridor is 3 blocks wide and 3 tall. Solids and overlapping track refuse the lay. Plants do not.
- Survival and adventure place one sample every `build.interval-ticks` (default 4) and consume `item-track`. Creative and spectator place the whole stroke at once. `interval-ticks: 0` always places at once.

### Curves

Extending a track keeps its bends local. A stroke curves at `curve-radius` (`trains.yml`, default 32 blocks) and runs straight elsewhere. A stroke too short for that radius curves tighter, down to the sharpest turn that `max-turn-degrees` allows over `min-lay-distance`.

Rows are the block-aligned headings: the four axes and the diagonals.

- A click within half a block of the track's line continues it straight.
- A click just beside the row the rail is on (up to 3 blocks across, within 8 degrees) keeps the rail on its row and shifts it across on a reverse curve just before the click. Laying 1,000 blocks with the end one block over leaves 990 blocks on the row.
- Turning onto a row curves at the corner where the two headings meet, with straight track either side.
- A track end left off the rows turns onto the row first when a corner would leave a long run off it, then shifts across near the click.
- Joining two track ends meets the far track along its own heading, without a kink.

Other clicks lay a single arc from the track's heading. Laying never reshapes existing track.

### Junctions and digging

Right-click existing track with the junction item to start a turnout, then right-click with the layer to lay one branch. Left-click with the layer cancels the pending junction. One branch per junction. To rejoin a line, end a stroke on it: right-clicking on another track part way along adds a junction there, and the new track runs into it along the line. A turnout that ends on another track's free end joins that track. Branches cannot be longer than `max-junction-length` (default 32). Junctions along the same track must be at least `min-junction-spacing` (default 16) apart.

The remover digs a sample. Digging the middle splits the track. Digging the initial turnout lay removes that turnout. Track past that first lay stays. You cannot dig track under a train, or next to a junction when that would remove a turnout a train is on; move the train first. Trains elsewhere on the track stay where they are.

## Driving

Bind a locomotive by driving it onto the track, or with `/vf track bind` while seated or standing within 8 blocks. `/vf track unbind` releases it.

Tickets and the whitelist use the locomotive while cars are coupled.

### Junctions

Hold `A` or `D` to set the next facing turnout within `junction-arm-distance` (default 16) of the leading wheels. Left and right are seen in the direction the train is travelling; when reversing, the last car's wheels lead. The key on the turnout's side sets the branch, and the other key sets the through route. The switch moves at once and chat reports the setting. While the train is stopped, the throttle selects the approach direction; at zero throttle, the train keeps its last direction.

Choose before the first wheels enter. The points then stay locked until the whole train clears, including when the last carriage leads while reversing. Stopping, reversing midway, or saving and loading keeps every coupled car on the same route. Closely spaced junctions keep their own settings while the train spans them. Coming out of a branch follows its connection back onto the main track.

### Track ends

The whole train stops before a checked wheel runs past an open track end, in either direction. A car's checked points are its `wheel-bones` and, when it rests on bogies, its bogie pivots; a car with neither is checked at its centre. Wheel bone positions come from the model and its scale. A car that already overhangs an end can drive back onto the rails. Connected junctions and loop seams are not ends.

A broken segment also stops the train. The train stays on the spline.

### Collision warnings

A locomotive that runs into another train at speed explodes, along with the car it hits. A car on its own with no locomotive explodes the same way when anything runs into it. Trains that meet slower than 3 blocks a second between them, about a fifth of a locomotive's full throttle, bump and stop instead. The anvil sound plays, the captain is told, and the throttle of whichever train was moving into the other drops to 0. Reverse to pull away. Set the speed with `collision.explode-speed` in `trains.yml`; `0` explodes on any contact. Coupled cars without their locomotive pass through each other. Everyone seated on a train heading for a collision is warned at least 30 seconds before it would happen, as long as speeds stay as they are. The first warning flashes a **Collision warning** title, at most once every 10 seconds. A red boss bar then counts down, for example "Oncoming train: collision in 24 s", while an alarm rings. The alarm rings twice as often in the last 10 seconds.

| Warning | Meaning |
| --- | --- |
| Oncoming train | A train is coming the other way on the same line |
| Stopped train ahead | A standing or parked train is on the line ahead |
| Train ahead | You are catching up a slower train, or one joining the line |
| Train closing from behind | A faster train is catching you up |
| Train approaching | Shown to riders of a standing train that another train is heading for |

The forecast assumes switches stay as they are now, including one armed with `A` or `D`. A train whose throttle rose since the last check is assumed to keep opening it at the full rate, a point a tick, up to its throttle limit; any other train keeps its current speed. Opening the throttle therefore brings a warning at the next check (half a second by default) once a collision comes within the look-ahead, but if it is by then less than 30 seconds away, that is the time the warning shows. The limit is 100, or 120 for a healthy locomotive going forwards that is not cooling down from overdrive; a damaged engine is held to its health. A train ahead that is accelerating is also checked at its current speed, in case it stops accelerating. Accelerating therefore shortens the countdown at once, and it lengthens again when the throttle is held steady. The forecast follows the track through junctions and stops at track ends and broken rail.

Cars that have not spawned count where they were last saved: those in unloaded chunks, and those in loaded chunks with no player near enough to spawn them. If digging has since moved or renamed the track under a parked car, the car is found again on the track nearest where it stood. Each such car counts as able to explode, because one that spawns before its locomotive behaves as a car on its own.

A collision counts from when the locomotive comes within `margin` blocks of the other train, a little before it touches, so the countdown runs slightly short. The warning comes at any speed, including for a slow approach that will only bump. Creeping right up to a standing car therefore gives a warning. When pushing cars into a loaded train, the warning is for the locomotive reaching its cars, or the pushed cars reaching its locomotive.

The bar clears 2 seconds after the danger has passed, for example once you stop, reverse or change the switch. Until then it stays up without the alarm, so a forecast near the limit does not flicker. Riders of a standing train keep their "Train approaching" warning until the other train stops or turns away. Players standing on a walkable deck are not warned; only seated riders are.

Settings are under `collision-warning` in `trains.yml`:

| Key | Default | Meaning |
| --- | --- | --- |
| `enabled` | `true` | Turns the warning on |
| `seconds` | `30` | How long before a collision the warning starts |
| `check-ticks` | `10` | Ticks between checks |
| `margin` | `2` | Blocks kept between trains |
| `parked-car-half-length` | `5` | Blocks either side of an unloaded car's saved centre that it covers |
| `sound`, `sound-volume`, `sound-pitch` | `minecraft:block.bell.use`, `1.0`, `1.5` | The alarm |
| `sound-interval-ticks` | `40` | Ticks between alarms, halved in the last 10 seconds |

## Locomotive overdrive

A vehicle with `locomotive: true` leads its train as a locomotive:

- Seated riders anywhere on the train take a quarter of incoming damage, up to 18 per hit. Riders in other vehicles take half, with the same cap.
- With a fully healthy engine, `W` raises the throttle up to 120% (the engine's `max` must allow it). A damaged engine is limited to its health percentage in both directions, so overdrive needs full engine health. Reverse is limited by the engine's `min`.
- Overdrive draws on a shared boost budget that lasts about 20 seconds at 110% or 10 seconds at 120%. Any throttle above 100% spends the same budget.
- Running out of boost, or returning to 100% or below, starts a five-minute cooldown. Throttle up to 100% stays available throughout.
- The scoreboard shows the boost time left, the cooldown, or that overdrive is ready.
- Boost and cooldown are saved with the locomotive. Their timers run in real time, so they include time spent unloaded.

Above 100%, the engine's fuel use per cycle is multiplied by `1 + (throttle - 100)² / 400`. With the shipped simple locomotive (`speed: 0.72`, `fuel-burn-rate: 1.25`, `max: 120`, `min: -100`):

| Throttle | Fuel per cycle | Extra fuel |
| --- | --- | --- |
| 100% | 1.25 | 0% |
| 110% | 1.5625 | 25% |
| 120% | 2.5 | 100% |

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

## Upgrading

Plugin updates never overwrite vehicle YAML or an existing `trains.yml`. Missing `trains.yml` keys use their defaults. Install the plugin before vehicle YAML that uses newer `behaviour.train` keys. Older releases ignore keys they do not know, so the feature silently stays off. Before 2.4.4, a skin without the bogie bones caused errors, so a vehicle with such a skin needs 2.4.4 or later before it lists `bogies`.

| Key or behaviour | First release |
| --- | --- |
| `locomotive` | 2.1.0 |
| `wheel-diameter`, `bogies` | 2.3.0 |
| `walkable`, `walkable.carry-max-speed` | 2.4.0 |
| `wheel-bones` | 2.4.1 |
| Skins without the bogie bones placed as rigid cars | 2.4.4 |
| `curve-radius` | 2.5.0 |
| Saved train facing and per-junction routes | 2.9.0 |

Saves and throttle tapes from earlier releases remain readable. Before downgrading below 2.9.0, restore the matching vehicle-data backup: older releases cannot represent a train facing the opposite way along a track.
