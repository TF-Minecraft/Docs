# Web catalog sync

## Purpose

ProvinceSystem character creator catalog matches in game permanent injury and prosthetic stages.

## `CreationCatalogSyncService`

| Trait | Include in catalog? |
|-------|---------------------|
| Healing injuries (`duration` set) | No |
| Permanent injuries (no `duration`, `key: injury`) | Yes |
| Prosthetics (`key: prosthetic`) | Yes |
| Runtime only | No |

## Payload fields

Each eligible trait includes:

- `id`, `name`, `key`, `cost`, `description`, `mutually_exclusive`
- `has_duration` for duration metadata
- `fuel_disclaimer` derived from the fuel template; mapped prosthetics also expose `replaces_injury`

## Stage sync

- Export new creator stages with same `min-select`, `max-select`, `points` as `stages.yml`
- Web applies: permanent injuries 0 cost multi select, prosthetic 1 point single select, both optional

## ProvinceSystem frontend

- Render permanent injury multi pick
- Render prosthetic single pick with point cost
- Skip buttons on both steps
- Arcane disclaimer text

Keep the plugin catalog and frontend selection rules aligned.

## Acceptance

- [ ] Web catalog lists permanent injuries and prosthetics only
- [ ] Point rules match in game
- [ ] Created character from web has same traits and `trait-state` as in game
