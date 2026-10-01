# Thievery display locks - Test matrix

Run these checks before releasing display-lock changes. Player-facing strings must not contain U+2014.

Run these checks on Minecraft **1.21.10** with the intended plugin dependencies and JVM from the [shared platform baseline](../../../PLATFORM.md). Record the source revision, server build, JVM and results; the checklist alone is not evidence of a passing release.

## Regression

| # | Check |
|---|--------|
| R1 | Door lockpick bar still runs; success opens door |
| R2 | Door fail/break applies 60s on that door only |
| R3 | Walking away cancels door pick |
| R4 | Chest GUI lockpick unchanged once the pin grid is solved |

## Chest pin grid

| # | Check |
|---|--------|
| G1 | Lockpick right-click on a chest opens the 6x6 grid; pins light for 4s, then hide |
| G2 | Setting every pin opens the hidden probe menu; probing, breaks, clues and taking behave as before |
| G3 | Three wrong cells: missed pins show yellow, grid closes, the chest refuses another attempt for 60s |
| G4 | Timer runs out: same as G3; the boss bar turns red with ticks for the last 3 seconds |
| G5 | Closing the grid early counts as a failure; logging out mid-grid does too |
| G6 | Failure snaps one lockpick about half the time (`fail-break-chance`); a stack loses one |
| G7 | A higher-Dexterity character gets more recall time |
| G8 | A second thief cannot start on a chest whose grid is running ("Someone is already picking this lock!") |
| G9 | Shift-click, number keys, drag and offhand swap in the grid move no items |
| G10 | A failed grid does not start the multi-day access cooldown; a solved grid does |
| G11 | `minigame.enabled: false` opens the probe menu straight away |
| G12 | Vanilla client without the resource pack sees the grid correctly |
| G13 | First probe never hits a seized pin; it and its neighbours show counts |
| G14 | Empty probed slots show the count by colour and stack size; item slots show it in the first lore line |
| G15 | Right-click marks and unmarks a hidden slot; a marked slot cannot be probed; the title `Seized:` count drops per mark |
| G16 | Probing a seized pin snaps one lockpick, shows every seized pin, and stops probing; revealed items can still be taken |
| G17 | Two wrong grid cells add two seized pins to the chest |
| G18 | High Dexterity or a strong pick on a small chest leaves few or no seized pins |
| D1 | Over several attempts, roughly half the chests open the dial instead of the grid |
| D2 | Dial: hovering the menu and pressing the shown key while the pick is in the cyan zone sets a tumbler; four tumblers open the probe menu |
| D3 | Dial: too soon, too late, the wrong key, or a full sweep without a press each add a red slip; three slips fail with the grid's penalties |
| D4 | Dial: presses with 100-200 ms ping still land where the pick looked; keys 5-9 and mouse clicks do nothing |
| D5 | Dial: slips add seized pins to the probe menu like wrong grid cells |

## Lock toggle and access

| # | Check |
|---|--------|
| L1 | Shift left-click on `artifact_display` / `pedestal` cycles PRIVATE / GUILD / FACTION / PUBLIC, does not break |
| L2 | Non-owner shift left-click does not break and does not change state |
| L3 | Stranger cannot take slot items from a PRIVATE locked display |
| L4 | Owner can take and can break |
| L5 | Guild member can access GUILD; outsider cannot |
| L5b | Faction member in another guild can access FACTION; another faction cannot |
| L6 | PUBLIC anyone can take/break |
| L7 | Unlisted IF type still breaks on left-click as today |
| L8 | Armor stand: sneak-hit toggles; locked stand cannot be stripped or killed by stranger |
| L9 | Item frame / glow frame: sneak-hit toggles; locked frame cannot be rotated, emptied, or broken by stranger |
| L10 | Chunk unload/reload: furniture lock still there (variables). Armor stand / frame lock still there (uuid file) |
| L11 | Pick up and replace furniture: lock still on that piece |
| L13 | Shift left-click on an owned chest, display and furniture: `/co inspect` or `/co lookup` shows `<player> set <block> lock to <state>.`; display and furniture entries sit on the supporting block |
| L14 | Staff shift left-click on another player's lock changes state, keeps the owner, and logs with "(staff override)" |

## Robbery

| # | Check |
|---|--------|
| S1 | Lockpick right-click starts the **same** bar (title dashes, risk line) |
| S2 | Already have access: refuse (unless `debug-allow-own-chest`) |
| S3 | No stealable item (wrong loadout or over capacity): refuse, no bar |
| S4 | One cheap legal item among illegal/expensive: bar allowed |
| S5 | Success: items leave in shuffled order; inventory full leaves remainder in the display (no ground dump) |
| S6 | Armor stand: sometimes helm, sometimes legs first across attempts |
| S7 | Fail: 60s on that entity; second pick blocked until expiry |
| S8 | Break: lockpick consumed, same 60s |
| S9 | Walk away: cancel, penalty cooldown |
| S10 | Meditation-locked pedestal slot: take event cancel skips that slot |
| S11 | Missing thief trait: refuse like chests |
| S12 | Weak pick vs `display-lock-strength` * min ratio: refuse |

## Polish

| # | Check |
|---|--------|
| P1 | Display cancel message does not say "door" |
| L12 | Break/kill display deletes entity lock file |
| P2 | No U+2014 in new messages or titles |

## Money and player robbery

| # | Check |
|---|--------|
| M1 | Loadout **without** `money`: Denar coin stacks hidden/unstealable in pickpocket, chest steal, display dump |
| M2 | Loadout **with** `money`: coin steal value = `coin.value * stack * amount_per_money`; budget limits quantity |
| M3 | `/robbery start` + accept: GUI slot 8 (top-right) shows pouch when victim balance > 0 and thief has `money` |
| M4 | Slot 8 left-click takes up to `pouch-click-amount` (10); shift-left up to `pouch-shift-amount` (100) |
| M5 | Pouch take capped by victim balance, remaining budget (`floor(remaining / amount_per_money)`), and config amounts |
| M6 | Pouch debits victim DenarEconomy pouch, credits robber pouch (not coin items); GUI title budget updates |
| M7 | Without `money` in loadout: slot 8 is filler; coins in shuffled grid stay hidden |
| M8 | Victim with 7 denars: single click takes 7 |
| M9 | Grave steal **without** `money`: coins in grave are skipped; message "nothing you can steal" if only coins |
| M10 | Grave steal **with** `money`: coins taken greedily like other items |
| M11 | No U+2014 in new player-facing strings (pouch pane, grave rob hint, steal messages) |
