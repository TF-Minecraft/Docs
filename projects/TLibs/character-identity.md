# Character identity API

[TLibs](README.md) · [All projects](../../README.md)

TLibs defines one API for asking which character a player is playing, in
[`net.tfminecraft.tlibs.character`](https://github.com/TF-Minecraft/TLibs/tree/main/src/main/java/net/tfminecraft/tlibs/character).
TLibs only defines it. A character plugin provides it by registering a
`CharacterIdentity` service in Bukkit's `ServicesManager` once its records have
loaded. [RPCharacters](../RPCharacters/docs/character-identity.md) implements the
provider, including saved and online identities, session boundaries and permanent
death records.

Service and `CharacterSessionMap` calls run on the main thread; the facade and map
throw `IllegalStateException` from any other thread. Providers fire the synchronous
events on that thread too. Returned values are immutable snapshots, so they can be
handed to background work.

## Values

`CharacterRef(ownerId, characterId)` is the durable identity of a character: the
owning account and the character's own UUID.

`CharacterSession(ref, sessionId)` is one stretch of play as a character. Every
activation gets a fresh `sessionId`, including a reconnect and switching back to the
same character, so two sessions of the same character are never equal.

`CharacterInfo` is a snapshot holding the ref, the real name (without masks or
aliases), a `CharacterStatus` of `ALIVE`, `DEAD` or `MISSING`, the race ID (or
null), trait IDs in lower case, playtime in seconds and when the character was last
played (or null). `alive()` is true for `ALIVE`.

## Lookups

Call the API through the static `Characters` facade. It looks the service up on
every call, so it follows registration and unregistration without any work from the
caller.

| Method | Returns |
| --- | --- |
| `available()` | Whether a provider is registered. |
| `currentSession(Player)` | The session being played now, or empty. |
| `isCurrent(CharacterSession)` | Whether that session is still being played. It turns false when the session ends and never turns true again. |
| `info(UUID characterId)` | Any character, online or offline, or empty if unknown. |
| `deathId(UUID characterId)` | Most recent saved death ID, including after revival; empty when unknown. |
| `characters(UUID ownerId)` | Every character on the account, as an immutable copy. Empty means the records could not be read; an empty list means the account has none. |
| `lastPlayed(UUID ownerId)` | The character the account played most recently, dead or alive. |
| `findByName(String name)` | Living characters whose real name equals `name`, ignoring case, as an immutable list. Masks and aliases never match. Several characters can share a name, so callers that need one character must handle more than one match. |
| `displayName(Player)` | The name other players see now, including masks and aliases. |

`findByName` was added in TLibs 2.5.0. The interface has an empty default, so a
provider built against an older TLibs finds nobody.

Without a provider, lookups return empty, `findByName` returns an empty list,
`isCurrent` returns false and `displayName` returns the account name. That fallback is acceptable for display and
gameplay checks. Ownership and money must wait for `available()`, and must never
treat an empty `characters` result as an account with no characters.

## Delayed work

Anything that finishes later than it starts (a timer, a database callback, a
cast time) should record the session when it starts and check
`Characters.isCurrent(session)` just before applying its effect. This catches a
player who switches from Alice to Bob and back to Alice while the work is running,
which a character ID check alone would miss.

## Events

`CharacterSessionStartEvent(player, session)` fires once the character is ready to
play, after join setup or a switch.

`CharacterSessionEndEvent(player, session, reason)` fires with reason `SWITCH`,
`QUIT`, `DEATH` or `SHUTDOWN`. It runs while the outgoing character's data and body
are still loaded, before the provider saves or unloads anything. The session is
already no longer current, so no new action can start against it, but listeners can
still clean up against it.

`CharacterDeathEvent(character, deathId, at, killerId, killerCharacter, cause)`
fires only after the death has been saved, and does not fire if the save fails.
`killerId` and `killerCharacter` may be null; a killer character always belongs to
`killerId`. Delivery is not durable: a crash between the save and the event loses
it. Consumers must be idempotent by `deathId`. Since TLibs 2.4.1, they can reconcile
`DEAD` characters through `Characters.deathId(characterId)` after restart. The
interface has an empty default for older providers. RPCharacters preserves each
saved ID across revival and assigns a new one for the next death. Older deceased
records without a saved ID use a deterministic legacy key based on their character
UUID; a later saved death supersedes that key.

`CharacterRevivedEvent(character, previousDeathId)` fires after a dead character has
been saved as alive again, and not if that save fails. It was added in TLibs 2.6.0
with the [estate API](estates.md); delivery is not durable either.

None of these events can be cancelled.

## Provider obligations

A provider must fire the end event for a session, and let it finish, before
starting the account's next session, and must never nest transitions for one
account, such as starting a session from an end listener. It must never reuse a
session ID, must fire a `SHUTDOWN` end for every active session when it disables,
and must return immutable lists. The `CharacterIdentity` Javadoc lists the same
rules.

## Per-session state

`CharacterSessionMap<V>` holds at most one value per account, stored against the
session that put it. Create it on enable with the plugin and an optional
`onEnd(session, value)` callback, and call `close()` last in `onDisable`.

`put(session, value)` stores the value and returns true only if the session is
current; a late callback for an ended session gets false and changes nothing. If the
account still holds a value from an earlier session whose end the map missed, `put`
passes that value to `onEnd` first; a failing callback is logged and the new value
is still stored. `get(session)` returns the value only while that session is current
and is the one that stored it, and `get(player)` does the same for the player's
current session. `remove(session)` removes the value only if that session stored
it, without calling `onEnd`.

Inside end-event listeners the ending session is no longer current, so `get`
returns empty there. Clean up in `onEnd`, or take the value with
`remove(session)`.

When a session ends, the map calls `onEnd` with the stored value and then removes
it, even if `onEnd` throws. A value the next session stores while `onEnd` runs is
kept. The map listens at `MONITOR` priority, after lower-priority end listeners.

`close()` stops listening and flushes every remaining value through `onEnd`. Call
it last in `onDisable`: consumers may stop before the provider can fire `SHUTDOWN`.
It also works after the provider unregisters. A callback that throws an exception
does not stop the other values from flushing; the exceptions are then thrown
together as suppressed exceptions on an `IllegalStateException`. Errors are not
caught. Closing again or closing from an end callback does not flush the same entry
twice. Once closing begins, `put` throws `IllegalStateException`; before that it
returns false for a session that is not current.

Use the map for state that lives only while the character is played, such as a
loaded cache that `onEnd` flushes. Debts, refunds, character cooldowns and anything
else that must outlive the session belong in the plugin's own storage.
