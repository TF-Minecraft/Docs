# CompanionPets pet types and ModelEngine

[CompanionPets](../README.md) · [All projects](../../../README.md)

## Pet types

[`config.yml`](https://github.com/TF-Minecraft/CompanionPets/blob/main/src/main/resources/config.yml)
defines pet types under `pets`. The key is the saved type ID and the name shown
in menus: `wolf` and `beagle` are distinct pets. Species, bodies, behavior
profiles and voices are described in the
[configuration guide](configuration.md#species-and-pets). The body (`entity`,
WOLF or CAT) supplies navigation and native AI; the appearance only changes what
players see. Vanilla pets need no ModelEngine installation. `mythic-mob` can
supply the body with a declared WOLF or CAT `entity`; CompanionPets should own
the appearance and animations of a body using this integration.

```yaml
pets:
  wolf:
    species: dog
    egg: WOLF_SPAWN_EGG
  beagle:
    species: dog
    model: beagle                  # ModelEngine at scale 1
    egg: "mmoitems:PETS:PET_BEAGLE_EGG"
  husky:
    species: dog
    appearance: {type: modelengine, model: husky, scale: 0.9}
    animations:
      paw: {name: paw, speed: 1.0, blend: 0.15}
    egg: "mmoitems:PETS:PET_HUSKY_EGG"
```

`model: <id>` selects ModelEngine at scale 1. Use `appearance` for other settings;
explicit appearance fields override the shortcut, and `appearance.type: vanilla`
disables a model. Top-level `animations` is a shortcut for
`appearance.animations`; explicit appearance mappings win for the same action.
Each type needs a unique egg; provider item IDs and the legacy
`egg-custom-model-data` are described in the
[configuration guide](configuration.md#eggs). The plugin checks the egg again
when the player confirms the name.

Changing a pet's underlying entity type takes effect when that pet is summoned
again.

## Animation clips

All model clips are optional. Available clips are discovered by their names,
which default to their configuration keys, so a model using these names only
needs `type: modelengine` and `model: beagle`. Each mapping accepts a clip name
or `{name: ..., speed: 1.0, blend: 0.15}`; `blend` is the transition time in
seconds.

| Clips | Trigger and playback |
| --- | --- |
| `idle`, `walk` | Actual displacement, including following, roaming, fetch and social play. Loop while applicable. |
| `sit` | Sitting. Stay remains standing unless the body is actually sitting. |
| `death` | Natural entity death, rendered by ModelEngine's default death handler. |

Optional clips are discovered by name when present in the model, or explicitly
mapped. Set a mapping to `""` to disable an optional clip.

| Extra clips | Trigger and playback |
| --- | --- |
| `lie`, `sleep` | Exhaustion/weakness and sleeping, including sleep caused by care needs. Loop until the pet recovers or wakes. Missing `sleep` falls back to `lie`, then `sit`. |
| `fly`, `hover` | Airborne flying bodies, moving/stationary. Fall back to `walk`/`idle`. |
| `crouch` | A cat moving while sneaking, and the `cat` profile's stalk before pouncing on a thrown toy. Falls back to `walk` when moving and `idle` while stalking. |
| `paw` | Giving a paw. Plays once while navigation pauses. |
| `head_tilt` | Brief head-only gesture for an unknown training word or a failed learning attempt, at most once every three seconds. Layers over the current standing/sitting pose. Author only head bones, and use a distinct clip name. Vanilla wolves use their interested state. |
| `shake` | A WOLF body's native water shake. Plays once at the clip's own speed; its length sets how long the shake and its droplets last. |
| `pet` | Normal petting reaction. Does not interrupt a belly moment or another gesture. |
| `jump`, `swim` | Optional air/water motions. ModelEngine plays `jump` for any jump, including the `cat` profile's pounce; `swim` loops. Missing clips use `idle` in the air and `walk` in water. |
| `attack`, `hurt`, `eat`, `speak`, `spawn` | Automatically used when present for their corresponding behaviour. Missing clips do not prevent the behaviour. |
| `lie_back`, `belly_up`, `get_up` | The optional [belly rub moment](gameplay.md#belly-rub-moment). |

No clip is required. Missing `idle`/`walk` logs a warning about a potentially
static model, but does not reject it. Without their clips, eating and speaking
use effects and sounds. No illness clip is needed.

The original `lay` is automatically recognised for `lie` if no mapping overrides
or disables it. If neither `lie` nor `lay` exists, an available, enabled `sleep`
clip supplies the lying posture, including its configured speed and blend.
Zero-length `head_tilt` is held briefly rather than vanishing. Head tracking
belongs to the model's head bone behaviour, not a look animation.

Without `jump`/`swim`, dogs and cats use `idle` in the air and `walk` in water;
jumping and falling remain physical movements.
`pet1`, `pet2`, and `despawn` have no automatic hooks. Map `pet: pet1` to use
an older petting clip. [Custom tricks](configuration.md#custom-tricks) may also
refer to arbitrary model clips.

For the belly rub moment, a zero-length `belly_up` is held by the plugin; an
animated one loops. Transitions retain their final frame until the next stage
to avoid snapping. All three clips must exist and be enabled.

Gestures finish into the pet's current pose. A new command interrupts the
previous gesture; sleep, lying down, water and falling can also interrupt it.
Sickness continues to use care particles and sounds. All tricks still work
with vanilla pets and their existing visual approximations.

Minecraft decides when a wet wolf shakes: it gets wet in water or rain, does not
shake while it is still raining on it, starts only once it stands on the ground,
and the native shake lasts two seconds. When it starts, modelled wolves play
`shake` once at the clip's own speed, including while walking, and emit splash
particles for as long as the clip plays. To make the shake longer or shorter,
change the clip's length in Blockbench. Water, lying down or sleeping stop both. If another
gesture is playing when a shake begins, that shake is not animated rather than
starting late. Fetching, greetings, toy focus and pet meetings postpone the shake;
the pet then ends dry instead of shaking again afterwards. Vanilla fallback wolves
keep Minecraft's own shake and droplets.

The plugin disables tail gestures for a model without a `tail`, `tail_…` or
`tail1…` bone, and belly rubs if `lie_back`, `belly_up` or `get_up` is missing or
disabled. Models are checked again until ModelEngine has registered them, so the
initial registration needs no reload; reload CompanionPets after regenerating a
blueprint that was already loaded.

## TFMC models

The `beagle`, `chihuahua`, `corgi`, `golden`, `husky`, `catblack`, `catfunny`,
`catorange`, `mainecoon` and `fox` models use `idle`, `walk`, `death`, `sit`,
`sleep`, `paw`, `head_tilt`, `lie_back`, `belly_up` and `get_up`. They need no
`lay` or `swim` clip. Dogs and the fox also have `shake`; the fox's `pet2` can be
enabled with `pet: pet2`. `paw` plays once even when the authored clip is marked
as a loop (the cats' `paw` clips are). The cats and the fox use the `cat` profile
but have no `crouch` or `jump` clip yet: their stalk waits in `idle` and the
pounce moves the body unanimated until those clips are added.

The frog retains `idle`, `walk`, `jump`, `swim`, `lay`, `croak` and `tongue`.
It uses its `jump` and `swim` clips without overrides to keep its
species-specific motions. Map `speak: croak` and optionally `eat: tongue` or
`attack: tongue`; its sleeping pose falls back to `lay`. Its zero-length
`animation.common.look_at_target` is not an action hook. These are
species-specific uses of existing clips, not additional animation requirements
for every pet.

## Authoring models

An empty Blockbench clip is an authoring placeholder, not a finished action.
Disable unfinished optional clips with `""` until they are animated.

Install ModelEngine 4 and serve its generated resource pack to players. Author
the model around the base entity's feet, with a correctly sized ModelEngine
hitbox and head bone behaviour for looking at players. Keep movement clips
in place: the body supplies translation and jumping, so animation root motion
would move the model away from its hitbox. Include all bones needed for each
full-body pose. The plugin hides the vanilla body only after a model is attached,
scales the model and hitbox together, loops poses and forces gestures to play
once. It does not generate model assets or a resource pack.

## Model attachment

An unavailable model leaves the pet visible as its vanilla body and logs the
reason. Failed attachments retry every 30 seconds; vanilla servers remain usable
without ModelEngine. Models are reapplied on chunk loads and on configuration
reload, removed when pets are stored or released, and detached when
CompanionPets stops. The old `trick-animations` mapping must move to
`animations` or `appearance.animations`.

The integration uses the
[ModelEngine 4 animation API](https://ticxo.github.io/Model-Engine-4.0-JavaDocs/com/ticxo/modelengine/api/animation/handler/AnimationHandler.html)
and was checked against the ModelEngine 4.1.1 API.
