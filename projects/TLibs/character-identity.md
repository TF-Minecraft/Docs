# Character identity API

[TLibs](README.md) · [All projects](../../README.md)

TLibs defines one API for asking which character a player is playing, in
[`net.tfminecraft.tlibs.character`](https://github.com/TF-Minecraft/TLibs/tree/main/src/main/java/net/tfminecraft/tlibs/character).
TLibs only defines it. A character plugin provides it by registering a
`CharacterIdentity` service in Bukkit's `ServicesManager` once its records have
loaded. No released plugin registers it yet; RPCharacters will, as part of
[RPCharacters#89](https://github.com/TF-Minecraft/RPCharacters/issues/89).

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
| `characters(UUID ownerId)` | Every character on the account. Empty means the records could not be read; an empty list means the account has none. |
| `lastPlayed(UUID ownerId)` | The character the account played most recently, dead or alive. |
| `displayName(Player)` | The name other players see now, including masks and aliases. |

Without a provider, lookups return empty, `isCurrent` returns false and
`displayName` returns the account name. That fallback is acceptable for display and
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
it, and a later replay may deliver it again, so consumers must be idempotent by
`deathId`.

None of these events can be cancelled.

## Per-session state

`CharacterSessionMap<V>` holds at most one value per account, stored against the
session that put it. Create it on enable with the plugin and an optional
`onEnd(session, value)` callback, and call `close()` on disable.

`put(session, value)` stores the value and returns true only if the session is
current; a late callback for an ended session gets false and changes nothing.
`get(session)` returns the value only while that session is current and is the one
that stored it, and `get(player)` does the same for the player's current session.
`remove(session)` removes the value only if that session stored it, without calling
`onEnd`.

When a session ends, the map calls `onEnd` with the stored value and then removes
it, even if `onEnd` throws. It listens at `MONITOR` priority, after lower-priority
end listeners. Providers must finish dispatching the end event before starting
another session; nested transitions would interrupt outgoing cleanup.

`close()` stops listening and flushes every remaining value through `onEnd`. Call
it on disable: consumers may stop before the provider can fire `SHUTDOWN`. It also
works after the provider unregisters. A failed callback does not prevent the other
values from flushing; failures are reported together as suppressed exceptions on
an `IllegalStateException`. Closing again or closing from an end callback does not
flush the same entry twice, and writes are rejected once closing begins.

Use the map for state that lives only while the character is played, such as a
loaded cache that `onEnd` flushes. Debts, refunds, character cooldowns and anything
else that must outlive the session belong in the plugin's own storage.
