# Thievery display locks - Test matrix

Run these checks before releasing display-lock changes. Player-facing strings must not contain U+2014.

Run these checks on Minecraft **1.21.10** with the intended plugin dependencies and JVM from the [shared platform baseline](../../../PLATFORM.md). Record the source revision, server build, JVM and results; the checklist alone is not evidence of a passing release.

## Regression

With TLibs **2.4.0**, RPCharacters **2.16.0** or newer, SimpleFactions **4.0.0**
and DenarEconomy **0.3.0**, check a restricted command,
container lockpick and display lockpick while the character is loading, after
loading a character with the required trait, and after switching to one without
it. Only the matching ready character should pass the trait restriction. Switch
back and repeat after changing that character's traits; the next check must use
the current traits. Confirm unrestricted lists still permit access (the
pickpocket loader defaults its empty list to `thief`). Configure a trait in
mixed case (`Thief`) and confirm it matches. For player robbery, send a request,
switch the robber to another character and back, then accept: the request must
have expired. Repeat with the victim switching. On a server with TLibs older
than 2.3.0, Thievery must stay enabled, locked chests and doors must stay
protected, and trait-restricted actions must be refused. Record these results in
addition to the checks below.

| # | Check |
|---|--------|
| R1 | Door lockpick bar still runs; success opens door |
| R2 | Door fail/break applies 60s on that door only |
| R3 | Walking away cancels door pick |
| R4 | Solving the ring opens the chest probe menu; budget, clues and taking items work as before (seized pins replace the random break roll, see G13-G18) |

## Hands-up inventory inspection

With ItemsAdder and the [hands-up asset](../../ServerAssets/handsup-emote.md)
installed, use two ordinary players. Run `/handsup` on one: both arms should
rise over 0.8 seconds and remain raised without resetting at the loop boundary.
Check another player's view, skins with classic and slim arms, equipped armour,
held items, and walking. Right-click the posed player with the
other. Confirm main inventory, hotbar, armour, off-hand, custom names and lore
match. Change the target's items and check the display updates. Try ordinary
clicks, shift-clicks in both inventories, drags spanning both inventories,
number keys, off-hand swaps, double-click collection and dropping. Repeat
middle-click cloning in creative mode. No items should transfer, disappear or
duplicate. Test with a nonempty cursor and confirm closing returns those items
normally.

Open two inspections of the same player, then lower their hands: both views
must close. Repeat with sneak, jumping, taking/dealing damage, replacing the
emote, disconnect, death, teleport and switching characters. After each, confirm
the pose ends and inspection cannot reopen. Test shutdown with a posed player
who has no viewers. A different emote must not be stopped by inspection cleanup.
Walk more than four blocks apart and check the view closes. Restart and confirm
consent starts off. Ordinary chests must still allow item movement. Arm
`/robbery start` or `/pickpocket start`, then right-click a consenting player:
only inspection should open. Repeat while sneaking and holding an off-hand
item on the viewer; there must be no duplicate window or theft attempt.

On an isolated fixture, test missing ItemsAdder, a missing `tfmc_handsup`
animation, and another plugin cancelling the emote start. `/handsup` must report
failure and leave inspection off. Starting `tfmc_handsup` directly through
ItemsAdder must not grant inspection access.

## Chest lock minigame

| # | Check |
|---|--------|
| G4 | Setting every tumbler opens the probe menu with seized pins (G13-G18); clues and taking behave as before |
| G10 | Failing on one half of a double chest puts both halves on the fail cooldown; a second thief cannot start on either half while one is working it |
| G11 | A failed pick with a different item forced into the hand never breaks that item |
| G12 | A guildmate opening a nearby chest's probe menu while you work this lock stops your probe menu opening, with the access cooldown message |
| D1 | Every lockpick right-click on a chest floats the lockpick ring in front of the thief; nobody else nearby sees it |
| D2 | A white needle with a dark edge crosses the dots, stays sharp at every angle, and glides smoothly round the ring at the client's frame rate |
| D3 | The middle shows the thief's own key: W/A/S/D on QWERTY, Z/Q/S/D on AZERTY, rebound keys if rebound; pressing it in the green sets a tumbler pin |
| D4 | The hotbar never changes; the thief cannot walk or jump, the field of view does not change, but they can look around |
| D5 | Too soon, too late, the wrong key, two keys at once, or a full pass without a press is a slip, and one slip fails, applies the 60s cooldown and may snap the pick |
| D6 | Each tumbler narrows the zone and reverses the sweep; notch clicks rise inside the zone |
| D7 | Picking while looking at a chest or wall up close, looking down at a chest on the ground from 1-4 blocks, or looking up at a raised chest floats the whole ring in front of it, never partly inside it |
| D8 | Sneak gives up; taking damage fails; being teleported away by staff ends the pick without a penalty; an ender pearl, chorus fruit or your own command teleport counts as a failed attempt |
| D9 | Logging out mid-ring fails the attempt and the next join walks and jumps normally; a crash mid-ring is undone on the next join |
| D10 | Riding a mount or gliding refuses to start the ring; a flying staff member is set down and can fly again afterwards |
| D11 | With 100-200 ms ping, presses still land where the pick looked |
| D12 | `/thievery testpick` runs the ring for staff on the targeted container, even with the minigame off |
| D13 | Starting a second pick while in one says "You're already working a lock." |
| D14 | During the ring, scrolling the hotbar, dropping, swapping hands, moving items and right-clicking a horse or boat do nothing |
| D15 | Starting the ring mid-jump lands the thief normally, with no flying kick, and the ring appears in front of them once they land |
| D16 | During the ring, right-clicking a locked door or a grave does nothing |
| D17 | `/thievery reload` during a minigame ends it without a penalty; the thief can move again |
| G13 | First probe never hits a seized pin; it and its neighbours show counts |
| G14 | Empty probed slots show the count by colour and stack size; item slots show it in the first lore line |
| G15 | Right-click (or shift-right-click) marks and unmarks a hidden slot; a marked slot cannot be probed; number keys and double clicks never probe; the title `Seized:` count drops per mark |
| G16 | Probing a seized pin snaps one lockpick, shows every seized pin, and stops probing; revealed items can still be taken |
| G17 | With `dial.mistakes-to-fail` raised, two ring slips add two seized pins to the chest |
| G18 | High Dexterity or a strong pick on a small chest leaves few or no seized pins |

## Pickpocket ring

| # | Check |
|---|--------|
| P1 | `/pickpocket start` and right-clicking a player within reach floats the gauge in front of the thief; nobody else sees it, and the mark sees nothing |
| P2 | The middle shows the thief's own jump key; mashing it fills the band clockwise from the top in cyan, and it drains when they stop |
| P3 | Filling the first phase pops its pip green; the second phase starts empty in orange and needs about twice as many presses |
| P4 | Filling both says "Got it" and opens the hidden pocket menu; budget, clues and taking items work as before |
| P5 | Letting the boss bar run out, sneaking or taking damage says "Noticed", plays the mark a bag rummaging sound with no title and refuses that mark for 60s with "Your mark is still on guard" |
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
| L15 | Your alt on the same account cannot open your PRIVATE chest, rotate it, clear its clues or merge a chest onto it |
| L16 | Placing a chest with no character selected leaves it unowned; staff with no character place a PRIVATE server chest only the staff override opens |
| L17 | A dead owner's GUILD chest still opens for the guild they died in; a revived owner's old guild has no access |
| L18 | A hopper minecart under an owned PRIVATE chest (either half of a double chest) takes nothing; under a PUBLIC or unowned chest it works |
| L19 | A block hopper under its owner's chest moves items; an alt's hopper under the same chest does not; server hoppers move between server chests |
| L20 | A double chest whose halves have two owners cannot be rotated or picked and appears in `/thievery locks quarantine` until `/thievery locks setowner` fixes it |
| L21 | Restart with RPCharacters failing to load: locks stay frozen ("Locks are starting up"), owned chests stay shut, key holders open doors, nothing in `plugins/Thievery/data` changes; the next good restart migrates |
| L22 | First boot on an old store: `Lock migration:` log line with counts and duration, `migrations/backup/locks-0001.zip`, a completed `journal-0001.json`, `data-version` in each store; a second boot changes nothing |
| L23 | Decided estate, restart: the dead owner's PRIVATE and PUBLIC chests, displays and doors go to the property recipient, GUILD and FACTION ones to the death guild's leader, states and thief cooldowns kept; `Estate <deathId> … locks DONE` in the log and `/estate show` lists the moved paths |
| L24 | A double chest of the dead owner's moves as a whole; a door's owner passes but the old keys still open it |
| L25 | Waiting guild part: GUILD chests stay with the dead owner and keep opening for the death guild; after a leader is chosen, the next restart moves them |
| L26 | Furniture of a dead owner with a decided estate passes to the recipient on the first interaction after the decision |
| L27 | Force the estate planner to fail (for example by stopping RPCharacters' estate service): the log shows the planner warning, locks still reach normal operation, the estate shows RETRY |
| L28 | `/thievery locks setowner <dead character's UUID>` is refused |
| L29 | `tools/thievery_rollback.py --estate-only --apply` with the server stopped restores only the estate moves and keeps the journals and `data-version` |

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
| M6 | Pouch debits the captured victim character, credits the captured robber character; only an applied transfer updates the budget |
| M7 | Repeat one payout attempt after ledger failure: reuse its operation ID and amount, charge budget once; a closed ledger or unwritable payment folder takes nothing |
| M8 | Switch either character after acceptance: no transfer from the new character; faction waiting grants no protected access |
| M7 | Without `money` in loadout: slot 8 is filler; coins in shuffled grid stay hidden |
| M8 | Victim with 7 denars: single click takes 7 |
| M9 | Grave steal **without** `money`: coins in grave are skipped; message "nothing you can steal" if only coins |
| M10 | Grave steal **with** `money`: coins taken greedily like other items |
| M11 | No U+2014 in new player-facing strings (pouch pane, grave rob hint, steal messages) |
