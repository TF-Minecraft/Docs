# Online player list

`/players`, or **Who's online** on the vanilla Quick Actions key (G), opens a
dialog listing online players. Each entry shows the player's face, rank tag and
safe character name, following the same rules as `%rpcharacters_display_safe%`.
Players the viewer cannot see, such as vanished staff, are left out.

Hovering a name shows the account name, rank and ping. Clicking opens a
character sheet: a pixel portrait of the player's current skin beside their
`profile-view.yml` lines, account name, rank and ping. **Back to player list**
or Esc returns to the list.

The sheet uses the normal profile view rules through `CharacterProfileViewEvent`
with the `SHEET` presentation. Viewers need `rpchar.profile`, and the view
cooldown applies. Masks do not hide sheets here: the list is out of character, and
refusing masked players would reveal who is masked. Shift-right-clicking a masked
player in the world is still refused. A hidden active character shows its facade.

## Configuration

`player-list.yml`:

| Key | Purpose |
| --- | --- |
| `permission` | Node to open the list (`rpchar.playerlist`, default true) |
| `title`, `header` | Dialog title and header; `{online}` is the number listed |
| `portrait` | Show the skin portrait on the character sheet |
| `quick-action.enabled`, `quick-action.label` | Put the list on the Quick Actions key |
| `ranks` | LuckPerms groups in priority order, each with its tag |

A player shows the tag of the first listed group they belong to, and the list is
sorted in that order, then by character name. Players in none of the groups are
listed last without a tag. Tags use `&` codes and `#RRGGBB` hex colours.

## Quick Actions key

The G key opens a dialog stored on the client, so it cannot list players
directly. RPCharacters keeps a small data pack, `rpcharacters-player-list`, in
the main world's `datapacks` folder. Its dialog has one button that sends the
`rpcharacters:player_list` custom click back to the server, which opens the
list. Data packs load at startup: after the pack is first written, or after
`quick-action.enabled` changes, restart the server. The plugin logs when a
restart is needed and removes only its own pack when the option is off.

## Skins

Portraits and faces come from each player's signed profile textures, so they
match the skin the player is wearing. Skin images are downloaded from
`textures.minecraft.net` only, off the main thread, and cached. The server needs
outbound HTTPS for portraits; without it the sheet shows the profile lines only.

## Manual checks

- [ ] `/players` lists everyone visible, sorted by rank, with faces and tags
- [ ] Hovering shows the account name, rank and ping
- [ ] Clicking a name opens the sheet; **Back to player list** returns
- [ ] A masked player's sheet opens from the list; shift-right-clicking them in the world is refused
- [ ] A hidden active character shows its facade in the list and on the sheet
- [ ] After a restart, G shows **Who's online** and opens the list
