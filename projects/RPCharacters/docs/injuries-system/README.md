# Injuries, healing and prosthetics

Healing injuries carry remaining duration; permanent injuries can have configured
prosthetic replacements. State belongs to the character. Death-zone handling
rolls permadeath first, then converts healing injuries or selects a new injury.
Prosthetics are excluded from the injury risk count.

The maintained references describe the current source on `main`:

| Reference | Contents |
| --- | --- |
| [Configuration](config-and-loaders.md) | YAML schema and loaders |
| [Trait persistence](trait-state-persistence.md) | Duration, fuel and saved identifiers |
| [Trait effects](trait-runtime-effects.md) | Scaling and powered/depowered variants |
| [Permadeath](permadeath-flow.md) | Death order, progression and risk |
| [Healing](healing-tick.md) | Active-character duration and completion |
| [Surgery](remedies.md) | Healing injuries are treated by Surgery |
| [Prosthetic installation](prosthetics-install.md) | Install, swap and confirmation |
| [Prosthetic fuel](prosthetic-fuel.md) | Burn, refuel and effects |
| [Character creation](creator-stages.md) | Injury/prosthetic selection |
| [Web catalog](web-catalog-sync.md) | ProvinceSystem contract |
| [Content and saved data](content-and-migration.md) | Trait definitions and compatibility |
| [Verification](verify-and-deploy.md) | Test matrix and rollback |

Checklists describe checks to run, not a claim that a release passed them.
