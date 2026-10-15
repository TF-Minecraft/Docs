# Character selection and separate bodies

[RPCharacters](../README.md) · [Shared identity](character-identity.md)

`character-bodies.enabled` enables selection at login. It defaults to `false` and
requires a server restart. With it disabled, the existing account progression
and character activation flow remains in use.

## Playing a character

Players enter a private selection world with no ready character session. A Paper
dialog focuses one living character at a time. Its card shows a skin portrait,
name, race, class, age, guild and when it was last played. Character tabs and
arrows change the preview; **Play** enters the selected character, and its
tooltip lists the playtime, pouch and bank, plus the birthday where recorded.
All living characters stay visible in compact rows of up to three names; characters
with the same name remain separate selections by ID. Changing the preview does
not shift the rows or hide other characters.
**New character** appears beside the character-name tabs. Selecting it shows a
welcome page with one **Create character** button, which starts creation when
slots and the switch cooldown allow it; its tooltip shows the slots used.
Existing-character cards have one **Play** button. Arrows include the new-character
tab, and incoming portrait loads do not replace its welcome page.
The **Memorials** link opens the records of dead and
missing characters. Pouch and bank come from the character's own DenarEconomy
ledger and the guild from SimpleFactions 4.0.0. The guild is hidden when the
character has none or factions are unavailable.

Portraits load asynchronously through ProvinceSystem's authenticated, read-only
`GET /characters/plugin/wardrobe/{player_uuid}/{character_id}/worn` route. It
returns `character_id`, `value` and `signature`; the latter two are null when
there is no signed worn skin. It checks ownership and reads the effective slot
without reconciling wardrobe limits, acknowledging changes or applying skins.
RPCharacters downloads the signed texture's image from `textures.minecraft.net`.
An unavailable wardrobe preview falls back to the account skin; if no image can
be loaded, the dialog shows a neutral figure. Everyone in selection wears the
default Steve skin, a Mojang-signed copy built into RPCharacters. It goes on as
the player joins, before Paper sends the player list, so they arrive as Steve
without a skin refresh during the resource-pack prompt. LibsDisguises re-reads a
cached player's skin 20 ticks after they join, which would now save Steve as
their disguise skin. Servers with selection enabled set `UpdateGameProfiles:
false` in `plugins/LibsDisguises/configs/libsdisguises.yml`. Skins already in its cache
stay as they are. Helmet, mask and
wardrobe changes do not replace it there. Portraits still
fall back to the account skin worn before it. Play puts the cached wardrobe or
account skin back at once, then refreshes the wardrobe from ProvinceSystem. A
player whose account skin cannot be read keeps it in selection. Previews never activate a character,
apply an outfit or restore their body. Old clicks and late portrait responses
cannot reopen a selector after playing, starting creation or reconnecting.

Play restores the chosen character's progression and body before publishing its
ready session. Dismissing the dialog does not admit the player into gameplay;
`/rpcharacter menu` reopens it. Players can use character creation and Discord
linking while selecting. Other commands, movement, damage, item transfers and
ordinary chat remain blocked. Players in selection are hidden from each other
and from players in the game worlds. Permanent-death respawns are hidden before
entering selection, while the outgoing body is saved after respawn.

On login, Paper first restores any saved vehicle in its original world. The
player then dismounts into selection; boats, mounts, other passengers and cargo
stay behind. Living players enter the selection world before the pack request.
With `character-bodies.require-resource-pack: true`, a **Loading TFMC** dialog holds
them there until the pack loads, before progression preparation and the selector.
Pending death/respawn recovery also waits for the pack before continuing.
It requires TFMCCore's `resource-pack.require-on-join: true`; both settings default
to `false` and require a restart. Core confirms every required pack part, or its
single-pack fallback, before selection opens. A missing provider, partial load,
failed load or old connection's response cannot admit the player. Play and New
character also recheck readiness.

The loading screen offers Leave. A failed request offers Retry and Leave; Retry
starts a fresh Core request without bypassing loading. A missing provider or a
wait exceeding 400 seconds offers Leave so the player can reconnect. The player
remains hidden and protected throughout, and logging out retains the recovered
body. The loading dialog uses vanilla text, so it does not need the pack it is
waiting for. See [required join packs](../../TFMCCore/resource-pack.md#required-join-packs)
for delivery settings and removing duplicate automatic requests.

With ProtocolLib on Minecraft 1.21.10, `character-bodies.hide-hud: true` (the
default) hides the survival HUD, custom action bar and loading titles throughout
loading, selection and the native creation wizard. The client displays spectator
HUD rules while its server game mode, player-list mode and actual abilities stay
unchanged. Mode and authoritative abilities travel together in a packet bundle;
Play restores the normal display before publishing the ready session. Other
Minecraft versions or an unavailable ProtocolLib keep the existing interface and
log the missing adapter. Changing the setting requires a restart.

Flight requests caused by the temporary client display are ignored while hidden.
Restoration uses a client ping acknowledgement before allowing flight requests
again, so a late spectator flight request cannot change the server's saved flags.

Plugin system messages wait until Play, including join messages and chat
sent before a delayed room teleport succeeds. Return countdown and cancellation
feedback stays live until the switch commits. The queue belongs to one connection,
retains up to 100 messages and 131,072 JSON characters, and preserves formatting,
clicks and hover text. Overflow omits the oldest messages, or a message larger than
the entire budget, and reports the omitted count when releasing the queue. Busy
queues drain in bounded batches; gameplay chat follows retained messages. Quit
discards undelivered chat, and plugin shutdown restores the display and releases
retained messages; arrivals beyond the shutdown drain budget report an omitted
count. Signed player chat and disguised chat from `/say` or `/me` remain untouched.

Selection and creation errors appear in their dialogs. When Discord linking is
required, **Link Discord to play** opens the readable chat-based linking flow;
new messages remain visible there, while previously queued ordinary messages
still wait for Play. `/rpcharacter menu` returns to selection. Already-received
chat fades normally when returning from gameplay. Minecraft's resource-pack
consent screen and progress notification remain visible; this needs no pack
changes or client mod.

If another plugin blocks the selection-room teleport, the
player remains hidden and unable to interact in the original world. The loading
dialog still opens before Minecraft's pack prompt, and room entry retries after
the pack loads. Character selection opens only after room entry succeeds.
Once the pack is ready, **Entering character selection** explains the delayed
room entry, retries automatically and offers **Leave**.

The destination teleport must succeed before progression or inventory is restored.
If another plugin blocks it, selection remains available without an activation
lease or a ready session. Wait for resource packs to finish loading before retrying;
ItemsAdder can block teleports while a pack is still loading.
Missing character class definitions also leave selection available so another
character can be chosen. Failures after progression restoration starts retain
their activation evidence for manual recovery; reward commands may already have
run, so blindly repeating that restoration is unsafe.

While playing, `/rpcharacter menu` returns the player to selection without
disconnecting. They must stand still for `character-bodies.return-seconds`
(default 5). Turning on the spot is fine; moving or teleporting more than a
quarter of a block, mounting, taking damage or any refusal below cancels it.
Starting character creation while playing does the same. It is refused while
dead or respawning, mounted, falling, creating or editing a character,
duelling, in a `/pvp` fight, knocked out, in a started SimpleFactions battle or
held by an evil-roleplay session. Other plugins can refuse it by
cancelling `CharacterSelectionRequestEvent`, which fires at the start and on each
second of the countdown; set a reason with `deny`. Use it where a logout carries
a penalty.

Once the countdown ends, the session ends with reason `SWITCH`, so session
listeners clean up while the outgoing body is still in the world. Open duel
challenges, an expired `/pvp` start mark and armour fastening are cancelled, and
a temporary alias ends. The
body and progression are then saved, and the player enters selection as at
login. A failed save disconnects the player with the body kept live for recovery.
An unfinished in-game creation draft is cancelled on logout.

Resuming the last character does not consume or require the
switch cooldown. Choosing another living character uses the configured
permission-group switch cooldown and records the switch. A dead previous
character does not prevent choosing a survivor. Permanent death ends the session
and returns the player to selection after the dying body is saved; it does not
automatically activate another character.

## Stored state

Each body has its own inventory, armor, offhand, ender chest, selected hotbar slot,
location, respawn and last-death locations, vanilla health and absorption, hunger,
saturation, exhaustion, experience, air, fire/freeze state, fall distance, potion
effects and explicitly configured persistent-data keys. Paper item bytes retain
item components and nested item data. Accessories implemented as vanilla slots,
including the TFMC ring and artifact slots, travel with that inventory. Separate
custom inventories owned by other plugins require their own integration.
Forced respawn points retain their forced flag. Empty vanilla accessory slots
are refreshed through MMOInventory without replacing equipped accessories.
Game mode, flight settings and shoulder entities remain account-level state.
Permanently dead characters cannot reopen their stored ender chests through
selection; those contents remain in the retained body record.

Each character also has its own MMOCore progression, class level and experience,
skills and bindings, profession experience, skill/attribute/profession point
pools, and current mana, stamina and stellium. The MMOCore account file is a cache
of the last applied character. Character progression files are authoritative.
Changes to experience queue a guarded checkpoint; quit and permanent death save
synchronously, with an additional periodic checkpoint. A sudden process or host
failure can lose changes since the latest completed progression checkpoint.

The original account progression fields remain unchanged. On an account's first
migration, an immutable baseline records the existing character roster and
legacy progression. Those characters each receive one independent copy. Later
characters start with fresh progression. Only the reviewed body heir receives
the legacy items; other characters receive empty bodies at their saved locations
or the configured spawn. Accounts with no characters have their legacy body
retained in quarantine rather than assigned to a future character.
The initial progression roster is captured at join. A web-created character
arriving while player data loads receives fresh defaults after the baseline is
saved, rather than inheriting the account's previous progression.

New graves record the dying character as well as the account. Locked-grave
ownership and insurance recovery require the matching ready character, unless
staff or public recovery rules allow access. Legacy graves use the account's
reviewed migration heir. Holograms identify the grave's character rather than
whichever character the account is playing now.

Account cosmetics, ranks, Discord linkage, bans and existing account-level kit
limits remain account-level. Profession permissions use transient LuckPerms nodes
when bodies are enabled. Removing them also retires matching legacy persistent
profession nodes in the configured server context.

## Configuration and cutover

```yaml
character-bodies:
  enabled: false
  heirs-sha256: ''
  selection-world: character_selection
  return-seconds: 5
  # Optional; otherwise the first loaded world is used.
  spawn-world: world
  persistent-keys: []
```

`selection-world` must be a separate world with a lowercase name containing only
letters, digits, underscores and hyphens. Existing unrelated worlds are refused.
The plugin creates a void world with a protected platform enclosed in black
concrete, so the selection dialog has a dark backdrop whatever the client's sky,
brightness or shaders. Selecting players are invisible, so third person shows
no body; the character's own effects replace this on **Play**. Spectator mode is
not used because it ignores the inventory clicks that creation menus need. The
dialog is the selection interface; this does not create mannequin displays.

All selecting players share that platform. The plugin sets `maxEntityCramming`
to `0` in its owned selection world. To disable server-side entity pushing as
well, set the following in `<selection-world>/paper-world.yml` and restart the
server, preserving the file's existing settings and `_version`:

```yaml
collisions:
  max-entity-collisions: 0
```

Apply this override only to the selection world. Both settings are needed to
skip Paper's entity-pushing and overcrowding checks; the gamerule alone does
not disable pushing. Mutual player hiding prevents selecting players from
receiving each other's entities. No scoreboard teams or per-character collision
flags are changed. A shared platform does not establish a concurrent-join limit;
validate client behavior and server load separately before increasing capacity.

`persistent-keys` lists exact player persistent-data keys to isolate by character.
Account-level keys remain outside this list. Keys in the plugin's reserved body
namespace are refused. Configure only keys whose owning plugin supports loading
and saving them with the character body.

Place a reviewed UTF-8 manifest at
`plugins/RPCharacters/character-body-heirs.yml`:

```yaml
version: 1
heirs:
  11111111-1111-4111-8111-111111111111: 22222222-2222-4222-8222-222222222222
```

The mapping is account UUID to character UUID. Pin the SHA-256 of the exact file
bytes in `heirs-sha256`.

Generate the manifest from the server's stopped data with
`tools/body_heirs.py` in RPCharacters (Python 3.10 or later, standard library only):

```sh
python3 tools/body_heirs.py plugins/RPCharacters/data out/ --overrides reviewed.yml
```

It writes `character-body-heirs.yml`, `character-body-heirs.sha256` and
`character-body-heirs-review.md`. Each account's heir is its active living
character, else its most-played living character, else its most-played
character. `--overrides` takes a file in the manifest format whose entries
replace the proposal, so staff decisions survive regeneration. The report lists
accounts that need a decision, heirs that are not the most-played character,
accounts with no characters, and records that block the manifest: unreadable
files, invalid IDs, duplicate character IDs and overrides naming a character
from another account. The tool exits with status 1 while any record blocks it. An account with existing characters and no valid reviewed
heir is blocked, except a first-ever Minecraft login with no inventory or ender
chest possessions. That new account's website-created characters start fresh;
the original body is retained in quarantine. Only exact MMOInventory accessory
slot placeholders count as empty slots, never equipped accessories or ordinary
diamond hoes. Previously played accounts still require a reviewed heir even if
their inventories are empty. Do not edit an already migrated account's heir to
transfer its possessions or grave privileges.

For cutover:

1. Stop Minecraft cleanly and back up vanilla player data, RPCharacters data,
   MMOCore data, graves, configuration and the reviewed manifest together.
2. Generate the manifest from the stopped server's data with the reviewed
   overrides, and resolve every blocked record and every account the report
   lists for a decision. Keep dead characters as records. Complete any
   pending vanilla death-screen respawn before this first cutover: an untagged,
   dead vanilla player is refused without changing its data. This is separate
   from the character's permanent-death status.
3. Set the correct profession permission context for this server. Dev must use
   `server=dev` because Dev and Main share LuckPerms storage. Configure the intended
   switch cooldowns in `permission-groups.yml`; the target migration policy is
   4/3/2/1 days by rank, with both top tiers using one day.
4. Install the intended build, manifest and checksum, enable the feature, and
   restart. Never hot-reload a body server. Enabling with players already online
   blocks entry and requires a restart.
5. Validate synthetic accounts and the recovery procedure before general use.
   A bad body configuration keeps logins blocked until it is repaired and the
   server is restarted.

## Persistence and recovery

State lives below `plugins/RPCharacters/data/`:

| Path | Contents |
| --- | --- |
| `body-migrations/<account>.yml` | Immutable legacy body, initial roster, heir and migration completion state. |
| `bodies/` | Versioned, checksummed character bodies and recovery copies. |
| `body-leases/<account>.json` | Durable activation claim with character, base revision, pending normal-respawn intent and completed vanilla respawn. |
| `progress/<account>/baseline.yml` | Immutable legacy progression baseline. |
| `progress/<account>/characters/<character>.yml` | Character progression and revision. |

Body and progression writes use atomic replacement. Previous files are recovery
evidence, not an automatic fallback: a corrupt or missing committed file blocks
activation rather than silently rolling back possessions or progression.

The vanilla player file carries a body tag naming its account, character and
stored base revision. Before restoring a body, the plugin creates and flushes a
matching activation lease. While playing, vanilla player data is the live item
copy; stored body files are used while a character is stowed. The plugin does not
periodically copy live items into a second playable body.

On a normal logout, session-end listeners run, the character is saved, its live
inventory is cleared, and the player file is saved with a selection-room tag.
The lease is removed after the body commit and selection-room player save.
On reconnect after a crash, a matching live tag, lease and body revision allow
recovery from the vanilla file. If a newer body was already committed, the stale
live copy is quarantined. A room or untagged player file with an outstanding
lease, a live tag without its lease, or mismatched evidence blocks login for
manual recovery. This also prevents replaying a body when Paper returns from a
player save without persisting it. Items returned by another plugin after stowing
are retained in quarantine and are not automatically merged into another body.

Disconnecting on the ordinary death screen leaves the live vanilla body and its
lease intact. Rejoining completes the normal respawn before opening selection;
the saved body retains its actual respawn location, items and experience and
restores full health after character equipment and attributes are applied.
Recovery waits for Paper to finish its actual respawn and teleport, even if a
progression plugin restores health first. The lease durably records both respawn
intent and completion. An interrupted respawn whose saved vanilla state disagrees
with that evidence blocks login for manual recovery. A living character body is
never recovered from the selection room.
Permanently dead character bodies remain dead; respawning the vanilla player
only returns them to selection. Unassigned returns from that respawn are
quarantined.

If recovery fails, keep the affected player offline. Stop Minecraft before
repairing files, retain the failed files and logs, and compare the player tag,
activation lease, body revisions and migration baseline. A room tag and an empty
inventory alone do not prove recovery is safe: another plugin could have moved
items or executed reward commands during the interrupted activation.

For a proven failed activation of an empty body, a reviewed recovery can retire
the exact matching lease after checking all of the following:

- Logs show the character never entered gameplay or published a ready session.
- The vanilla file is alive and tagged ROOM in the selection world, with no
  inventory, cursor, crafting or ender chest possessions; exact accessory GUI
  placeholders are the only permitted inventory contents.
- Lease owner, character and revision match the checksummed stored body, with
  neither pending nor completed respawn recorded. The target body contains no
  gameplay items, and the migration and progression records are intact.
- Class and level reward effects have been checked independently. If commands
  may already have granted items, money or other state, reconcile those effects
  before allowing restoration to repeat; an empty target body is insufficient.
- A coordinated backup retains every original file and log. Recheck their hashes
  while stopped, move the lease into a preserved recovery directory, and leave
  body, progression and vanilla files unchanged. Normal ROOM recovery quarantines
  leftover placeholders before reopening selection.

Other ambiguous cases remain blocked for investigation. Do not delete tags or
leases merely to bypass a refusal, reset revisions, remove baselines, or activate
both a quarantined copy and its committed body.

Rollback restores the entire coordinated pre-cutover backup while Minecraft is
stopped. Simply disabling the feature after characters have played would expose
a stowed account inventory and legacy progression, so it is not a data rollback.
Graves, world containers and other plugins are not part of one cross-plugin
transaction; a whole-server crash still needs their own recovery procedures.

## Verification

Run `mvn clean verify` using Java 21 and the pinned dependencies. The existing
100% line-coverage gate remains enforced. Unit tests cover body serialization,
strict file validation, revision conflicts, partial writes, migration retries,
progression cloning and isolation, selector actions, ownership and stale
callbacks.

A Paper integration run should verify real item components and accessory slots,
A → logout → B → logout → A isolation, cooldown and same-character resume, death
and grave recovery, creation, selection during resource-pack loading and retry
after loading, server restart, live-tag crash recovery, saved mounts with cargo,
first-login web characters, roster changes during loading, failed storage and
corrupt-file refusal. Mocked Paper or MMOCore boundaries alone do not prove those
runtime behaviors.
