# Character selection and separate bodies

[RPCharacters](../README.md) · [Shared identity](character-identity.md)

`character-bodies.enabled` enables selection at login. It defaults to `false` and
requires a server restart. With it disabled, the existing account progression
and character activation flow remains in use.

## Playing a character

Players enter a private selection world with no ready character session. A Paper
dialog lists living characters with their race, class, age, last location and
playtime. Dead and missing characters remain visible as records. Guild membership
and pouch/bank balances are labelled as shared by all characters; this feature
does not migrate money or factions.

Play restores the chosen character's progression and body before publishing its
ready session. Dismissing the dialog does not admit the player into gameplay;
`/rpcharacter select` reopens it. Players can use character creation and Discord
linking while selecting. Other commands, movement, damage, item transfers and
ordinary chat remain blocked. Players in selection are hidden from each other
and from players in the game worlds.

Starting character creation while playing also requires reconnecting into
selection. An unfinished in-game creation draft is cancelled on logout; completed
characters remain saved and can be selected after reconnecting.

While playing, `/rpcharacter select` disconnects the player. Reconnecting opens
selection and follows the existing logout and combat rules. There is no live
inventory swap. Resuming the last character does not consume or require the
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
  # Optional; otherwise the first loaded world is used.
  spawn-world: world
  persistent-keys: []
```

`selection-world` must be a separate world with a lowercase name containing only
letters, digits, underscores and hyphens. Existing unrelated worlds are refused.
The plugin creates a void world and a protected quartz platform. The dialog is
the selection interface; this does not create mannequin displays.

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
bytes in `heirs-sha256`. An account with existing characters and no valid reviewed
heir is blocked. Do not edit an already migrated account's heir to transfer its
possessions or grave privileges.

For cutover:

1. Stop Minecraft cleanly and back up vanilla player data, RPCharacters data,
   MMOCore data, graves, configuration and the reviewed manifest together.
2. Verify the manifest against the current roster and resolve duplicate or
   unreadable character records. Keep dead characters as records. Complete any
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
| `body-leases/<account>.json` | Durable activation claim with character, base revision and pending normal-respawn intent. |
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
Durable respawn intent also covers another interruption during this recovery.
Permanently dead character bodies remain dead; respawning the vanilla player
only returns them to selection. Unassigned returns from that respawn are
quarantined.

If recovery fails, keep the affected player offline. Stop Minecraft before
repairing files, retain the failed files and logs, and compare the player tag,
activation lease, body revisions and migration baseline. Do not delete tags or
leases to bypass a refusal, reset revisions, remove baselines, or activate both
a quarantined copy and its committed body.

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
and grave recovery, creation, server restart, live-tag crash recovery, failed
storage and corrupt-file refusal. Mocked Paper or MMOCore boundaries alone do not
prove those runtime behaviors.
