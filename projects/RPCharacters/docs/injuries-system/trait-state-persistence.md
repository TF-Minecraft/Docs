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
| `expiresAtMs` | long | Healing injury expiry in epoch milliseconds |
| `fuel` | double | Fueled prosthetics |

## Database (`Database.java`)

**Save** character JSON:

```json
"trait-state": {
  "broken_arm": { "expires-at-ms": 1791633600000, "duration-remaining-ms": 172800000 },
  "arcane_prosthetic_arm": { "fuel": 42.5 }
}
```

`duration-remaining-ms` is also written as a compatibility snapshot; `expires-at-ms` is authoritative for current readers.

**Load:**
1. Parse `trait-state` or default `{}`
2. Prefer `expires-at-ms`; legacy `duration-remaining-ms` starts a new expiry from load time.
3. Apply missing-state defaults, and remove expired duration traits on inactive characters.
4. No trait id migration in Database.

## Defaults on load

| Trait type | Missing state |
|------------|---------------|
| Healing (`duration` in YAML) | Expiry = current time + full duration from trait definition |
| Fueled prosthetic | `fuel` = `fuel-capacity` from trait def |
| Other | no state entry required |

## API on `RPCharacter`

- `getTraitState(traitId)`, `setDurationRemainingMs`, `setDurationExpiresAtMs`, `setFuel`, `removeTraitState`
- `initializeTraitState` on `addTrait`, clear on `removeTrait`
- `ensureTraitStateDefaults()` after load

## Acceptance

- [ ] Old characters without `trait-state` load cleanly
- [ ] Round trip save/load preserves expiry and fuel; remaining time continues to decrease
- [ ] Saved `one_handed` / `one_legged` ids resolve without JSON rewrite
