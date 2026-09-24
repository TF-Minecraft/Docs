# Trait state persistence

## Purpose

Persist per trait instance state on characters and migrate missing fields on load.

## Trait ids

| Id | Type |
|----|------|
| `one_handed` | permanent arm loss |
| `one_legged` | permanent leg loss |
| `broken_arm` | healing arm injury |
| `broken_leg` | healing leg injury |
| `half_blind` | healing |
| `blind` | permanent |

Progression: `broken_arm` → `one_handed`, `broken_leg` → `one_legged`, `half_blind` → `blind`.

No JSON trait id rewriting. Saved `one_handed` stays `one_handed`.

## Data model

`RPCharacter` field:

```java
Map<String, TraitInstanceState> traitState; // keyed by trait id (lowercase)
```

`TraitInstanceState`:

| Field | Type | Used by |
|-------|------|---------|
| `durationRemainingMs` | long | Healing injuries |
| `fuel` | double | Fueled prosthetics |

## Database (`Database.java`)

**Save** character JSON:

```json
"trait-state": {
  "broken_arm": { "duration-remaining-ms": 172800000 },
  "arcane_prosthetic_arm": { "fuel": 42.5 }
}
```

**Load:**
1. Parse `trait-state` or default `{}`
2. For each trait on character, apply defaults (see below)
3. No trait id migration in Database

## Defaults on load

| Trait type | Missing state |
|------------|---------------|
| Healing (`duration` in YAML) | `duration-remaining-ms` = full duration from trait def |
| Fueled prosthetic | `fuel` = `fuel-capacity` from trait def |
| Other | no state entry required |

## API on `RPCharacter`

- `getTraitState(traitId)`, `setDurationRemainingMs`, `setFuel`, `removeTraitState`
- `initializeTraitState` on `addTrait`, clear on `removeTrait`
- `ensureTraitStateDefaults()` after load

## Acceptance

- [ ] Old characters without `trait-state` load cleanly
- [ ] Round trip save/load preserves duration and fuel
- [ ] Saved `one_handed` / `one_legged` ids resolve without JSON rewrite
