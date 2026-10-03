# CompanionPets staff commands

[CompanionPets](../README.md) · [All projects](../../../README.md)

All commands are staff-only. The command is `/companionpets`; there are no other
root aliases. Running `/companionpets` shows help and examples.

| Command after `/companionpets` | Purpose |
| --- | --- |
| `reload` | Reload config and refresh models. Provider problems are logged automatically. |
| `moment <affection/bark/mischief/dig/belly>` | Trigger a moment while looking at your pet; normal care and animation conditions apply. |
| `testpet <type> [name...]` | Spawn a normal pet with every compatible trick learned. No special marker, pause state or cleanup category. |
| `list <player> [pet name...]` | Open that player's pets or a selected pet's read-only profile. Console gets readable names. |
| `find <player> [pet name...]` | Show shelter, current or last-known location, and missing or duplicate bodies for that player's pets, without loading chunks. |
| `create <player> type=<type> name=<name...> [option=value ...]` | Create a new saved replacement in the owner's shelter. |
| `egg <type/all> [online-player] [1..64]` | Give configured eggs; omit the recipient in game to receive them yourself. |

```text
/companionpets list Nowko
/companionpets find Nowko Toby
/companionpets create Nowko type=beagle name=Toby tricks=all
/companionpets create Nowko type=beagle name=Toby de prueba tricks=follow,sit:sientate,lay:duerme hunger=80 mood=90 energy=70 cleanliness=100 health=100 bond=60 sex=male personality=friendly agehours=48
/companionpets egg all
/companionpets testpet frog Rana
/companionpets moment belly
```

## Browsing players and pets

Tab completion suggests player names first, then only that player's pet names.
Names can contain spaces. Duplicate pet names are never resolved arbitrarily:
select the pet from `list` to view its identity internally. There is no player
inventory: select the owner using command completion.

The selected pet's staff inventory shares the normal pet profile: species,
name, sex, age, needs, bond, personality, favourite toy and learned tricks. It
is read-only, including its trick inventory; renaming, calling, shelter and
release actions are omitted. No UUIDs or audit snapshots are required or shown
in command help, completion or pet cards. Menu layout and navigation are
described in the [gameplay guide](gameplay.md#menus).

## Creating pets

`create` makes a new identity. It accepts tricks, the five needs, bond, sex,
personality and `agehours`. Named parameters can appear in any order. Names may
contain spaces up to the next `parameter=value`. Tab after the owner immediately
offers `type=` and `name=` examples, plus optional parameters; Tab after `=`
suggests suitable values. Previously supplied keys disappear from suggestions.
Trick suggestions use the selected type and exclude IDs already included in a
comma-separated list. The earlier positional type/name syntax remains accepted
for compatibility.

`tricks` is a comma-separated list of IDs or `ID:word`, learned at 100% in
addition to configured default tricks. `tricks=all` teaches every compatible
enabled trick; `tricks=none` adds no extra tricks. Defaults: needs 100, bond 0,
male, new age, generated personality.

An explicitly supplied owner UUID is still accepted for reconstruction of an
unknown or offline player; ordinary browsing and completion use player names.
Creation validates options before writing and checks shelter capacity. The owner
takes the created pet out through their shelter menu.

## Test pets and moments

`/companionpets testpet <type> [name]` spawns any configured pet with all
compatible tricks learned at 100%, including its custom tricks. `type` is the key
under `pets` in the active config; tab completion lists these keys. For example,
`/companionpets testpet beagle Toby` or `/companionpets testpet frog Rana` (with
`tongue` and `croak` configured). Only enabled tricks are included; custom tricks
need a usable animation or text fallback. The spawn message lists the bound
words; look at the pet and say a word or use the pet name and word, such as
`Rana tongue`. These are ordinary saved pets: active-pet limits and care needs
still apply. Pets created with `testpet` learn the word `lay`.

Look at a pet and use `/companionpets moment dig` to show a find. `/companionpets
moment belly` triggers the [belly rub moment](gameplay.md#belly-rub-moment)
without the chance roll or cooldown. The pet must still meet the health and
activity requirements and have all three model clips.

Old `test-pet` and `test-frozen` save fields are ignored and disappear on save;
previously marked or paused pets resume their normal behaviour.

## Eggs

MMOItems eggs dispatch `mi give TYPE ID PLAYER AMOUNT` from console; they are not
also inserted via the API. Vanilla and ItemsAdder eggs retain their identity.
All selected egg IDs are checked before delivery. See the
[MMOItems command documentation](https://docs.phoenixdevt.fr/mmoitems/general/commands.html).

## Reloading configuration

`/companionpets reload` applies edits to `config.yml` without restarting the
server. The command checks the YAML and keeps the current settings if a saved
pet type would disappear. Active ModelEngine appearances are reapplied; open pet
menus and pending training prompts are closed. Changing a pet's underlying
entity type takes effect when that pet is summoned again.

## Permissions

The [plugin descriptor](https://github.com/TF-Minecraft/CompanionPets/blob/main/src/main/resources/plugin.yml)
defines all permissions; each defaults to operators.

| Permission | Grants |
| --- | --- |
| `companionpets.staff` | All staff commands and inventory browsing. |
| `petcompanions.staff` | Alias of `companionpets.staff`, retained for existing permission assignments. |
| `companionpets.admin` | All staff management: reload, list, create, find and egg. |
| `companionpets.reload` | `reload` |
| `companionpets.admin.list` | `list` |
| `companionpets.admin.create` | `create` |
| `companionpets.admin.locate` | `find` |
| `companionpets.admin.giveegg` | `egg` |
| `companionpets.test` | `testpet` and `moment` only. |

Inventory permissions are checked again when clicked.

## Audit

Staff interventions are audited privately to
`plugins/CompanionPets/staff-audit.yml.log`. An unavailable audit or persistence
store refuses mutations. Deletion uses the durable identity journal described in
[Saved data and recovery](saved-data.md).
