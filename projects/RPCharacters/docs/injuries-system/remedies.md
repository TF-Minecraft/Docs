# Remedies

## Purpose

Remedies instantly cure **healing** injuries only.

## `RemedyListener` changes

In `findCurableTrait`:

- Trait must be in remedy whitelist (unchanged)
- Trait must be healing: `TraitData.hasDuration()` or `InjuryProgressionLoader.isHealingTrait(id)`
- Permanent injuries (`blind`, `one_handed`, `one_legged`, …) → skip

## `items.yml`

```yaml
remedies:
  healing_draught:
    item: v.potion
    traits:
      - broken_arm
      - broken_leg
      - half_blind
```

No permanent ids in list.

## Edge cases

- Consume with no curable healing injury: no effect, do not cancel consume (locked behavior)

## Acceptance

- [ ] Remedy removes healing `broken_arm`
- [ ] Remedy does nothing on `one_handed` or `blind`
- [ ] Clears `trait-state` for removed trait

## Implementation

- `RemedyListener.findCurableTrait` filters by `InjuryProgressionLoader.isHealingTrait` and `current.hasDuration()`
- `RemedyLoader` validates remedy trait ids at load (after traits); skips non-healing entries with warnings
- `remedyLoader.load()` moved after trait/injury loaders in `RPCharacters.loadConfigs()`
