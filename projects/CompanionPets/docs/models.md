# CompanionPets pet types and ModelEngine

[CompanionPets](../README.md) · [All projects](../../../README.md)

## Pet types

[`config.yml`](https://github.com/TF-Minecraft/CompanionPets/blob/main/src/main/resources/config.yml)
defines pet types under `pets`. The key is the saved type ID and the name shown
in menus: `wolf` and `beagle` are distinct pets. `entity` selects the Minecraft
body and AI, so both can use `WOLF`. `appearance.type` selects `vanilla` (the
default) or `modelengine`. Vanilla pets need no ModelEngine installation and
keep their existing behaviour. `mythic-mob` can supply the body instead of
`entity`; CompanionPets should own the appearance and animations of a body using
this integration.

```yaml
pets:
  wolf:
    entity: WOLF
    appearance:
      type: vanilla
    egg: WOLF_SPAWN_EGG
    sex: random
    # Inherits the global interaction lists.
  beagle:
    entity: WOLF
    egg: WOLF_SPAWN_EGG
    egg-custom-model-data: 12001
    appearance:
      type: modelengine
      model: beagle
      scale: 1.0
      animations:
        idle: idle
        walk: walk
        sit: sit
        death: death
        lie: sleep
        sleep: sleep
        head_tilt: head_tilt
        shake: shake
        paw: {name: paw, speed: 1.0, blend: 0.15}
    sex: random
    # Inherits the global interaction lists.
```

The plain vanilla spawn egg selects `wolf`; an egg of the same material with
CustomModelData `12001` selects `beagle`. The custom egg must be supplied by
your item provider or a command. For this legacy example, each type needs a
unique combination of egg material and optional custom model data. The plugin
checks the egg again when the player confirms the name. Provider item IDs for
eggs are described in the [configuration guide](configuration.md#eggs).

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
| `run` | Falls back to `walk` at 1.5 times its configured speed. `run-speed` defaults to 0.22 blocks/tick, with hysteresis. |
| `crouch` | A cat moving while sneaking; falls back to `walk`. |
| `paw` | Giving a paw. Plays once while navigation pauses. |
| `head_tilt` | Brief head-only gesture for an unknown training word or a failed learning attempt, at most once every three seconds. Layers over the current standing/sitting pose. Author only head bones, and use a distinct clip name. Vanilla wolves use their interested state. |
| `shake` | Begins when the native wolf shake clock starts, alongside its vanilla sound. Play once. |
| `pet` | Normal petting reaction. Does not interrupt a belly moment or another gesture. |
| `jump`, `fall`, `swim` | Optional air/water motions. Jump plays once and holds until landing or the fall pose; swim loops. Missing clips use normal movement/idle fallbacks. |
| `beg`, `attack`, `hurt`, `eat`, `speak`, `spawn` | Automatically used when present for their corresponding behaviour. Missing clips do not prevent the behaviour. |
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
jumping and falling remain physical movements. `beg` remains a learned command
using its vanilla sitting/attention behaviour when no `beg` clip is present.
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

Modelled wolves emit water splash particles throughout their native shake clock,
alongside the `shake` animation and vanilla sound. Vanilla fallback wolves
retain their original particles.

## TFMC models

The `beagle`, `chihuahua`, `corgi`, `golden`, `catblack`, `catfunny`,
`catorange` and `fox` models use `idle`, `walk`, `death`, `sit`, `sleep`, `paw`,
`head_tilt`, `lie_back`, `belly_up` and `get_up`. They need no `lay`, `jump` or
`swim` clip. Dogs and the fox also have `shake`; the fox's `pet2` can be enabled
with `pet: pet2`. `paw` plays once even when the authored clip is marked as a loop.

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
CompanionPets stops. The old top-level `model` key is accepted with a migration
warning; old `animations` and `trick-animations` mappings must move to
`appearance.animations`.

The integration uses the
[ModelEngine 4 animation API](https://ticxo.github.io/Model-Engine-4.0-JavaDocs/com/ticxo/modelengine/api/animation/handler/AnimationHandler.html)
and was checked against the ModelEngine 4.1.1 API.
