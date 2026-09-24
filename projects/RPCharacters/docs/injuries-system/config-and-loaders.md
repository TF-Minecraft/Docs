# Config and loaders

## Purpose

Define YAML schemas and load them at plugin startup.

## Resource files

### `fuel-templates.yml`

```yaml
arcane_fuel:
  item: m.miscellanea.arcane_fuel
  amount-per-item: 50
  burn-rate: 1
  burn-interval: 1h
```

### `injury-progression.yml`

```yaml
progression:
  broken_arm: one_handed
  broken_leg: one_legged
  half_blind: blind
```

### `prosthetics.yml`

```yaml
replacements:
  one_handed:
    wooden_claw_arm: m.utils.wood_claw_arm
    basic_prosthetic_arm: m.utils.iron_claw_arm
    arcane_prosthetic_arm: m.utils.arcane_claw_arm
  one_legged:
    pegleg: m.utils.wood_claw_leg
    basic_prosthetic_leg: m.utils.iron_claw_leg
    arcane_prosthetic_leg: m.utils.arcane_claw_leg
```

### `traits/prosthetic-traits.yml`

Six prosthetic traits with `key: prosthetic`, tiered modifiers, arcane entries with `fuel-template`, `fuel-capacity`, `powered` / `depowered` sections.

### `injuries.yml`

Pool lists **healing** trait ids only (`broken_arm`, `broken_leg`, `half_blind`).

### `traits/injury-traits.yml`

Healing and permanent traits form progression pairs. Healing traits include `duration`; saved permanent IDs remain valid.

## Trait YAML extensions (`TraitLoader` / `TraitData`)

| Field | Type | Notes |
|-------|------|-------|
| `duration` | duration string | Healing only; parsed by `DurationParser.parseLockTimeMs` |
| `fuel-template` | string | Prosthetic only |
| `fuel-capacity` | double | Prosthetic only |
| `powered` | section | name override, description, attribute-modifiers, potion-effects |
| `depowered` | section | same shape |

## Loaders

| Loader | Registry API |
|--------|----------------|
| `FuelTemplateLoader` | `getByString(id)`, `getByItem(path)` |
| `InjuryProgressionLoader` | `getPermanentId(healingId)`, `isHealingTrait(id)` via trait duration |
| `ProstheticLoader` | `getReplacement(injuryId)`, `getReplacementForProsthetic(prostheticId)`, `resolveForItem(item)` |

## Bootstrap (`RPCharacters.java`)

- `createConfigs()` / `createFolders()`: copy missing bundled yml files
- `loadConfigs()`: loads these loaders after traits

## Acceptance

- [ ] `/rpcharacter reload` loads all files without warnings
- [ ] Invalid progression target logs warning and skips entry
- [ ] Prosthetic trait keys map to install item paths
