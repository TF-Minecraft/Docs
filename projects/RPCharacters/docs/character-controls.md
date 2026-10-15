# Character controls and combat

[Project index](../README.md)

Commands and configuration below describe the bundled defaults on `main`. Server configuration can override them.

## Character selection

With [separate bodies](character-bodies.md) enabled, login opens the character
selection dialog. `/rpcharacter menu` reopens it while selecting; while playing,
it returns you to selection after you stand still for five seconds. Each character has
its own items and progression. `/linkdiscord` remains available in selection.

Under each character's card, **Background** opens the character's background on
its own page, and **Traits** and **Clues** show on hover. **End character** asks twice, then kills the character for good
and moves it to Memorials; only staff can revive it. Staff use
`/rpcharacter menu <player>` for the chest view of another player's characters,
where they can revive dead ones.

See [in-game character creation](character-creation.md) for the dialog wizard,
Back/Next, draft resumption and review editing.

## Mail recipient visibility

`/rpcharacter mail` toggles whether your active character appears in BirdMessenger’s recipient list; `/rpcharacter mail off` hides it and `/rpcharacter mail on` restores it. Characters are listed by default, and the setting persists across logouts and restarts. Already-sent mail still arrives.

## Character focus

Focus is a shared, regenerating per-character resource used by Research and Magic. Right-clicking a Focus Potion restores 50 focus (set in `focus.yml` under `restore_items`); it is not used up while focus is full.

## Class picks

`/class` and `/rpcharacter class` open the base-class window. `/subclass`, `/rpcharacter subclass` and the Subclasses button open a separate window showing only the active character's class family, in place of MMOCore class points.

A character's first class and first subclass are free. Other picks are priced like the class creation stage: free during its lock-time (5 days), then the `paid-changes` class rule (100, 1000, 3000 denars). `class-selection.change-cost` is used only when there is no class rule. `infinite-points: true` makes every pick free, for the tutorial server. A class picked above a skill-slot level still gets the slots its exp table unlocks.

Paid picks, and paid changes to a locked creation stage, are charged to the character being changed: the whole price comes from its own pouch or bank, tried in the configured `accounts` order. This needs DenarEconomy 0.3.0. RPCharacters saves the payment on the character, with its debit and refund operation IDs, and forces the file and its folder to disk before it posts the debit. If the server stops part way, the next join asks the ledger whether the debit went through. A debit that never applied is dropped without a refund. An applied one is kept when the change stuck and refunded otherwise, always with the stored refund ID, so a retry never pays twice. A paid class pick whose class could not be applied is marked for refund, so reaching that class later never counts as using it. While a payment is held, the character cannot open a stage edit or pick a class until it settles. A payment held from before the character ledger is treated as already taken from the account's money. It is always refunded to the account's legacy heir, whatever the character has changed since, and waits until heirs are known.

Staff with `class-selection.reset-permission` (`rpchar.class.reset`) can run `/rpcharacter admin resetclasses confirm` to give every character a fresh class window: class and subclass changes are free for the lock-time again, paid prices start over and the first subclass is free again. Online characters start now, offline ones when they next join. The reset count is kept in `data/class-resets.yml`.

With separate bodies disabled, the class level is shared by every character and
kept in the player file (`account-class-level`). Enabling bodies gives each
character its own saved class level. A class capped below the saved level, such
as a base class, shows its cap without lowering the level available to that
character's other classes. Legacy accounts start from MMOCore's saved level.

## Nonlethal knockouts

GSit holds downed players in a crawl pose for the knockout duration, alongside freeze and blindness. The pose uses GSit's API, bypasses command restrictions, respects other plugins' crawl vetoes, and releases only knockout-created crawls on recovery. GSit is optional for the rest of RPCharacters; without it, knockouts retain freeze and blindness only.

While downed, a player can only be finished by another player in lethal mode, a mob, `/kill`, the void or the world border: falls, drowning, fire and other damage with no attacker leave them at half a heart, and the fall distance built up by the freeze is cleared when they get up. Knockouts never apply to players in a started SimpleFactions battle, so the battle records the death and routes the respawn.

## PvP strikes

After `/pvp start`, the fight lasts 15 minutes unless the player who started it runs `/pvp end`. When it ends, players who have not died see a title that a new RP interaction is needed. Whoever kills or knocks someone out chooses to spare them or give a strike; the third strike kills the character, though a killer can wound or maim instead of killing.

The same player must wait 24 hours by default before striking a character again (`strikes.same-target-cooldown-hours` in `pvp.yml`; 0 disables the wait), so at that default they cannot land all three strikes in a day. Lockpicking, robbing, pickpocketing and looting locked graves start a timed evil RP session, during which any strike kills and a death leaves an unlocked grave.

## Codex rarity

`%rpcharacters_codex_percent_<category>:<discovery>%` is the nearest whole percent of Codex journals that have unlocked that entry. `%rpcharacters_codex_holders_<category>:<discovery>%` is the count. [TFMC Codex](../../Codex/overview.md) keeps a journal per character, so these count characters; with upstream Codex they count accounts. An unknown category or entry is blank. The figure refreshes about once a minute from Codex's saved files, using live Codex data for characters being played.

## Armour takes time

Putting armour on takes a while (by default 1 second for a helmet, 20 for a chestplate, 12 for leggings and 8 for boots). Pieces go on one at a time and the player is slowed until they're done. Taking or dealing damage, sprinting, dying or logging out stops it.

`/pvp start` takes off any chestplate, leggings or boots that someone in range put on in the last 3 minutes, and nobody in the fight can put armour on until it ends unless they die. Once recent armour is off, it notes who is still in a chestplate, leggings and boots: they keep their helmet and can take it off and put it back on for the rest of the fight. Anyone else also loses any helmet, mask or head they put on in the last 3 minutes, and can't put one on until the fight ends. This is decided when the fight is called and doesn't change during it. The times are set under `armour` in `pvp.yml`. Masks, heads and elytras go on at once.

## Source references

- [Character commands](https://github.com/TF-Minecraft/RPCharacters/blob/main/src/main/java/net/tfminecraft/rpcharacters/command/CharCommand.java)
- [Class selection and paid changes](https://github.com/TF-Minecraft/RPCharacters/blob/main/src/main/resources/config.yml) and [creation stages](https://github.com/TF-Minecraft/RPCharacters/blob/main/src/main/resources/stages.yml)
- [PvP and armour configuration](https://github.com/TF-Minecraft/RPCharacters/blob/main/src/main/resources/pvp.yml)
- [Focus configuration](https://github.com/TF-Minecraft/RPCharacters/blob/main/src/main/resources/focus.yml)
- [Codex population service](https://github.com/TF-Minecraft/RPCharacters/blob/main/src/main/java/net/tfminecraft/rpcharacters/placeholder/CodexPopulationService.java)

Realm OOC chat follows the active character's top-overlord realm. Online accounts
receive it only while playing a character in that realm. It waits for
SimpleFactions readiness; another character on the account grants no access.
