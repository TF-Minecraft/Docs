# Codex

[Project index](README.md)

## Journals per character

Each character has its own journal in `plugins/Codex/characters/<character>.yml`. Codex opens it when the character's session starts and saves it when the session ends, whether by switching, quitting, death or shutdown. It also saves open journals every `player_data_save` seconds. A new character starts with an empty journal, so it discovers places and lore again and earns their rewards again, such as the Player EXP for a point of interest.

Between characters, for example in the selection room, a player has no journal. Discoveries and rewards wait until a character is in play, and `/codex` answers `noCharacterInPlay` ("Choose a character to open the Codex.") instead of opening.

## Out-of-character reference

An entry any of the account's characters has found, alive or dead, stays unlocked in `/codex`. Its click actions, such as the lore sub-pages on Main, still run, unless the entry sets `click_actions_cooldown`: that cooldown is kept on the character's own entry, so an entry with one runs its click actions only for a character that found it itself. Its hover text then names the living characters who can use it in character, the played character first: "Aldric and Mira can use this in character." If only dead characters found it, the line reads "No living character can use this in character." When the played character has not found the entry itself, a further line says "Aldric knows this only out of character." These three lines are `knownInCharacterBy`, `knownInCharacterByNobody` and `knownOutOfCharacterOnly` in `messages.yml`, and Codex adds them to existing files along with `noCharacterInPlay`.

Codex reads the other characters' journals when a session starts, since they cannot change while the account plays someone else, again after the start-up move of account files, and after `/codex resetplayer *`. Category progress, completion rewards and placeholders count only the played character's own discoveries.

A journal file records `owner` (the account UUID), `name` (the account name when last saved) and, for each category, whether it is completed and its discoveries as `id;date;millis`.

## Discoveries from before characters

Upstream Codex kept one journal per account in `plugins/Codex/players/<account>.yml`. Each of these goes to the character RPCharacters chose as the account's heir at the bodies cutover, the same character that received its money and body. Accounts missing from that review give theirs to their most-played living character, or else their most-played character. Their other characters start empty.

Codex moves every account file once RPCharacters reports its heirs, a few seconds after start-up, and again at the start of each session. RPCharacters reports heirs only when `character-bodies` is enabled; if it has not after 60 seconds, Codex logs a warning and the files wait. A reviewed heir deleted since the review falls through to the most-played rule. If the heir already has a journal, the two merge: the heir keeps its own entries and gains the rest, and a category counts as completed if either side completed it. The moved file goes to `plugins/Codex/players-migrated/`, as `<account>-2.yml` and so on if an earlier copy is already there. An account with no character keeps its file in `players/` until it has one. The server log records each move as `Moved <n> Codex discoveries of account <account> to character <character>`.

## Staff commands

`/codex resetplayer <player> [category] [discovery]` resets the journal of the character the player is playing now, and the player must be online. `/codex resetplayer * …` resets every character's journal file, every open journal and every account file in `players/` that has not moved yet.

## Placeholders

RPCharacters' `codex_percent_` and `codex_holders_` placeholders count character journals; see [character controls](../RPCharacters/docs/character-controls.md#codex-rarity).
