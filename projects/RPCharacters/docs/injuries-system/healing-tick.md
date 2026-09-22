# Healing tick

## Purpose

Decrement healing duration while player is online with the injury on the active character.

## `InjuryHealingService`

- Runs at the interval configured in `injuries.yml`
- For each online player with active character:
  - For each owned trait with `duration` in YAML:
    - Subtract elapsed ms from `duration-remaining-ms`
    - If `<= 0`: remove trait, lost message, update integrator, clear state
    - Else: `character.update()` if progress crossed int threshold (optional optimization: only on minute boundaries)

## Tick rules

- **Only** when character is active (`character.isActive()`)
- **Only** while player online
- Inactive characters or offline: duration frozen

## Configuration (`injuries.yml`)

```yaml
healing-tick-interval: 1m
```

Default 1 minute if omitted.

## Acceptance

- [ ] Active character heals over time; inactive does not
- [ ] Fully healed injury removed with lost message
- [ ] Attribute penalties decrease as duration decreases

## Implementation

- `healing-tick-interval: 1m` in `injuries.yml`, read by `InjuryPoolLoader`
- `InjuryHealingService` repeating task: decrements `duration-remaining-ms`, removes healed traits with lost message, refreshes integrator on active characters
- Started from `PlayerManager.start()`
