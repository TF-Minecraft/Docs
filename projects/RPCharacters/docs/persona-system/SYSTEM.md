# Persona, identity and chat

RPCharacters owns character identity, aliases, name colours, masks, profiles,
chat, dice rolls and calendar-based ages. Build from `main`; command routing and
configuration are defined by the source and bundled YAML files.

## Identity

[DisplayIdentityService](https://github.com/TF-Minecraft/RPCharacters/blob/main/src/main/java/net/tfminecraft/rpcharacters/identity/DisplayIdentityService.java)
provides distinct views of the character:

| View | Behavior |
| --- | --- |
| Character name | Stored character name |
| Effective plain name | Character alias or name |
| Tab display | Coloured alias/name; ignores masks and temporary aliases |
| Safe display | Uses a facade when the active character is hidden |
| Chat display | Mask first, then temporary alias, then coloured alias/name |

Use `%rpcharacters_display_safe%` for TAB. A real active-character display is not
safe for TAB when hidden characters are enabled. No-character rendering follows
`persona.yml` and the calling context.

## Configuration

| File | Purpose |
| --- | --- |
| `persona.yml` | Identity validation and defaults |
| `profile.yml` | Character-menu slots and limits |
| `profile-view.yml` | Profile output |
| `permission-groups.yml` | Rank limits and character-switch cooldowns |
| `chat.yml` | Channels, formats, ranges, permissions and character requirements |
| `masks.yml` | Mask item matching and display label |
| `custom-masks.yml` | Approved custom 3D masks written by ArmourShop (`ia.{namespace}:{slug}`) |
| `rolls.yml` | Dice limits and attribute modifiers |
| `calendar.yml` | Season calendar and age rules |
| `races.yml` | Race definitions and age limits |

Character identity and birthday belong to character data. Switch cooldowns use a
wall-clock timestamp on the player; current rank settings determine eligibility.
Temporary aliases are session state. Name colours use TLibs formatting.

## Commands and integration

`/rpcharacter` handles profile and persona operations, including alias,
namecolour, gender, description, temporary alias and hidden-character controls.
Channel commands come from `chat.yml`. `/channel` selects the default channel;
`/channeltoggle` controls visibility. `/roll` supports numeric and attribute rolls.

Channel permissions, character requirements and recipient rules are enforced by
the chat services. Masks affect eligible chat/profile views; account-name channels
and safe TAB identity have separate rules. Profiles enforce target and permission
checks before rendering.

`CharacterChatEvent` and `CharacterProfileViewEvent` expose integration hooks.
Conversation tracking consumes character-chat events. Profile placeholders expose
name, display, age, race, gender and description for other plugins.

See [validation and operations](RUNBOOK.md) for configuration checks and smoke tests.
