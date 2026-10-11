# Shared character identity

[RPCharacters](../README.md) · [TLibs API](../../TLibs/character-identity.md)

RPCharacters provides TLibs' `CharacterIdentity` service through Bukkit's
`ServicesManager`. The build pins TLibs 2.3.0; install that release or a compatible
newer one before RPCharacters. Consumers use the `Characters` facade rather than
reading RPCharacters files or waiting a fixed number of ticks after login.

## Directory

Startup reads `plugins/RPCharacters/data/playerdata/` and
`plugins/RPCharacters/data/characterdata/` before registering the service. The
in-memory directory includes inactive, dead, missing and hidden characters, with
canonical names rather than aliases. Queries do not read disk or instantiate
offline player data. Successful saves update it, and queries overlay unsaved
changes from loaded accounts. Failed creation rollback removes the corresponding
entry.

Unreadable records, invalid UUIDs, and conflicting character IDs make the affected
accounts unavailable. A duplicate ID across accounts makes both unavailable. The
log identifies the records that need repair. `characters(ownerId)` returns an
empty optional for an unavailable account, but a present empty list for an account
with no characters. If the directory itself cannot be enumerated, plugin startup
fails before the service registers. Repair files with the server stopped and
restart to rebuild the directory; ordinary saves do not clear a quarantine.

Login also compares loaded character IDs against the directory. An account whose
records cannot be loaded completely is disconnected before admission or saves.

`CharacterInfo.name` is the real, plain character name. `displayName(player)` uses
the current mask and temporary alias rules. The playtime field is the existing
`online-playtime-seconds` counter, with no visibility filtering.

## Sessions and readiness

`CharacterTransitions` owns join, switch, quit, permanent death and shutdown.
Each activation receives a fresh session token, including reconnecting or
switching Alice → Bob → Alice. Ended tokens never become current again.

The start event follows successful MMOCore join setup, or successful class,
attribute and profession activation during a switch. Activation is saved before
the session is published. Setup timeout, class-application failure or activation
save failure disconnects the player instead of announcing a ready session.
Selection during pending join changes the selected character without applying
MMOCore state early.

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

Legacy characters without a session timestamp do not supply a fabricated
`lastPlayed` result. Dead characters can still be the most recently played.
Revival retains the previous death record; a subsequent death generates a new ID.

The RPCharacters `CharacterPermakillEvent` remains cancellable and fires before
mutation. The shared `CharacterDeathEvent` fires only after an atomic character
file save records `DEAD`, the inactive flag and death metadata. Save failure
restores the in-memory status, disconnects the player and emits no shared death
event. The event includes the killer's account and current character when known.

Event delivery is not durable. A crash after saving but before dispatch can lose
the event; consumers must use `deathId` for idempotency. Account saves still write
individual character files and then the account file, rather than one transaction
covering the whole account.

## Verification

Run `mvn clean verify` with Java 21 and pinned dependencies installed. The unit
suite checks directory corruption and duplicates, immutable snapshots, live
updates, delayed readiness, reconnects, repeated-character switches, event order,
quit and shutdown cleanup, cancelled and inactive deaths, distinct death IDs after
revival, and failed saves. It enforces the repository's 100% line coverage gate.
Mocked MMOCore boundaries do not replace a full Paper integration run with the
pinned runtime plugins.
