# Vehicle configuration

Each file in `plugins/VehicleFramework/vehicles/` is YAML. The root key is the vehicle id used by `/vf spawn`. One vehicle per file is easier to edit. Several root keys in one file also load.

A short ship looks like this:

```yaml
gunboat:
  name: "§l§eGunboat"
  model: gunboat
  skins:
    gunboat:
      name: "Gunboat"
      model: gunboat
  death:
    template: ship
  behaviour:
    rotator: body_controller
    vector: move.movealign
    float: true
    float-in:
      - WATER
      - KELP
  states:
    floating:
      keybinds:
        W: THROTTLE_UP
        S: THROTTLE_DOWN
        A: TURN_LEFT
        D: TURN_RIGHT
        SHIFT: SEAT_SELECTION
  components:
    hull:
      health: 290.0
      repair-time: 100
      damage-chance: 1.0
      sinkable: true
      armor: wooden
      role: hull_wood
  seats:
    - captain(captain)
```

`name` is the sidebar name. `model` is the default skin id, and that skin's `model` is the ModelEngine model id. `fixed: true` keeps a vehicle in place. `towable: true` lets another vehicle hitch it.

Bones are described in [Models](models.md). Weapons are in [Weapons and ammunition](weapons.md). Shared death, armor, and weapon blocks are in [Templates](templates.md).

## States

A vehicle has up to three states: `ground`, `floating`, and `flying`. Each state has its own `keybinds` and `animations`.

Animation names:

| Key | Plays when |
| --- | --- |
| `default` | The state is active |
| `forward`, `backward`, `up`, `down`, `left`, `right` | Moving that way |
| `engine_active` | The engine is running |
| `explode`, `sink`, `crash`, `die` | That death type starts |
| `reload`, `shoot` | A weapon reloads or fires |

Keys you can bind:

`W`, `A`, `S`, `D`, `SPACE`, `SHIFT`, `SWAP` (offhand swap, usually F), `LEFT_CLICK`, `RIGHT_CLICK`, plus `SHIFT_` or `SPACE_` combined with `W`/`A`/`S`/`D` or a click.

Actions you can bind them to:

| Action | Effect |
| --- | --- |
| `THROTTLE_UP`, `THROTTLE_DOWN` | Change throttle |
| `TURN_LEFT`, `TURN_RIGHT` | Turn in world yaw |
| `TURN_LEFT_LOCAL`, `TURN_RIGHT_LOCAL` | Turn in the vehicle's local frame |
| `JUNCTION_LEFT`, `JUNCTION_RIGHT` | Arm a railroad switch |
| `FORWARD`, `BACKWARD`, `UP`, `DOWN`, `MOVE` | Direct movement |
| `PITCH_UP`, `PITCH_DOWN`, `ROLL_LEFT`, `ROLL_RIGHT` | Aircraft attitude |
| `WEAPON_UP`, `WEAPON_DOWN`, `WEAPON_LEFT`, `WEAPON_RIGHT` | Aim |
| `WEAPON_SHOOT`, `WEAPON_RELOAD`, `WEAPON_RELOAD_AND_SHOOT`, `WEAPON_SWITCH` | Fire, reload, or change weapon |
| `SEAT_SELECTION` | Open the seat menu |
| `LIGHTS`, `HORN` | Lights and horn, if `utilities` defines them |
| `NONE` | Ignore the key |

`switch-parameters` on a state explode the vehicle if it enters that state outside the listed bounds. Values are `min,max`:

```yaml
ground:
  switch-parameters:
    velocity:
      y: -1.0,1.0
    rotations:
      pitch: -15.0,15.0
      roll: -15.0,15.0
```

`terrain-follow: true` on a state makes a ground vehicle follow the blocks under it. Optional tuning keys are `step-height`, `snap-speed`, `climb-lead-ticks`, `climb-lead-factor`, `air-gravity`, `air-drag`, and `ground-probes`. Trains do not use this. They follow spline track.

`break: true` on a state brakes the vehicle and ignores drive input while that state is active. The small car uses this on `floating` so it stops in water.

## Behaviour

| Key | Meaning |
| --- | --- |
| `rotator` | Controller bone |
| `vector` | `bone.bone` forward vector |
| `secondary-rotators` | Extra bones the plugin may rotate |
| `turn-scaling` | Scale turn rate with speed. Default `true` |
| `float` | Sit on fluids |
| `float-in` | Material names. Defaults to water when omitted |
| `rotation-targets` | Pitch, yaw, or roll goals while conditions match |
| `train` | Present on locomotives and cars. See [Trains](using-trains.md) |

A rotation target sets `pitch`, `yaw`, and `roll` in degrees and an `interval` for how fast it gets there. Every condition in the list must match. `OR(...)` and `AND(...)` group checks with `;` between them.

Condition names: `state(ground)`, `lift(true)`, `passengers(true)`, `seat_filled(bone)`, `seat_empty(bone)`, `is_passenger(true)`, `has_fuel(true)`, `throttle_less_than(10)`, `throttle_more_than(10)`, and `health_percent(hull;less_than=25)`.

## Components

The component key is the type. A vehicle has one of each type. `steering` is not loaded.

| Component | Role |
| --- | --- |
| `hull` | Main health. `sinkable: true` lets a ship sink |
| `engine` | Throttle, speed, fuel |
| `geared_engine` | Several gears instead of one throttle range |
| `wings` | Lift from speed. `lift` scales with health |
| `balloon` | Lift for airships. `lift` scales with health |
| `pump` | Counters sinking. `power` is the pump strength |
| `harness` | `mount-bones` and `turn-rate` for draft animals |

Shared component fields: `health`, `repair-time` (ticks), `damage-chance` (0 to 1), `alias`, `fatal`, `vfx`, `armor`, `role`, and an optional `damage` overlay. Damage numbers are multipliers for a hit type. With `armor` or `role` set, those templates merge and a local `damage` map overrides them. Without templates, `damage` is a list of `type(amount)` entries.

Engine fields: `max` and `min` throttle (negative `min` is reverse), `speed` at full throttle, `turn-rate`, `requires-start`, `fuel`, `fuel-capacity`, `fuel-burn-rate`, and `refuel-states`. Sounds and particles on the engine play while it runs. `particle-bones` is a list of `bone.bone` vectors.

A geared engine uses a `gears` list. Each gear has `name`, `max`, `min`, `speed`, and `acceleration`. `start-gear` picks the initial gear.

## Seats

```yaml
seats:
  - captain(driver)
  - mechanic(mechanic)
  - gunner(front_gunner)
  - passenger(passenger_1)
  - entity(skeleton_seat)
```

The word before the parenthesis is the seat type. The word inside is the ModelEngine mount bone name. A weapon's `seat` uses that same bone name. The shipped gunboat keeps the cannon on a `passenger` seat. Use `gunner` when you want the seat type to say so.

`entity-seat-whitelist` lists who may sit in an entity seat. `v.skeleton` is a vanilla mob. `mm.SkeletonBoss` is a MythicMobs id. The `mm.` prefix is case-sensitive.

## Death

`death` is either written in full or pulled from a template. Types are `explode`, `sink`, and `crash`. `die` is the fallback animation name.

`duration` is how many ticks the wreck stays. `fragments` on `explode` is how many pieces are thrown. Those pieces can ignite other vehicles. `sounds` uses the same sound entries as weapons.

An override swaps the death type when its conditions match. The biplane uses this so a flying wreck uses `crash` instead of exploding in the air:

```yaml
death:
  template: explode_medium
  explode:
    overrides:
      crashing:
        type: crash
        conditions:
          - state(flying)
  crash:
    nop: true
```

`nop: true` means that death block has no extra settings.

## Containers, lights, and towing

```yaml
containers:
  hold:
    name: "Hold"
    size: 27
    seat: captain
    bones:
      - cargo
    allow-items:
      - m.utils.cannonball

utilities:
  horn:
    sound: minecraft:block.note_block.bell
    volume: 1.0
    pitch: 1.0
  lights:
    headlight:
      vector: light.lightalign
      power: 8
      falloff: 1

towing:
  bone: tow_connection
  reversed: false
```

A container opens when a player who is already in `seat` right-clicks the vehicle. `allow-items` limits what it accepts. `size` is the inventory size. Light `power` is a block light level from 1 to 15 (default 8). `vector` is a `bone.bone` pair aimed the way the light points.

`custom-effects` plays a short script on engine start, engine stop, fire, and death. The keys are `engine_start`, `engine_start_fail`, `engine_stop`, `fire_start`, `crash`, `explode`, `sink`, and `die`. Each entry is a list of steps such as `sound(bone;namespace:sound;volume;pitch)` and `delay(20)`. The small car in the repository is a full example.

`towable: true` on the pulled vehicle and `towing` on the pulling vehicle are both required.
