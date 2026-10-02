# Thievery - Display locks

Steal from lockable **displays**: InteractibleFurniture types, armor stands, and item frames. Chests and doors stay as they are.

See [TEST_MATRIX.md](TEST_MATRIX.md) for the manual checklist.

## Responsibilities

| Target | Lock model | Robbery | Fail |
|--------|------------|---------|------|
| Doors | Key + strength (`DoorData`) | Title **bar** | 60s on that door |
| Chests / barrels / etc. | Owner + `LockState` | **Pin grid** dialog or floating **lockpick ring**, then hidden **GUI** probe with seized pins | Grid: 60s on that chest (`fail-cooldown-ms`). Probe: access-map cooldown |
| IF furniture, armor stands, item frames | Owner + `LockState` (chest model) | Same **bar** as doors | Same 60s as doors (`fail-cooldown-ms`) |

## Chest hopper automation

When a **block hopper** moves items (`InventoryMoveItemEvent`), allow pull/deposit only if the hopper and every involved block container (chest, barrel, hopper, etc.) share the same **non-null owner UUID**. Guild/PUBLIC player access does not apply to hoppers — only owner equality. Unowned containers block automation; hopper minecarts are not covered. Droppers and other initiators are unchanged.

Displays do not use the chest GUI. Doors and displays share one engine.

## Chest lock minigames

Right-clicking a chest with a lockpick runs every existing chest check (trait, access, owner online, clues, already picking, held lockpick, access-map cooldown), then `LockMinigameManager` opens a lock minigame instead of the probe menu: the floating lockpick ring for `minigame.dial-chance` (50%) of attempts, otherwise the pin grid dialog. Both are `LockMinigame` subclasses (`PinGridGame`, `RingDialGame`) and share the boss bar, the end-of-game pause, the failure rules and the cooldown below. Staff can force either with `/thievery testpick [grid|dial]` while looking at a container and holding a lockpick; it skips the trait, clue, ownership and access checks.

### Pin grid (dialog)

Modelled on the NoPixel thermite minigame and shown as a vanilla dialog (`GridDialogs`), so it works on unmodded clients. Each cell is a button showing a block texture: an unlit redstone lamp, a lit lamp while memorising, a sea lantern once set, a redstone block for a wrong cell and a gold block for a pin missed on a fail. `minigame.grid.sprites: false` draws coloured squares instead. The puzzle state lives in `PinGrid`; `GridScreen` is one frame of the dialog.

1. Prepare (`prepare-seconds`): every lamp unlit.
2. Scan: the pins light row by row, two ticks a row, with a rising tick.
3. Memorise (`memorise-seconds`): every pin lit.
4. Recall (`recall-seconds` + `recall-seconds-per-dexterity` x Dexterity): the lamps go dark and the thief clicks the pins. Each correct pin plays the next note of a pentatonic scale; a wrong cell plays a bass note. The boss bar is the timer and ticks red for the last 3 seconds.

The dialog cannot be closed with Escape; "Give up" is the way out and counts as a failed attempt. The dialog is redrawn only when something changes. A quick thief often clicks again before the redrawn frame arrives, so a cell click counts whichever frame it came from; a cell is the same cell on every frame, and clicking a cell twice does nothing. Buttons from an old dialog stop working once that game ends, is cancelled or is replaced by a new one.

A dialog button whose label is only a texture draws nothing on 1.21.10 clients, so each label is a one-pixel dot in the button's face colour (no shadow) followed by the texture, tinted white.

### Lockpick ring (display entities)

Modelled on the NoPixel lockpick minigame. `RingView` floats a ring of 24 dots in front of the thief, made of display entities that only the thief can see: the tumbler pins and slip marks above it, the key to press in the middle, and the thief's own lockpick (a copy of the held item, glowing gold) as the pick. The server sends the pick's position two ticks ahead and lets the client interpolate, so it moves at the player's own frame rate rather than in 20-a-second steps.

- Keys are the movement keys, read from the player input packet (`PlayerInputEvent`), so the thief's hotbar never changes. The middle shows a keybind component, so each player sees their own key for forward, left, back or right (Z/Q/S/D on AZERTY, or their rebinding). Sneak gives up.
- The thief is held still while picking (`LockFreeze`): walk speed 0, which also keeps the field of view unchanged, a transient jump modifier, and flight switched off and restored afterwards. Movement events hold the thief's horizontal position against knockback, water or a nudge, but allow looking around and falling, so a thief who started mid-jump lands rather than hovering until the server kicks them for flying. Hotbar scrolling, dropping, swapping hands, inventory clicks and mounting a horse or boat are cancelled, so the lockpick stays in hand. The original walk speed is stored on the player, so a crash mid-pick is undone on their next join.
- Each pass (`Sweep`) takes `dial.min-lap-seconds` to `dial.max-lap-seconds`, plus `dial.lap-seconds-per-dexterity` per Dexterity level, with a zone of `dial.zone-width` of the ring somewhere after the first third. Each set tumbler narrows the zone by `dial.zone-shrink-per-tumbler` (never below 40%) and, with `dial.alternate-direction`, reverses the sweep like a combination lock.
- Quiet clicks mark each notch the pick passes; they rise in pitch inside the zone.
- A press is judged where the pick was `ping / 50ms` ticks earlier (up to `dial.max-lag-ticks`), which is what the thief saw. A hit pops a pin and a green burst; too soon, too late, the wrong key, two keys at once (fumbled) or a full pass without a press is a slip, with a red flash and smoke. Particles are sent to the thief only.
- The ring floats at `dial.distance` blocks, or at most 60% of the way to the block being looked at, scaled so it looks the same size, and slightly above the crosshair to clear the action bar.
- Setting `dial.tumblers` (4) solves the lock. `mistakes-to-fail` slips fail it. Slips count as mistakes for seized pins, the same as wrong grid cells.
- You cannot start the ring while riding or gliding.

### Failure and interruptions

Failing means `mistakes-to-fail` wrong cells or slips, the grid's recall timer running out, giving up (the dialog button or sneak), being hurt, or logging out mid-pick. On failure:

- On the grid, the missed pins show as gold.
- `LockPickManager.applyCooldown` puts the chest's target id `chest:<world>:<x>:<y>:<z>` on `fail-cooldown-ms`. A new attempt is refused until it expires, and `/thievery` cooldown resets clear it.
- `fail-break-chance` rolls whether one lockpick from the main-hand stack snaps.

Ending without a penalty: being teleported away (another world, or more than a block), the chest being broken, a reload or a shutdown. Logging out after solving gives no reward. A thief already in a minigame is told "You're already working a lock." and cannot start another; a player in a minigame counts as already picking that chest. Chest access, nearby pings and the multi-day access cooldown are recorded only when the probe menu opens. `lockpicking.chest.minigame.enabled: false` skips the minigame.

## Chest probe: seized pins

The probe menu is a minesweeper-style puzzle instead of a random break roll. `SeizedPins` hides seized pins among the menu's chest slots, using the menu's nine-column grid for adjacency.

- Pins are placed on the first probe. That slot and, when there is room, its eight neighbours stay clear, so the first probe always reveals something.
- Each safe probe shows how many of the eight surrounding slots hide a seized pin. An empty slot becomes a glass pane whose colour and stack size give the count (white 0, light blue 1, lime 2, yellow 3, orange 4, magenta 5 or more). An item slot gets the count as its first lore line.
- Right-clicking a hidden slot marks it as a suspected seized pin (red pane). Marked slots cannot be probed until right-clicked again. The title's `Seized: N` counts pins not yet marked.
- Probing a seized pin snaps one lockpick, reveals every seized pin (iron bars) and stops probing. Slots already revealed can still be taken, as before.
- Items under seized pins cannot be reached in that session.

Pin count = chest slots x `lockpicking.chest.seized-density` (0.3) x break chance x the lock type's `break-chance-multiplier`, rounded, plus `seized-per-grid-mistake` (1) for each wrong cell on the pin grid or slip on the dial. Break chance is `1 - success chance`, from `base-success-chance`, Dexterity (`dex-map`) and pick strength, capped by `max-success-chance`. With an iron pick (0.35), a 27-slot chest at Dexterity 0 hides 5 pins, and a 54-slot double chest hides 11. At Dexterity 40 the chest hides none before grid mistakes. Risk gain per probe and clue drops are unchanged.

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
