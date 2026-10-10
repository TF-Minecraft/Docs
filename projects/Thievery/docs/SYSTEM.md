# Thievery - Display locks

Steal from lockable **displays**: InteractibleFurniture types, armor stands, and item frames. Chests and doors stay as they are.

See [TEST_MATRIX.md](TEST_MATRIX.md) for the manual checklist.

## Responsibilities

| Target | Lock model | Robbery | Fail |
|--------|------------|---------|------|
| Doors | Key + strength (`DoorData`) | Title **bar** | 60s on that door |
| Chests / barrels / etc. | Owner + `LockState` | Floating **lockpick ring**, then hidden **GUI** probe with seized pins | Ring: 60s on that chest, both halves of a double chest (`fail-cooldown-ms`). Probe: access-map cooldown |
| IF furniture, armor stands, item frames | Owner + `LockState` (chest model) | Same **bar** as doors | Same 60s as doors (`fail-cooldown-ms`) |

## Chest hopper automation

When a **block hopper** moves items (`InventoryMoveItemEvent`), allow pull/deposit only if the hopper and every involved block container (chest, barrel, hopper, etc.) share the same **non-null owner UUID**. Guild/PUBLIC player access does not apply to hoppers — only owner equality. Unowned containers block automation; hopper minecarts are not covered. Droppers and other initiators are unchanged.

Displays do not use the chest GUI. Doors and displays share one engine.

## Chest lock minigame

Right-clicking a chest with a lockpick runs every existing chest check (trait, access, owner online, clues, already picking, held lockpick, access-map cooldown), then `LockMinigameManager` opens the floating lockpick ring (`RingDialGame`) instead of the probe menu. It is a `LockMinigame`, like the pickpocket ring, and shows its state on a boss bar. Staff can run it with `/thievery testpick` while looking at a container and holding a lockpick, even with the minigame off; it skips the trait, clue, ownership and access checks.

Both halves of a double chest are one lock (`ContainerManager.lockBlock`, the left half): they share the fail cooldown, and only one thief at a time can work either half, in the ring or the probe menu. The access cooldown is checked again when the minigame is solved, because a guildmate's pick nearby can start it while the lock is being worked. While a thief works a lock, Thievery's door picking and grave looting ignore their clicks; those listeners handle cancelled clicks, so the ring's cancel alone does not stop them.

### Lockpick ring (display entities)

Modelled on the NoPixel lockpick minigame. `RingView` floats a ring of 24 dots in front of the thief, made of display entities that only the thief can see: the tumbler pins and slip marks above it, the key to press in the middle, and a white needle with a dark edge across the dots as the pointer. The needle is the backdrop of a text display around a space, so its edges stay straight and sharp at any angle, where a font glyph or the lockpick item blurred into pixels. The server sends the needle's position two ticks ahead and lets the client interpolate, so it moves at the player's own frame rate rather than in 20-a-second steps.

- Keys are the movement keys, read from the player input packet (`PlayerInputEvent`), so the thief's hotbar never changes. The middle shows a keybind component, so each player sees their own key for forward, left, back or right (Z/Q/S/D on AZERTY, or their rebinding). Sneak gives up.
- The thief is held still while picking (`LockFreeze`): walk speed 0, which also keeps the field of view unchanged, a transient jump modifier, and flight switched off and restored afterwards. Movement events hold the thief's horizontal position against knockback, water or a nudge, but allow looking around and falling, so a thief who started mid-jump lands rather than hovering until the server kicks them for flying. The ring waits for them to land, or be in water or on a ladder, for up to a second (`RingDialGame.LANDING_TICKS`), so it floats before their eyes where they come to rest; the steady countdown starts once it appears. Hotbar scrolling, dropping, swapping hands, inventory clicks and mounting a horse or boat are cancelled, so the lockpick stays in hand. The original walk speed is stored on the player, so a crash mid-pick is undone on their next join.
- Each pass (`Sweep`) takes `dial.min-lap-seconds` to `dial.max-lap-seconds` (1.44 to 2.08), plus `dial.lap-seconds-per-dexterity` (0.008) per Dexterity level, with a zone of `dial.zone-width` of the ring somewhere after the first third. Each set tumbler narrows the zone by `dial.zone-shrink-per-tumbler` (never below 40%) and, with `dial.alternate-direction`, reverses the sweep like a combination lock.
- Quiet clicks mark each notch the needle passes; they rise in pitch inside the zone.
- A press is judged where the needle was `ping / 50ms` ticks earlier (up to `dial.max-lag-ticks`), which is what the thief saw. A pass only runs out that many ticks after its end, so a laggy press for a zone near the end still arrives in time. A hit pops a pin with a green puff of dust; too soon, too late, the wrong key, two keys at once (fumbled) or a full pass without a press is a slip, with a red flash and a red puff. The puffs go off just past the needle's outer tip, clear of the zone, scale with the ring, and are sent to the thief only.
- The ring floats at `dial.distance` blocks, slightly above the crosshair to clear the action bar, and shrinks as it comes closer so it always looks the same size. Because of that, each point of the ring stays on one sight line from the eye; placement traces a 5x5 grid of sight lines across the ring's outline (needle, pins, hint and labels) and keeps every point at most 60% of the way to the block behind it, but no closer than 0.25 blocks. Checking only the crosshair let the ring sink into a chest's lid when looking down at it, or into a raised chest when looking up.
- Setting `dial.tumblers` (4) solves the lock. `dial.mistakes-to-fail` slips (1) fail it. A solved ring therefore has no slips, so it adds no seized pins unless that setting is raised.
- You cannot start the ring while riding or gliding.

### Failure and interruptions

Failing means `dial.mistakes-to-fail` slips, giving up (sneak), being hurt, or logging out mid-pick. On failure:

- `LockPickManager.applyCooldown` puts the chest's target id `chest:<world>:<x>:<y>:<z>` on `fail-cooldown-ms`. A new attempt is refused until it expires, and `/thievery` cooldown resets clear it.
- `fail-break-chance` rolls whether one lockpick from the main-hand stack snaps. Only the pick the thief started with can snap: during the ring the hotbar, dropping, swapping hands and moving items are blocked, and a different item in hand is never broken.

Being teleported away (another world, or more than a block) ends the pick. A teleport the thief brings on themselves, after running a command or by ender pearl or chorus fruit, counts as a failed attempt; one done to them, by staff or another plugin, does not.

Ending without a penalty: being teleported away by someone else, the chest being broken, `/thievery reload` or a shutdown. Logging out after solving gives no reward. A thief already in a minigame is told "You're already working a lock." and cannot start another; a player in a minigame counts as already picking that chest. Chest access, nearby pings and the multi-day access cooldown are recorded only when the probe menu opens. `lockpicking.chest.minigame.enabled: false` skips the minigame.

## Pickpocket ring

`/pickpocket start` then right-clicking a player runs the pickpocket checks (trait, range, guild access cooldown), then `LockMinigameManager.startPickpocket` floats the pickpocket ring before the pocket opens. It is modelled on level 2 of the NoPixel lockpick: a gauge that drains while the thief mashes a key to fill it. It is the only pickpocket minigame. `PickpocketGame` is a `LockMinigame` with no chest, so it shares the lockpick ring's hold-still rules, landing wait, blocked hands and interruptions above.

- `RingView.openGauge` floats a band of 40 touching dots where the lockpick ring would float, but also short of the mark's body, so a mark standing closer than `dial.distance` cannot hide it. It has a pip above it for each phase, a hint above that, and in the middle the phase name, the percentage and the key to mash. Only the dots that change are sent.
- The key is jump, read from the player input packet; the middle shows each player's own binding. The real game's mash key, E, opens the inventory, which the client never tells the server. Sneak gives up.
- Two phases, cyan then orange. Each press adds 2.05% (give or take 15%) and the ring drains 3.52% a second on a slow wave of about 3%: level 2's base drain with the original's random surges smoothed into the same average. The first phase is half length, so it fills and drains twice as fast. A filled phase pops its pip green and the next starts empty half a second later. At about seven presses a second the ring fills in roughly 15 seconds.
- A 1-second "Steady..." pause comes first. Then the boss bar counts down `pickpocket.minigame.time-limit-seconds` (30, at least 5) across both phases.
- Filling both phases opens the pocket. It checks again that the mark is online, within `pickpocket.max-distance` and not taken by a guildmate meanwhile; the guild access cooldown is recorded only then.

Failing means the time running out, giving up, being hurt, logging out or teleporting yourself away mid-pick. It alerts the mark with `pickpocket.alert-subtitle` and puts that mark on `lockpicking.fail-cooldown-ms` for the thief (target id `pocket:<victim uuid>`); `/thievery` cooldown resets clear it. Nothing breaks. The mark going offline or out of `pickpocket.max-distance` ends the attempt without a penalty. A thief already in a minigame cannot start one. `pickpocket.minigame.enabled: false` opens the pocket straight away. Staff can play the ring with no mark using `/thievery testpick pocket`; it applies the cooldown to `pocket:test` and alerts no one.

## Chest probe: seized pins

The probe menu is a minesweeper-style puzzle instead of a random break roll. `SeizedPins` hides seized pins among the menu's chest slots, using the menu's nine-column grid for adjacency.

- Pins are placed on the first probe. That slot and, when there is room, its eight neighbours stay clear, so the first probe always reveals something.
- Each safe probe shows how many of the eight surrounding slots hide a seized pin. An empty slot becomes a glass pane whose colour and stack size give the count (white 0, light blue 1, lime 2, yellow 3, orange 4, magenta 5 or more). An item slot gets the count as its first lore line.
- Right-clicking (or shift-right-clicking) a hidden slot marks it as a suspected seized pin (red pane). Marked slots cannot be probed until right-clicked again. Only a left click probes, so a number key, drop or double click on a hidden slot does nothing. The title's `Seized: N` counts pins not yet marked.
- Probing a seized pin snaps one lockpick, reveals every seized pin (iron bars) and stops probing. Slots already revealed can still be taken, as before.
- Items under seized pins cannot be reached in that session.

Pin count = chest slots x `lockpicking.chest.seized-density` (0.3) x break chance x the lock type's `break-chance-multiplier`, rounded, plus `seized-per-slip` (1) for each slip on the ring (the older `seized-per-grid-mistake` key is still read). Break chance is `1 - success chance`, from `base-success-chance`, Dexterity (`dex-map`) and pick strength, capped by `max-success-chance`. With an iron pick (0.35), a 27-slot chest at Dexterity 0 hides 5 pins, and a 54-slot double chest hides 11. At Dexterity 40 the chest hides none before slips. Risk gain per probe and clue drops are unchanged.

## Bar engine

`LockPickManager` is the only bar.

- Cooldown identity is a **string target id**:
  - Doors: `door:<world>:<x>:<y>:<z>`
  - Entities: `entity:<uuid>`
- `SessionKind`: `DOOR` and `DISPLAY` (furniture, armor stand, and item frame all use `DISPLAY`).
- `DoorLockpick.ProximityAnchor` has `DoorProximityAnchor` and `EntityProximityAnchor` implementations (both use `door-max-distance`).
- `startDoorSession` is a thin wrapper. Displays call the shared `startSession`.
- Fail and break call `cancelSession(uuid, true)` so they share `lockpickFailCooldownMs`.
- Right-click while already in a session for **that** target is select. Starting a session cancels (and penalizes) any previous one.

Display bar difficulty uses config `lockpicking.display-lock-strength` (no key). Same formula as doors:

`effectiveStrength = strength * (1 - pickStrength * lockpickMaxReduction)`

Honor `min-lock-strength-ratio` against that display strength.

## Lock state

Reuse `LockState` (`PRIVATE` / `GUILD` / `FACTION` / `PUBLIC`) and the same access rules as `ContainerData.canAccess` (owner, same guild, same faction, public, `thievery.admin` bypass). `FACTION` is every guild in the owner's faction. Vassals are not included. Chest lockpick sessions scale budget, risk, critical chance, and break chance from `lockpicking.lock-types`.

Shift left-click is the toggle (same titles/sound as chests). The owner rotates state; staff with `thievery.admin` can also rotate a lock another player owns, and the placer stays the owner. Shift left-click **never** breaks a lockable display.

### Lock change logging

Each rotation on a container, display or furniture lock is logged to CoreProtect through `CoreProtectAPI.logLockChange` (`LockStateLog`). Lookups and the block inspector show the entry under the player's own name with the new state, for example "Steve set chest lock to Private.", and add "(staff override)" when staff changed a lock another player owns. Lock changes are never rolled back.

- A double chest is logged once, on the half that was clicked.
- CoreProtect drops interactions on air, so display and furniture changes are logged on the block holding the display: the block an item frame hangs on, or the block below other displays. The entry names that block rather than the display.
- Claiming an unowned display on the first toggle is not logged.
- Logging needs CoreProtect API 14 (CoreProtect 25.1.0) or later. Older versions, or servers without CoreProtect, skip logging.

If the player cannot access a locked display, cancel:

- IF: `FurnitureBreakEvent`, slot take/add, empty-hand pickup
- Armor stand: `PlayerArmorStandManipulateEvent`, damage
- Item frame: interact (rotate/insert), punch-out, hanging break

Owner / guild / public access still allows legitimate break and take.

Owner is set on place (`FurniturePlaceEvent`, `EntityPlaceEvent`). If missing, the first successful owner toggle may claim it.

## Persistence (entity-capable)

`ContainerDataManager` is block-file keyed. Do not reuse it for entities.

**Vanilla entities** (armor stand, item frame, glow item frame): `plugins/Thievery/entities/<uuid>.json` (`owner`, `lockState`). Delete on entity remove.

**IF furniture:** do not key only by `Furniture.getEntityId()`. Restore can respawn the ItemDisplay and change the UUID (`FurnitureRestoreHandler.ensureDisplay`). Store `thievery.owner` and `thievery.lockState` in `Furniture.getVariables()` and `persistFurniture`. The lock follows pickup, chunk reload, and respawn.

Config:

```yaml
lockpicking:
  lockable-furniture:
    - artifact_display
    - pedestal
  lockable-entities:
    - ARMOR_STAND
    - ITEM_FRAME
    - GLOW_ITEM_FRAME
  display-lock-strength: 0.5
```

Only listed IF ids are lockable. Listed entity types are all lockable.

Thievery softdepends InteractibleFurniture. Register IF listeners only when IF is present.

## Robbery (success loot)

Start the bar only if the player does not already have access (same as chests; honor `debug-allow-own-chest`). Apply the chest **thief trait** check (`Cache.traits`). Reuse door start checks: clues, guild-online, fail cooldown, lockpick strength.

Contents:

- IF: items in `getActiveSlots()`
- Armor stand: helmet, chest, legs, boots, main hand, offhand
- Item frame: the framed item

**Gate:** at least one item the thief can take: `CategoryHandler.canRevealItem` (loadout) and `StealBudget.computeTakeableAmount` > 0, using lockpick `capacity`. Bundles: `ItemValue.hasStealableContents` / `canStealAnything`. If none, refuse.

On **SUCCESS**: shuffle slots, walk that order (armor stand piece is luck). For each:

- Skip if not on loadout or over remaining budget
- `addItem`; if it does not fit, **leave it in the display** (no world drop)
- Charge `StealBudget` from the lockpick capacity

On **FAIL / BREAK**: same titles, sounds, and lockpick break as `DoorManager.handleSelectResult`. Cooldown is already applied by `LockPickManager`.

When removing IF slot items, fire `FurnitureSlotItemTakeEvent` first. If another plugin cancels (meditation lock, etc.), skip that slot.

## Risk and clues

Starting the bar uses `RiskSource.DOOR` (same minigame). After a successful dump, drop door-style clues at the display location (owner UUID). Do not open a chest GUI or ramp chest break chance.
