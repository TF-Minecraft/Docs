# Codex

[Project index](README.md)

## Journals per character

Each character has its own journal in `plugins/Codex/characters/<character>.yml`. Codex opens it when the character's session starts and saves it when the session ends, whether by switching, quitting, death or shutdown. It also saves open journals every `player_data_save` seconds. If a journal cannot be written when its session ends, Codex logs an error, keeps it in memory and retries with every save; the character gets it back if it returns first. A new character starts with an empty journal, so it discovers places and lore again and earns their rewards again, such as the Player EXP for a point of interest.

Between characters, for example in the selection room, a player has no journal. Discoveries and rewards wait until a character is in play, and `/codex` answers `noCharacterInPlay` ("Choose a character to open the Codex.") instead of opening.

## Out-of-character reference

An entry the account found before journals were per character, or that any of its characters has found since (alive or dead), stays unlocked in `/codex`. Its click actions, such as the lore sub-pages on Main, still run, unless the entry sets `click_actions_cooldown`: that cooldown is kept on the character's own entry, so an entry with one runs its click actions only for a character that found it itself. Its hover text then names the living characters who can use it in character, the played character first: "Aldric and Mira can use this in character." If no living character found it itself, the line reads "No character can use this in character." When the played character has not found the entry itself, a further line says "Aldric knows this only out of character." These three lines are `knownInCharacterBy`, `knownInCharacterByNobody` and `knownOutOfCharacterOnly` in `messages.yml`, and Codex adds them to existing files along with `noCharacterInPlay`.

Codex reads the other journals when a session starts, since they cannot change while the account plays someone else, and again after `/codex resetplayer *`. Category progress, completion rewards and placeholders count only the played character's own discoveries.

A journal file records `owner` (the account UUID), `name` (the account name when last saved) and, for each category, whether it is completed and its discoveries as `id;date;millis`.

## Discoveries from before characters

Upstream Codex kept one journal per account in `plugins/Codex/players/<account>.yml`. As a one-off, at the start of an account's first character session after the change, Codex copies that journal into the journal of the account's most-played living character (else its most-played character), using RPCharacters' playtime at that moment. The choice is pinned in `plugins/TLibs/legacy-recipients/<account>.txt`, which ConditionalEvents reads too, so both give the account's old data to the same character and a retry never picks another. That character knows those entries in character; every other character starts with an empty journal and earns each discovery and its rewards again. If the most-played character already had a journal, the two merge: it keeps its own entries, and a category counts as completed if either side completed it.

The account file stays where it is and feeds the out-of-character reference above. It gains `seeded-to: <character>` so the copy never repeats. A failed copy is logged as `Could not copy the old Codex of account …` and retried at the account's next session; a successful one as `Copied <n> old Codex discoveries of account <account> to its most-played character <character>`. ConditionalEvents gives the account's old per-character event data to the same character.

## Staff commands

`/codex resetplayer <player> [category] [discovery]` resets the journal of the character the player is playing now, and the player must be online. `/codex resetplayer * …` resets every character's journal file, every open journal and every account file in `players/`.

## Placeholders

RPCharacters' `codex_percent_` and `codex_holders_` placeholders count character journals; see [character controls](../RPCharacters/docs/character-controls.md#codex-rarity).
