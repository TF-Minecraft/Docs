# CompanionPets configuration

[CompanionPets](../README.md) · [All projects](../../../README.md)

The default configuration is
[`src/main/resources/config.yml`](https://github.com/TF-Minecraft/CompanionPets/blob/main/src/main/resources/config.yml).
Pet types are covered in [Pet types and ModelEngine](models.md).

Existing `config.yml` files are not overwritten when the plugin updates. Add new
sections, such as `moments.belly-up`, manually when you want to tune them. Use
`/companionpets reload` to apply edits without restarting the server; see
[Staff commands](staff.md#reloading-configuration).

## Species and pets

A new pet usually needs only a species, a model and an egg:

```yaml
pets:
  beagle:
    species: dog
    model: beagle
    egg: "mmoitems:PETS:PET_BEAGLE_EGG"
```

The `pets` key is the saved type ID and the name shown in menus; keep it stable
once pets exist. Two species are built in: `dog` (WOLF body) and `cat` (CAT body).
Each supplies its body, native voice, the eight built-in tricks and its behavior
profile. Only WOLF and CAT bodies are supported, because they provide native
following; types with other entities are skipped and their saved pets kept.

Define other animals, or adjust the built-ins, under `species`. A species accepts
the same shared fields as a pet: `entity`, `behavior`, `voice`/`sounds`, `tricks`,
`default-tricks`, `animations`, appearance settings, `items`, `sex` and
`native-combat`. A pet overrides any inherited field. Mappings merge by key,
ordinary lists replace the inherited list, and a species cannot inherit another
species. Unknown species are logged and the pet is skipped.

```yaml
species:
  frog:
    entity: WOLF          # body: navigation and native AI only
    behavior: basic       # character, independent of the body
    voice: frog           # sounds, independent of the body
    tricks: [follow, come, stay, jump, lay, tongue, croak]
    animations: {lie: lay, sleep: lay}
pets:
  frog:
    species: frog
    model: frog
    egg: "mmoitems:PETS:PET_FROG_EGG"
```

`model: <id>` is a shortcut for a ModelEngine appearance at scale 1, and top-level
`animations` is a shortcut for `appearance.animations`; see
[Pet types and ModelEngine](models.md). Pets without `species` still load with
their own `entity` and the profile of that body.

## Behavior profiles

Spontaneous behavior is not configured action by action. Each species or pet
chooses `behavior: dog`, `cat` or `basic`; without it, the body decides
(WOLF → `dog`, CAT → `cat`). An unknown profile logs a warning listing the three
choices and uses the body's profile. Old `behaviors` lists are ignored with a
single warning.

Every pet comes over to welcome its owner, gets excited about toys and fetches,
greets and sniffs other pets and makes friends, reacts to petting and remembers
who cares for it. The profiles differ in how emotion is shown:

| Profile | Character | For | How it shows emotion | On its own |
| --- | --- | --- | --- | --- |
| `dog` | Exuberant | Dogs and dog-like animals | Wags its tail, jumps, circles the owner and shuffles eagerly in front of a held toy. Chases and protests at other pets; rolls over for belly rubs. | Digs up gifts and makes mischief, such as pulling up plants. |
| `cat` | Restrained | Cats and cat-like animals | No tail wagging or happy jumps. A calmer, chattier greeting. Stalks an uncontested thrown toy and pounces on it. Chases and protests at other pets; rolls over for belly rubs. | Digs up gifts and makes mischief. |
| `basic` | Neutral | Any other animal: frogs, rabbits, birds… | Small hops and excited sounds only. No circling, tail, stalking, chasing or belly rubs. | Nothing. |

Choose `basic` for an animal that is neither dog-like nor cat-like. Sounds come
from the pet's voice, so a fox with the `cat` profile greets with fox sounds at
the cat's rhythm. Gestures the model cannot animate are disabled automatically:
tail gestures need a tail bone, and belly rubs need their three clips. See
[Pet types and ModelEngine](models.md#animation-clips).

## Voices

Without `voice` or `sounds`, a pet keeps its body's native audio. `voice: <preset>`
replaces it with a profile and silences the body. The presets `wolf`, `cat`,
`fox`, `frog` and `parrot` include specialised cues (purr, whine, hiss…); any other
vanilla entity ID, such as `voice: rabbit`, builds a voice from that entity's
ambient, hurt and death sounds. `none` starts empty and `voice: false` silences
the pet.

```yaml
voice:
  preset: fox
  pitch: 1.3                     # multiplies every event's pitch (0.1–2)
  ambient-interval-seconds: 25   # randomised ±20%; 0 disables idle sounds
  greeting: {sounds: [ENTITY_FOX_AMBIENT, "tfmc:pet.hello"], volume: 0.6, pitch: 1.1}
  toy: false
```

Events are `ambient`, `happy`, `happy-quiet`, `sad`, `hurt`, `death`, `greeting`,
`toy`, `social`, `protest` and `eat`. Each accepts a sound name, a list,
`false`/`[]`, or `{sounds, volume, pitch, min-interval-seconds}`. Use Bukkit sound
names or namespaced resource-pack keys; `minecraft:` keys must exist on the server,
and missing generated sounds fall back to the ambient sound or are disabled with
a warning. Omitted events inherit the preset. A pitch-only mapping keeps the
species or body voice. The older `sounds` key accepts the same settings.

## Interaction item IDs

Item IDs use the same notation and optional provider APIs as Archaeo:

| Provider | Example |
| --- | --- |
| Vanilla | `STICK` or `minecraft:stick` |
| MMOItems | `mmoitems:PETS:MEAT_TREAT` (type `PETS`, item ID `MEAT_TREAT`) |
| ItemsAdder | `itemsadder:tfmc:pet_ball` (namespace `tfmc`, item ID `pet_ball`) |

Aliases `mi:TYPE:id`, `ia:namespace:id` and bare `namespace:id` also work.
Quote custom IDs in YAML; one-key maps caused by unquoted colons are recovered
as in Archaeo. Provider IDs are matched case-insensitively and independently of
base material/model data. Vanilla excludes provider-identified items but accepts
renamed/enchanted vanilla items. MMOItems identity uses its `getTypeName`/`getID`
API; custom APIs are optional and loaded by reflection. CompanionPets has no
runtime dependency on Archaeo, Cooking or MCPets. The former dotted selectors
(`v.stick`, `m.pets.meat_treat`, `ia.tfmc:pet_ball`) remain compatible.

Custom IDs reference provider-owned items. Unknown or unavailable items never
substitute unrelated vanilla items. Menus show the provider model/name and all
accepted treats, medicines and brushes. Lookups retry as provider registries
become available. Existing saved vanilla toys and favourite-toy IDs still load.

## Global interaction items

The five global categories are under `items`. All species share these defaults:

```yaml
items:
  treats: [mmoitems:PETS:FISH_SNACK, mmoitems:PETS:BISCUIT_TREAT]
  foods:
    - {item: mmoitems:PETS:MEAT_TREAT, hunger: 35}
    - {item: mmoitems:PETS:FISH_TREAT, hunger: 35}
  medicines: [mmoitems:PETS:PET_MEDICINE]
  brushes: [mmoitems:PETS:PET_BRUSH]
  toys: [STICK, mmoitems:PETS:PET_BALL, mmoitems:PETS:PET_CHEW_BONE, mmoitems:PETS:PET_TUG_ROPE, mmoitems:PETS:PET_MOUSE_PLUSH, mmoitems:PETS:PET_TEDDY_PLUSH]
```

The default custom IDs must be registered in MMOItems. Servers using only
vanilla items can replace the global lists with vanilla IDs.

All accepted treats train and reward every species. Players may switch accepted
treats without ending a training session. Treat rewards consume one treat and use
the training settings. Hungry pets may eat a treat for 30 hunger points and the
`care.favorite-food-mood` bonus. Regular food (Meat Meal `MEAT_TREAT` and Fish
Meal `FISH_TREAT`; the IDs are kept for existing items) uses each entry's
`hunger` value. Pet Medicine consumes one item to treat sickness and applies
`care.medicine-health-bump`. The Pet Brush cleans without being consumed. Toys
retain their full metadata through throwing, fetching, returns and saved carried
items.

## Per-pet overrides

For a replacement in one species or pet, use the same fields under `species.<id>.items` or `pets.<id>.items`:

```yaml
pets:
  cat:
    species: cat
    egg: CAT_SPAWN_EGG
    items:
      treats: ["mmoitems:PETS:FISH_SNACK"]
      foods: [{item: SALMON, hunger: 55}]
      medicines: []
      # brushes and toys are omitted, so they remain global.
```

A present category **replaces the entire corresponding global list**. It never
appends to that list. An omitted category inherits; `[]` disables that category.
`items: {}` inherits everything. Malformed or invalid override entries are logged
and skipped without falling back to the global category. The shipped pet types
have no active overrides.

### Legacy item settings

Legacy per-pet `care.foods`, `care.favorite`, `care.medicine` and root `toys`
remain category replacements unless the corresponding new `items` list is
present. The former global `items.brush` is accepted if `items.brushes` is absent.
Food accepts the old `MATERIAL: hunger` map as well as `item`/`hunger` lists.
Finite non-negative hunger values are required.

## Dig gifts

`moments.dig-loot` lists the items a pet can dig up for its owner. It accepts the
same item IDs in `item`/`weight` lists with positive integer weights. The old
material map also works, and `dig-loot: []` disables gifts.

## Eggs

Eggs remain unique per pet type. Use `mmoitems:PETS:PET_BEAGLE_EGG` or an
ItemsAdder ID alone for custom eggs. The legacy `egg-custom-model-data` only
works with vanilla material selectors; those material/model combinations also
accept provider-created eggs for compatibility. Explicit provider IDs take
priority. Confirmation rechecks the held item before consuming it.

## Pet Houses

Pet House placement stays global: `items.kennel` selects the consumed held item;
`items.kennel-block` selects the actual vanilla block (`BARREL` for custom
tokens). Without `items.kennel-furniture`, this places a regular Pet House.

For ItemsAdder furniture, configure the held item and the matching placed
furniture ID. Only simple furniture is supported: complex furniture events do
not expose the player needed to record ownership and enforce owner-only access.

```yaml
items:
  kennel: "itemsadder:tfmc:pet_house"
  kennel-furniture: "tfmc:pet_house"
  kennel-block: BARREL
```

ItemsAdder handles normal placement, protection checks, consumption and drops.
CompanionPets records the owner after successful placement. Right-clicking opens
the owner's Pet House menu; other players cannot open it. Breaking the furniture
removes its ownership record without deleting pets. Registered barrel Pet Houses
remain usable, and vanilla-only configurations keep sneak and right-click
placement. Plant and block settings continue to use vanilla materials.

## Learnable tricks per pet type

`tricks` in a species or pet selects which tricks a type can learn and perform,
for both vanilla and ModelEngine appearances:

| Form | Result |
| --- | --- |
| Omitted | Inherit the species, or the eight built-in tricks |
| `{add: [id], remove: [id]}` | Edit the inherited set; removal wins if an ID is in both |
| `[id, id]` | Replace the inherited set |
| `[]` | No tricks beyond the default tricks |

Built-in IDs: `sit`, `follow`, `come`, `stay`, `speak`, `jump`, `lay`, `paw`.
Custom tricks are opt-in: defining one under `custom-tricks` does not grant it to
every pet. Name it in a species or pet list, or use `tricks: {add: [salute]}`.
Names are case-insensitive and duplicates are ignored. Species adjustments apply
first, then the pet's. Configured default tricks are always enabled. Unknown IDs
are skipped with a warning; a malformed value disables additional tricks, but the
pet still loads.

The selection filters learning and learned menus, word suggestions, binding,
training rewards, and spoken or command-driven trick execution. Disabled tricks
retain their saved words and progress so they can be enabled later. Ordinary
care, automatic rest, navigation, and responding to the pet's name are unchanged.
An animation's presence does not grant a trick, and a permitted trick does not
require a custom animation.

### Default tricks

Initial learning is configured globally and can be replaced per type:

```yaml
training:
  default-tricks: [follow]
pets:
  wolf:
    species: dog
    egg: WOLF_SPAWN_EGG
    # Omit default-tricks to inherit the species or global list.
    # default-tricks: [follow, sit, lay]
    # default-tricks: [] # No initial learning for this type.
```

These tricks start at 100% and get their lowercase ID as a command word, shown
in the Tricks menu. This also grants missing defaults to existing pets during
startup or reload. Removing a default does not delete learned progress or words.
Existing bindings are preserved when a default word is already used for another
trick. Unknown or removed IDs and malformed default lists reject the
configuration. Custom trick IDs are supported.

Come is learned independently of Follow; add it to `default-tricks` if it should
be known from birth. Saved Come learning remains separate from Follow. The
literal word `come` that an earlier dev build assigned to Follow is restored to
Come, preserving its progress; other Follow words retain their bindings.

### Legacy trick IDs

`lay` replaces the former Rest trick (`sleep` ID). The pet lies down awake, uses
the `lie` pose and does not show the Sleeping label; only automatic sleep uses
the sleep state and label.
Legacy `sleep` entries in configuration and saved words or progress are accepted
as `lay`; subsequent saves use `LAY`. Existing spoken words remain bound, and the
highest progress is retained if both old and new IDs are present. Spin has been
removed from tricks, training, completion and saved legacy words and progress.

### Custom tricks

Define custom gestures at the top level:

```yaml
custom-tricks:
  salute:
    display-name: "Saludar"
    animation: salute
    fallback-text: "{pet} te saluda."
    duration: 2
  roll:
    display-name: "Rodar"
    animation: roll
  croak:
    display-name: Croak
    animation: croak
    sound: ENTITY_FROG_AMBIENT
    at: [0.54, 2.33, 2.67]
```

Custom tricks share the normal word binding, training, progress and rewards.
The animation is an exact model clip name. If it is unavailable, `fallback-text`
appears above the pet (`{pet}` and `{owner}` are replaced; plain text only).
Without either an available animation or fallback text, the trick is omitted
for that pet. Invalid definitions are skipped individually. Base trick IDs
cannot be redefined. Menus paginate when there are more than nine choices.
`duration` defaults to two seconds and controls text and zero-length animation
poses; moving clips play once at their own length. Definitions may be removed
and restored without losing stored words or progress.

`sound` is optional and uses the same names, lists or `{sounds, volume, pitch}`
mapping as [voice events](#voices). `at` gives the seconds from the start of the
trick at which it plays, as a number or a list (default `0`), so it can follow
the clip. The sound also plays with fallback text, and a new command cancels
cues still pending from the previous trick.

## Belly rub moment

Configure the optional belly rub moment under `moments.belly-up`:

```yaml
moments:
  belly-up:
    enabled: true
    chance: 25
    idle-seconds: 5
    cooldown-seconds: 60
    min-mood: 70
```

`min-mood` sets the mood the pet needs. Each eligible attempt uses the cooldown,
including unsuccessful rolls. Setting `enabled: false` disables the moment. The
player-facing behaviour is described in the [gameplay guide](gameplay.md#belly-rub-moment),
and the model clips it needs in [Pet types and ModelEngine](models.md#animation-clips).

## Care and roaming settings

- `care.sleep-minutes-to-full` sets how many minutes sitting, lying and
  sleeping pets take to recover full energy (default 8, or 12.5 points per minute).
- `care.sleeping-hunger-multiplier` reduces hunger decay while a pet sleeps.
- `orders.hearing-radius` (default 12 blocks) limits which pets hear named orders.
- `roaming.name-attention-seconds` (default 10 seconds) sets how long a called
  pet waits after arriving.
- `care.health-regen-per-minute` (default 20) sets natural health recovery; see
  the [gameplay guide](gameplay.md#care).

### Relaxed care preset

For a server where pets need less frequent care, the optional
[relaxed care preset](https://github.com/TF-Minecraft/CompanionPets/blob/main/config-presets/relaxed-care.yml)
records the values used on TF Dev. It is a partial preset: copy its values into
the matching sections of your existing config and keep your pet types, models
and item selectors. Set each existing food entry's `hunger` to 45, as the preset
indicates. With these settings, a fully cared-for pet walking near its owner for
four hours keeps about 62 hunger, 75 mood, 62 energy, 80 cleanliness and full
health. Its belly-up chance is 25%.
