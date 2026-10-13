# Shared character identity

[RPCharacters](../README.md) · [TLibs API](../../TLibs/character-identity.md)

RPCharacters provides TLibs' `CharacterIdentity` service through Bukkit's
`ServicesManager`. The build pins TLibs 2.5.0; install that release or a compatible
newer one before RPCharacters. Consumers use the `Characters` facade rather than
reading RPCharacters files or waiting a fixed number of ticks after login.

## Directory

Startup reads `plugins/RPCharacters/data/playerdata/` and
`plugins/RPCharacters/data/characterdata/` before registering the service. The
in-memory directory includes inactive, dead, missing and hidden characters, with
canonical names rather than aliases. Queries do not read disk or instantiate
offline player data. Successful saves update it; a save off the main thread
queues its update for the main thread. Each query overlays unsaved changes from
the loaded account it reads, or for `info(characterId)` from every loaded account
holding that ID. Failed creation rollback removes the corresponding entry.

Entries directly in `playerdata/` or `characterdata/` whose names are not account
UUIDs, such as `x.json.bak` or `.DS_Store`, belong to no account. Startup logs a
warning naming each one and skips it. Inside an account's character folder, every
file other than an atomic-save staging file must be a character record.

Unreadable records, invalid character filenames or IDs, and conflicting character
IDs make the affected accounts unavailable. A duplicate ID across accounts makes
both unavailable. The log identifies the records that need repair.
`characters(ownerId)` returns an empty optional for an unavailable account, but a
present empty list for an account with no characters. If the data folders
themselves cannot be listed, plugin startup fails before the service registers.
Repair files with the server stopped and restart to rebuild the directory;
ordinary saves do not clear a quarantine.

Login also compares loaded character IDs against the directory. An account whose
records cannot be loaded completely is disconnected before admission or saves.

`CharacterInfo.name` is the real, plain character name. `displayName(player)` uses
the current mask and temporary alias rules.

`findByName(name)` first overlays every loaded account, then scans the in-memory
directory, so it reads no files. It returns every `ALIVE` character whose real name
equals the trimmed `name`, ignoring case. Dead and missing characters, aliases,
masks and temporary aliases never match, and unavailable accounts are skipped. The playtime field is the existing
`online-playtime-seconds` counter, with no visibility filtering.

## Sessions and readiness

With [separate bodies](character-bodies.md) enabled, login waits in selection
without a ready session. Play restores the chosen body and progression before
publishing a session; permanent death returns to selection. The automatic
activation and replacement behavior below applies while bodies are disabled.

`CharacterTransitions` owns join, switch, quit, permanent death and shutdown.
Each activation receives a fresh session token, including reconnecting or
switching Alice → Bob → Alice. Ended tokens never become current again.

The start event follows successful MMOCore join setup, or successful class,
attribute and profession activation during a switch. Activation is saved before
the session is published. The player is disconnected instead of getting a ready
session when MMOCore setup times out, MMOCore attribute removals are still
pending after the join retries, the class cannot be applied, the outgoing
character fails to save during a switch, or the activation save fails. Selection
during pending join changes the selected character without applying MMOCore
state early.

In-game creation and website creates add the new character to the account before
activating it; a website create saves it first. If that activation fails, the
player is disconnected and their quit saves the account, but the creation still
completes: kit eligibility is kept, the creator session closes and the website
receives a success acknowledgement.

An end event invalidates the outgoing token before dispatch. Listeners run while
the outgoing character remains loaded, so they can flush their state before
RPCharacters saves or unloads it. Switches, quits, active-character deaths and
plugin shutdown emit the corresponding reason. Killing an inactive character
leaves the active session intact. Same-account nested transitions are rejected;
terminal quit cleanup remains possible when a transition disconnects the player.

Focus loads and flushes on the shared session events. The existing RPCharacters
`CharacterActivatedEvent` remains available, emitted after the shared start event
while the session is still current. Creation and other existing events remain.

## Saved timestamps and deaths

Character JSON adds optional fields without changing existing character UUIDs:

| Field | Meaning |
| --- | --- |
| `last-played-at-ms` | UTC epoch milliseconds at the latest successful session start. |
| `death-id` | UUID of the latest committed permanent death. |
| `died-at-ms` | UTC epoch milliseconds for that death. |

`lastPlayed` returns the character with the latest `last-played-at-ms`.
Characters saved before session timestamps existed have none, so an account
without any timestamp falls back to the character whose legacy `active` field is
true. Any timestamp beats that flag, and an account with neither returns empty.
The fallback reads existing files without rewriting them. Dead characters can
still be the most recently played. Revival retains the previous death record; a
subsequent death generates a new ID.

The RPCharacters `CharacterPermakillEvent` remains cancellable and fires before
mutation. The shared `CharacterDeathEvent` fires only after a durable (fsynced)
character file save records `DEAD`, the inactive flag and death metadata, and
after the death's [estate record](estates-and-wills.md) is written. Save failure
restores the in-memory status, disconnects the player and emits no shared death
event. The event includes the killer's account and current character when known.

A session end with reason `DEATH` fires before that save, so it does not mean the
death was committed: `CharacterDeathEvent` is the authority. If the save fails,
the character stays alive and the player is disconnected. A player who
disconnects while the end event is dispatched also keeps the character alive.
Once the death is saved, a replacement character that cannot be activated
disconnects the player, and the death's own follow-up, such as the roster push
and the caller's result, still runs.

`Characters.deathId(characterId)` returns the latest saved death ID, including
for offline characters. Revival retains it; another death replaces it. A revive
saves the character as alive durably, then fires the shared
`CharacterRevivedEvent` with the previous death ID; a failed save fires nothing. A legacy
DEAD record without a death ID uses a deterministic UUID derived from
`rpcharacters:legacy-death:<characterId>`, stable across restarts without
rewriting the original record. Quarantined or unknown records return empty.
Consumers recover their incomplete journals first, then reconcile DEAD records;
they must not replay an old death just because a living character retains its ID.

Event delivery is not durable. A crash after saving but before dispatch can lose
the event; consumers must use `deathId` for idempotency. Account saves still write
individual character files and then the account file, rather than one transaction
covering the whole account.

## Verification

Run `mvn clean verify` with Java 21 and pinned dependencies installed. The unit
suite checks directory corruption and duplicates, skipped stray entries, the
legacy `lastPlayed` fallback, name lookups, immutable snapshots, live updates, delayed
readiness, reconnects, repeated-character switches, event order, quit and
shutdown cleanup, cancelled and inactive deaths, distinct death IDs after
revival, failed saves, and activation failures after a committed death or
creation. It enforces the repository's 100% line coverage gate.
Mocked MMOCore boundaries do not replace a full Paper integration run with the
pinned runtime plugins.
