# Weapons and ammunition

Weapons live under `weapons` on a vehicle, or in `templates/weapons/` and referenced with `template`. Ammunition files live in `plugins/VehicleFramework/ammunition/`. The file name does not matter. The root key is the ammunition id.

Bone setup is in [Models](models.md).

## A weapon on a vehicle

```yaml
weapons:
  naval_gun:
    name: "§eFront Cannon"
    template: naval_cannon
    seat: front_gunner
    body-bone: gun_body
    head-bone: gun_rotator
    head-axis: x
    rotation-limits:
      min-yaw: -120
      max-yaw: 120
      min-pitch: -60
      max-pitch: 20
    bones:
      - exit.exitalign
    animations:
      shoot:
        - shoot
```

The seat value is the mount bone of the player who aims and fires. Keybinds on the weapon replace driving keys for that seat. The shipped gunboat puts the cannon on a passenger seat named `front_gunner`.

| Key | Meaning |
| --- | --- |
| `template` | Merge a weapon template under this weapon. Local keys win |
| `fixed` | No yaw and pitch bones |
| `health`, `repair-time` | Weapon component health. Default health is 100 |
| `turn-rate` | How fast the turret turns. Default 0.5 |
| `aim-mode` | `manual` (default) or `cursor` |
| `cursor-range` | How far cursor aim looks. Default 80 |
| `aim-vector` | Optional vector bone used when aiming |
| `reload-time` | Ticks to reload. Default 4 |
| `cooldown` | Ticks between shots. Default 10 |
| `delay` | Ticks after the key press before the shot leaves. The animation starts immediately |
| `accepted-ammunition` | Ammunition ids this weapon loads |
| `bones` | One or more `exit.exitalign` vectors. Each one needs its own round |
| `damage` | `type(amount)` multipliers for hits on the weapon |

At 0% weapon health, reload time scales up by `weapon-degraded-reload-multiplier` in `config.yml` (default 2). The scale is linear between full health and empty.

`aim-mode: cursor` aims at the block or entity the gunner is looking at, out to `cursor-range`. `weapon-aim-debug: true` in `config.yml` draws the aim point while you tune it.

These keys on the weapon override the same values on the ammunition: `projectile-damage`, `projectile-damage-type`, `projectile-speed` (or `projectile-velocity`), `projectile-yield`, `projectile-radius`, `projectile-explosive`, and `projectile-cluster-amount`.

`data` holds shoot and reload sounds plus muzzle particles. See the sound and particle shapes below. The shipped naval cannon template is a full example in [`templates/weapons/naval_cannon.yml`](https://github.com/TF-Minecraft/VehicleFramework/blob/main/src/main/resources/templates/weapons/naval_cannon.yml).

## Ammunition

`type` is `cannonball`, `bullet`, `cluster`, `torpedo`, or `bomb`.

| Field | Use |
| --- | --- |
| `input` | TLibs item path consumed from the gunner's inventory |
| `rounds` | How many shots one item contains. Bullets use this as a magazine |
| `damage`, `damage-type` | Hit strength and the damage id armor templates match |
| `yield`, `radius` | Explosion size |
| `explosive`, `fire` | Whether the hit explodes and whether it lights blocks |
| `fuse` | Ticks before a bomb or torpedo detonates |
| `amount`, `spread` | Cluster submunitions |
| `range` | Bullet travel distance |
| `potion-effects` | Effect entries applied on hit |
| `model` | `type: item` with `material`, `small`, and `model-data`, or a ModelEngine model |

`sounds`, `particles`, and `hit-sfx` / `hit-vfx` use the shapes below. A sound may set `delay` and `pitched: true`.

`/vf ammo` gives every loaded ammunition item to a player with `vehicleframework.spawn`. The `input` items still have to exist on the server.

## Sounds and particles

```yaml
sound:
  sound: minecraft:entity.generic.explode
  pitch: 1.0
  volume: 6.0

particle1:
  particle: FLAME
  amount: 70
  spread: 0.2
  speed: 1.2
```

`sound` is a namespaced sound, including sounds from your resource pack. `particle` is a Bukkit particle name. Particles on a weapon or engine spawn along that section's vector bones.
