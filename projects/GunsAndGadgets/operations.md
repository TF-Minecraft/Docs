# Commands and ammunition handling

[GunsAndGadgets documentation](README.md) · [All projects](../../README.md)

## Staff gun commands

`/gg give <player> <rifle|pistol|shotgun|launcher> <part> [part...]`

Gives one completed, unloaded gun to an online player. Use part IDs from
`parts.yml` and supply exactly one enabled, compatible part for every category in
`required-parts` in `config.yml`. The normal assembly builder applies stats,
skins, and part provenance. Conflicting class requirements and invalid designs
are rejected. The recipient needs an empty inventory slot.

No crafting materials are charged. The item explicitly records an empty set of
consumed crafting inputs, so compatible recycling cannot return unpaid materials.
Load ammunition normally.

`give-permission` in `config.yml` defaults to `gunsandgadgets.give` (operators).
Set it to your staff permission; a blank value disables giving. This permission
is independent of `gunsandgadgets.reload`, which gates `/gg reload` and
`/gg refresh`. Reload configuration with `/gg reload`. Tab completion suggests
recipients, weapon types, and enabled compatible parts for required categories
that are still missing. It stops after a complete assembly.

`/gg refresh` is player-only and force-refreshes the gun in the main hand. See
[revision and craft provenance](docs/REVISION_SYSTEM.md) for automatic refresh
triggers and the data preserved when stats change.

## Ammunition selection

Crouch and right-click with a gun to cycle through compatible ammunition carried
in the inventory. The next reload uses the selected calibre, and the choice is
saved on that gun. Already loaded ammunition stays loaded. Without a selection,
reloads use the first compatible ammunition carried.

The action bar confirms the selection and carried amount, or reports that no
compatible ammunition is available. Selection is blocked while the gun is
reloading.

## Shot handling

The `handling` section of `config.yml` (GunsAndGadgets 2.2.0) tunes spread,
damage over distance and the headshot bonus. Leaving a key out keeps the
behaviour from before the section existed: headshot 1.5, every spread
multiplier 1, no falloff.

| Key | Effect |
| --- | --- |
| `headshot-multiplier` | Damage multiplier for hits in the top quarter of a player's hitbox. |
| `spread-multipliers.sneaking` | Multiplies the ground value (still or moving) while crouched. |
| `spread-multipliers.moving` | Any movement key held (`Player#getCurrentInput`). |
| `spread-multipliers.sprinting` | `isSprinting()`; beats `moving`. |
| `spread-multipliers.airborne` | Not on the ground; water, climbing and creative flight don't count. Beats sprinting. |
| `spread-multipliers.mounted` | Riding an animal, or a seat whose vehicle is moving. |
| `max-spread-degrees` | Upper limit for the final launch spread. No limit when left out. |
| `falloff.start-distance` | Bullets do full damage up to this many blocks from the muzzle. |
| `falloff.min-multiplier` | Damage multiplier at the shot's maximum range, reached linearly. `1` turns falloff off. |

Non-finite values (`.nan`, `.inf`) fall back to each key's default.

The stance is read once, when the shot fires, and applies to every pellet of
that shot. It widens only the launch cone; a rocket's wobble in flight keeps the
gun's own spread. Seats count as mounted only while moving:
- VehicleFramework seats riders through ModelEngine, so they have no Bukkit
  vehicle. GunsAndGadgets finds them with `getByPassenger` and checks the access
  panel speed of the vehicle at the front of the coupling. Train carriages
  therefore move with their locomotive, and harnessed carts count too.
- Minecarts count by their own horizontal velocity.
- A player-driven boat moves on its driver's client and shows no velocity on the
  server. It counts as moving while its driver holds forward or back. Other seats
  don't read their rider's keys.
- Animals always count as mounted.
- GSit chairs and parked vehicles count as standing still.

A shooter's own VehicleFramework vehicle never stops their bullets: the muzzle
starts inside the vehicle, next to its base. Other vehicles and people still do.

Players standing on a vehicle's deck count as on foot. Swimming fast counts as
sprinting. Falloff applies to bullet hits on living entities; rocket explosions
and vehicle hits are unchanged.

Two more `handling` keys:

| Key | Effect |
| --- | --- |
| `smooth-accuracy` | `true`: above accuracy 5, each point tightens spread by 5%. Off or left out: the old line, which reaches 1.2° at 20 and 0.07° at 30. |
| `pellet-cone.tighten-per-accuracy` / `pellet-cone.min-factor` | A shotgun barrel's pellet cone (its `spread` stat) shrinks by this share per point of accuracy, down to `min-factor` of its size. Defaults 0.03 and 0.4. |

## Forged parts

A part in `parts.yml` with `tendencies` is forged. It becomes one part per
material in `metals.yml`, with the id `<part>@<material>` (for example
`heavy_barrel@steel`), which is what `/gg give` and crafted guns use. In the
gunsmith, players pick the part, then the material.

`metals.yml` lists the materials. Each one has:
- `kind`: `metal` or `wood`. A part forges from one kind: `material: wood` for
  stocks; metal by default.
- `tier`: sets the part tier, and the shot tier a barrel loads.
- `cost` and `permission`: the ingot or wood paid per part, and who may forge it.
- `better` and `worse`: multiply a part's upsides and downsides. A number sets
  every stat; a section sets `default` plus per-stat factors.
- `description`: notes on the material for config readers; players see the
  part lore instead.

A new material (an alloy) only needs a new entry. Every forged part of its kind
gains it.

Part keys:

| Key | Effect |
| --- | --- |
| `tendencies` | `stat value` lines written for the reference material (steel; maplewood for stocks). The material scales them. Lore shows them as one to three arrows, not numbers. |
| `fixed` | Stats no material changes: shots held, a shotgun's pellet cone (`spread`), a revolver's damage percentage. |
| `by-metal` | Extra stats per material, e.g. the multi-tube chamber's rockets. |
| `metals` | Limits the part to these materials. |
| `cost-amount`, `cost` | Ingots of the material (default 2), plus any other cost entries. |
| `ammo-family` | `shot`, `spreadshot` or `rocket`: the barrel loads that family up to its material's tier. Ammunition entries carry `family`, `tier` and `powered`. |
| `ammo-filter` | `powered` or `plain`: the gun loads only that shot. |
| `skin-base` | Matches gun designs as if the action were this part, e.g. `flintlock`. |
| `metal-lore` | One lore line per material (`iron: "..."`), shown on that variant. The part list, before a material is picked, shows `lore`. |

New stats: `damage_percent` (scales gun and shot damage), `falloff` (blocks
added to `falloff.start-distance`), `pierce` (added to the shot's pierce), and
`moving`, `mounted` and `sneaking`. The last three are percentages: positive
means steadier. `moving 40` lets 60% of the walking, sprinting and jumping
penalty through, and `sneaking 50` deepens the crouch bonus by half. The
combined factor stays between 0.5 and 2. Editing `metals.yml` or a part changes
its revision, so existing guns refresh to the new numbers.

### Retiring old parts

Forged parts reuse old part ids (`matchlock`, `single_shot`, …), so move the old
`parts.yml` entries to `retired-parts.yml` when switching. Those parts load
disabled: guns built from them still resolve, but nobody can craft them. An id
that `parts.yml` also defines is skipped.

With `retire-disabled-part-guns: true` in `config.yml`, a gun stamped with a
disabled part refuses to fire or reload. Nothing is written to the gun, so
setting it back to `false` restores the gun. Its holder sees one warning per gun
per restart.

### Refunds

`refunds` in `config.yml` removes old guns so none stay on the server. A gun is
old when it carries a retired (disabled) or removed part, or when it is from
before guns recorded their parts (GunsAndGadgets 2.0.0; on Main, guns crafted
15–23 September 2026).

What the player gets back:
- what the crafting took, recorded on guns crafted since 2.0.6;
- older stamped guns: their parts' `cost` from `retired-parts.yml`;
- nothing for guns crafted for free (staff bypass, `/gg give`), unstamped guns,
  and guns with a removed part and nothing recorded. They are just removed.

A full inventory drops the rest at the player's feet.

- Right-clicking the gun station with an old gun takes it apart.
- `automatic: true` also does it wherever guns are refreshed: on join
  (inventory and ender chest), selecting it in the hotbar, clicking it in an
  inventory, and opening storage that holds it (the opener gets the materials).
  These checks read each item's data in place and copy only guns.
- Each refund is logged: `[Refund] <player> gun_id=<id> returned {...}`.

Both are off by default. Turn them on with the switch to forged parts.

### Forged gun looks

A gun built only from forged parts is drawn from the parts it is made of. It
needs ServerAssets' `tfmc_guns` ItemsAdder pack folder, generated by
`tools/forged_guns/build.js`.

- `skins.yml` entries with `forged-model` (`forged_rifle`, `forged_pistol`,
  `forged_shotgun`, `forged_launcher`) win over every other skin for such a gun.
  The item model is `<forged-model>_carry`, `_reload` or `_aim`, on the
  `carry`/`reload`/`aim` material: a crossbow keeps the aiming hold. Remove those
  entries to show forged guns with the old fixed designs.
- The gun's `custom_model_data` strings tell the pack which part goes in each
  slot: barrel, its material, loader, material, chamber, material, action,
  material, stock (`none` without one), wood (the stock's, or `barkwood`).
- Pistols take a grip in the stock slot (`standard_grip`, `birdshead_grip`,
  `pommel_grip`, `wrapped_grip`), so `required-parts.pistol` includes `stock`.
  Launchers never have one.
- `part-icons` in `config.yml` (default `tfmc_guns:part/`) shows each forged
  part's pack icon in the gunsmithing menus, plus `_<material>` once the
  material is chosen. Blank shows each part's own `item`.

Sound and effect keys:

| Where | Key | Effect |
| --- | --- | --- |
| Part or material `sounds` | `pitch=` / `volume=` after the keys | Scale that sound group, e.g. `- shoot minecraft:guns.musket_5 pitch=0.95`. |
| Part | `sound-pitch`, `sound-volume` | Multiply the gun's whole report, e.g. the proof chamber's heavier charge. |
| Part | `ignition` | Effect at the lock when firing: `flint`, `ember`, `wheel`, `steam`, `arc` or `fuse`. |
| Part | `smoke`, `smoke-cone`, `backblast` | Muzzle smoke amount (1 = the old cloud) and fan width (default 0.2); `backblast: true` also blows smoke out of the back. |
| Material | `sound-pitch`, `sound-volume`, `sounds` | The barrel's material pitches the report and can add layers, e.g. mythril's ring. |
| Material | `flash`, `trail` | Hex colours of the muzzle flash and the shot's trail for a barrel of that material. |

Steamlocks keep `smokeless` and `no_light`, so they show only their steam.
Sound changes count as part changes, so existing guns refresh to them.

### Draw time and aiming

`handling.draw` in `config.yml` gives guns a draw time. A gun taken into the
hand can't fire or start a reload until it is drawn. It counts as taken into
the hand after:
- a hotbar change;
- a swap into the main hand;
- moving it into the hand slot;
- a respawn or join.

The hotbar shows the vanilla cooldown sweep for the time left.

| Key | Effect |
| --- | --- |
| `draw.base-seconds.<type>` | Seconds for `pistol`, `shotgun`, `rifle`, `launcher`. Leave the section out for no draw time. |
| `draw.stance.<stance>` | How much longer drawing takes each tick spent `moving`, `sprinting`, `airborne` (jumping or falling) or `mounted` (a moving seat). `sneaking` multiplies the on-foot value, so below 1 is quicker. |

The parts' `draw` stat (Draw Speed) scales the base time: `+25` is 25% quicker
and `-30` is 30% slower, held between half and double.

`aiming` turns on crouch to aim. Crouching with a loaded, drawn gun raises it:
- the model becomes `<forged-model>_ads`;
- walking slows by `slow` (0 to 0.9), which also narrows the field of view.
  Players with FOV effects off get only the slowdown.

A gun with a `scoped` part (the arclock) becomes a spyglass while aimed: hold
right-click to look through it, then release to fire. The release fires only
after `aiming.scope-settle-seconds` (default 0.6); an earlier release lowers the
scope without a shot. A click sound and "Steady" on the action bar mark the
moment. Releasing the crouch, changing item or running empty lowers the gun.

`handling.spread-multipliers.hip` (1.75 in the bundled config) widens the spread
of shots fired without aiming, only while `aiming` is on. Aimed shots still take
the `sneaking` multiplier.

The swap-hands key with a gun in hand picks the next shot; crouch + right-click
no longer does. Messages name the player's own key binding.

### Names and lore

- `metals.yml` `color` (hex) is the material's colour: its ingot or refined
  wood. A forged part's name is written in it ("Steel Long Rifled Barrel").
- An assembled gun's name takes the colour of the metal of its final (majority)
  tier. Bundled `name-impact` entries build [chamber] [action] [barrel], e.g.
  "Double Flintlock Rifle", "Revolving Wheellock Pistol", "Salvo Rocket
  Launcher".
- Each part and material has its own line of lore (`metal-lore`). Its arrows
  show the tendencies in that material, so the lore adds no line on what the
  material does.
- Every stat on an assembled gun has a short note on what it measures.
- Parts whose shot rules leave the gun nothing to load show a barrier: "These
  parts don't make a gun".
- `type-icons` in `config.yml` (default `tfmc_guns:`) draws the gun type buttons
  as a steel gun of that type (`<prefix><type>_carry`). Blank shows paper.

## Character sessions and reload cleanup

The build pins TLibs 2.3.0. With an older TLibs that lacks the character API,
GunsAndGadgets logs an update message and disables itself at startup.
RPCharacters is neither a build dependency nor a `softdepend`: GunsAndGadgets
listens for the shared `CharacterSessionEndEvent`, which RPCharacters 2.16.0
fires when installed. Without a character provider guns work normally; with one,
gun use waits until the character has a ready session.

A reload reserves the exact ammunition stacks it consumes and captures the current
session. Its timer checks that session before progressing; a stale session or a
provider appearing during account fallback cancels it. Switching character,
permanent death, quit and provider shutdown cancel the reload while the outgoing
inventory is still loaded, before it is saved or replaced. Cancellation restores
the reserved items, drops only overflow and clears the reload marker. Duplicate
end/quit notifications and late reload timers cannot refund twice or cancel a
newer reload. GunsAndGadgets also refunds active reloads on its own disable,
covering either plugin shutdown order. Its quit listener remains available when
there is no identity provider.

The deferred held-slot validation captures the current session. It stops if that
session ends, even when the player switches away and back to the same character.
It also stops on disconnect, pending character readiness, or a provider appearing
between scheduling and completion.

To check on a server, start a reload and end the session by switching, permanent
death, quitting and shutdown. Each time the ammunition must return to the outgoing
character's inventory and the next character must not finish the old reload.
Repeat without RPCharacters to check quit cleanup. See the
[shared identity API](../TLibs/character-identity.md) and
[RPCharacters provider](../RPCharacters/docs/character-identity.md).
