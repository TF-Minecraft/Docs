# Codex

[Project index](README.md)

## Journals per character

Each character has its own journal in `plugins/Codex/characters/<character>.yml`. Codex opens it when the character's session starts and saves it when the session ends, whether by switching, quitting, death or shutdown. It also saves open journals every `player_data_save` seconds. A new character starts with an empty journal, so it discovers places and lore again and earns their rewards again, such as the Player EXP for a point of interest.

Between characters, for example in the selection room, a player has no journal. Discoveries, rewards and `/codex` entries wait until a character is in play.

A journal file records `owner` (the account UUID), `name` (the account name when last saved) and, for each category, whether it is completed and its discoveries as `id;date;millis`.

## Discoveries from before characters

Upstream Codex kept one journal per account in `plugins/Codex/players/<account>.yml`. Each of these goes to the character RPCharacters chose as the account's heir at the bodies cutover, the same character that received its money and body. Accounts missing from that review give theirs to their most-played living character, or else their most-played character. Their other characters start empty.

Codex moves every account file once RPCharacters reports its heirs, a few seconds after start-up, and again at the start of each session. If the heir already has a journal, the two merge: the heir keeps its own entries and gains the rest, and a category counts as completed if either side completed it. The moved file goes to `plugins/Codex/players-migrated/`. An account with no character keeps its file in `players/` until it has one. The server log records each move as `Moved <n> Codex discoveries of account <account> to character <character>`.

## Staff commands

`/codex reset <player> [category] [discovery]` resets the journal of the character the player is playing now, and the player must be online. `/codex reset * …` resets every character's journal file and every open journal.

## Placeholders

RPCharacters' `codex_percent_` and `codex_holders_` placeholders count character journals; see [character controls](../RPCharacters/docs/character-controls.md#codex-rarity).
