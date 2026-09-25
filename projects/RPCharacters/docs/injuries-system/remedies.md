# Healing injuries and surgery

Instant remedies are gone. A healing injury recovers over time, or a physician removes it with Surgery.

## What can be treated

`HealingInjuries` returns traits that have a duration and are injury keys. Permanent injuries such as `one_handed`, `one_legged`, and `blind` are excluded.

| Method | Effect |
|---|---|
| `HealingInjuries.list(player)` | Healing injuries on the active character |
| `HealingInjuries.cure(player, traitId)` | Removes the injury and sends its lost message |
| `HealingInjuries.extend(player, traitId, extraMs)` | Adds time to the remaining duration |

Surgery is the only treatment plugin. It cures on a successful operation and extends the duration when a surgery fails after the patient was sedated or cut.

## Acceptance

- [ ] A successful surgery removes `broken_arm`, `broken_leg`, or `half_blind`
- [ ] Surgery cannot see or remove a permanent injury
- [ ] A failed surgery after the patient was sedated or cut leaves the injury in place with a longer remaining time
