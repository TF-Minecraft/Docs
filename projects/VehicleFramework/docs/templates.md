# Templates

Templates are shared YAML so each vehicle does not repeat the same cannon, hull armor, or sinking wreck. They load from `plugins/VehicleFramework/templates/`. A vehicle or weapon sets `template: <id>`, where `<id>` is the root key inside a template file. Keys written on the vehicle override the template.

The plugin copies the shipped templates on first run if those files are missing. Later edits in the jar do not replace files already on disk.

## Death

`templates/death/` holds `explode`, `sink`, and `crash` blocks. [`ship.yml`](https://github.com/TF-Minecraft/VehicleFramework/blob/main/src/main/resources/templates/death/ship.yml) is the usual ship wreck: an explosion with fragments, then a sink. `explode_small`, `explode_medium`, and `explode_large` are shorter blast deaths.

```yaml
death:
  template: ship
```

Add an `explode` or `crash` section under `death` when one vehicle needs an override the template does not have. See [Configuration](configuration.md).

## Armor and roles

`templates/armor/` is the base damage map for a material, such as `wooden` or `armored`. `templates/roles/roles.yml` is the per-part map, such as `hull_wood` or `engine_aircraft`. A component names both:

```yaml
hull:
  armor: wooden
  role: hull_wood
  damage:
    cannonball: 2.0
```

The plugin merges armor, then role, then the local `damage` map. A later layer replaces the same damage id. Values are multipliers. `FALL: 0.0` means fall damage does not hurt that component.

Damage ids used by the shipped ammunition include `bullet`, `cannonball`, `small_bomb`, `torpedo`, and `clusterbomb`, plus Bukkit sources such as `entity_attack`, `projectile`, and `entity_explosion`.

## Weapons

`templates/weapons/` holds a full weapon body: reload time, accepted ammunition, keybinds, and shoot particles. A vehicle weapon names the template and then sets the seat and bones for that model:

```yaml
naval_gun:
  template: naval_cannon
  seat: front_gunner
  body-bone: gun_body
  head-bone: gun_rotator
  bones:
    - exit.exitalign
```

Shipped weapon templates are `naval_cannon`, `gun_turret`, `aa_turret`, `flak_cannon`, and `autocannon`. Duplicate template ids keep the first file loaded and log a warning.
