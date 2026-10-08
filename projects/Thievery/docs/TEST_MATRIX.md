# Thievery display locks - Test matrix

Run these checks before releasing display-lock changes. Player-facing strings must not contain U+2014.

Run these checks on Minecraft **1.21.10** with the intended plugin dependencies and JVM from the [shared platform baseline](../../../PLATFORM.md). Record the source revision, server build, JVM and results; the checklist alone is not evidence of a passing release.

## Regression

| # | Check |
|---|--------|
| R1 | Door lockpick bar still runs; success opens door |
| R2 | Door fail/break applies 60s on that door only |
| R3 | Walking away cancels door pick |
| R4 | Solving a minigame opens the chest probe menu; budget, clues and taking items work as before (seized pins replace the random break roll, see G13-G18) |

## Chest lock minigames

| # | Check |
|---|--------|
| G1 | Lockpick right-click on a chest opens the pin grid dialog about half the time; lamps scan on row by row, hold for 4s, then go dark |
| G2 | Every grid cell shows its texture (unlit lamp, lit lamp, sea lantern, redstone block, gold block); no stray dots are visible, hovered or not |
| G3 | Clicking the pins plays a rising scale; a wrong cell plays a bass note and shows a redstone block; the status line counts pins and slips |
| G4 | Setting every pin opens the probe menu with seized pins (G13-G18); clues and taking behave as before |
| G5 | Three wrong cells or the timer running out shows missed pins in gold, applies the 60s cooldown and may snap the pick; the title's countdown (and the pack's strip) turns red and ticks for the last 3 seconds; no boss bar shows |
| G6 | Escape does not close the grid; "Give up" does, and counts as a failed attempt |
| G7 | Clicking pins as fast as possible sets every one; none are dropped while the dialog redraws |
| G8 | With `grid.pack: true` and the pack loaded, the grid is one dark board of square tiles with a rim; the hovered tile shows a white outline; Give up is a red plate closing the bottom of the board |
| G9 | With the pack, the strip along the board's top drains gold while memorising, then green, then red for the last 3 seconds; the title counts down the seconds |
| G10 | Failing on one half of a double chest puts both halves on the fail cooldown; a second thief cannot start on either half while one is working it |
| G11 | A failed pick with a different item forced into the hand never breaks that item |
| G12 | A guildmate opening a nearby chest's probe menu while you work this lock stops your probe menu opening, with the access cooldown message |
| D1 | The other half of picks float the lockpick ring in front of the thief; nobody else nearby sees it |
| D2 | A white needle with a dark edge crosses the dots, stays sharp at every angle, and glides smoothly round the ring at the client's frame rate |
| D3 | The middle shows the thief's own key: W/A/S/D on QWERTY, Z/Q/S/D on AZERTY, rebound keys if rebound; pressing it in the green sets a tumbler pin |
| D4 | The hotbar never changes; the thief cannot walk or jump, the field of view does not change, but they can look around |
| D5 | Too soon, too late, the wrong key, two keys at once, or a full pass without a press is a slip, and one slip fails with the grid's penalties |
| D6 | Each tumbler narrows the zone and reverses the sweep; notch clicks rise inside the zone |
| D7 | Picking while looking at a chest or wall up close, looking down at a chest on the ground from 1-4 blocks, or looking up at a raised chest floats the whole ring in front of it, never partly inside it |
| D8 | Sneak gives up; taking damage fails; being teleported away by staff ends the pick without a penalty; an ender pearl, chorus fruit or your own command teleport counts as a failed attempt |
| D9 | Logging out mid-ring fails the attempt and the next join walks and jumps normally; a crash mid-ring is undone on the next join |
| D10 | Riding a mount or gliding refuses to start the ring; a flying staff member is set down and can fly again afterwards |
| D11 | With 100-200 ms ping, presses still land where the pick looked |
| D12 | `/thievery testpick grid` and `/thievery testpick dial` force each minigame for staff |
| D13 | Starting a second pick while in one says "You're already working a lock." |
| D14 | During the ring, scrolling the hotbar, dropping, swapping hands, moving items and right-clicking a horse or boat do nothing |
| D15 | Starting the ring mid-jump lands the thief normally, with no flying kick, and the ring appears in front of them once they land |
| D16 | During the ring, right-clicking a locked door or a grave does nothing |
| D17 | `/thievery reload` during a minigame ends it without a penalty; the thief can move again |
| G13 | First probe never hits a seized pin; it and its neighbours show counts |
| G14 | Empty probed slots show the count by colour and stack size; item slots show it in the first lore line |
| G15 | Right-click (or shift-right-click) marks and unmarks a hidden slot; a marked slot cannot be probed; number keys and double clicks never probe; the title `Seized:` count drops per mark |
| G16 | Probing a seized pin snaps one lockpick, shows every seized pin, and stops probing; revealed items can still be taken |
| G17 | Two wrong grid cells or ring slips add two seized pins to the chest |
| G18 | High Dexterity or a strong pick on a small chest leaves few or no seized pins |

## Pickpocket ring

| # | Check |
|---|--------|
| P1 | `/pickpocket start` and right-clicking a player within reach floats the gauge in front of the thief; nobody else sees it, and the mark sees nothing |
| P2 | The middle shows the thief's own jump key; mashing it fills the band clockwise from the top in cyan, and it drains when they stop |
| P3 | Filling the first phase pops its pip green; the second phase starts empty in orange and needs about twice as many presses |
| P4 | Filling both says "Got it" and opens the hidden pocket menu; budget, clues and taking items work as before |
| P5 | Letting the boss bar run out, sneaking or taking damage says "Noticed", shows the mark the alert subtitle and refuses that mark for 60s with "Your mark is still on guard" |
| P6 | The mark walking out of reach or logging out ends the ring with "Your mark is out of reach." and no alert |
| P7 | The thief cannot walk or jump during the ring, the hotbar does not change, and they move normally afterwards |
| P8 | `/thievery testpick pocket` plays the ring for staff with no mark and says "Pocket picked." when filled |

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
