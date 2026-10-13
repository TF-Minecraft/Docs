# Estate API

[TLibs](README.md) · [All projects](../../README.md)

TLibs defines how a dead character's property passes to its heirs, in
[`net.tfminecraft.tlibs.character.estate`](https://github.com/TF-Minecraft/TLibs/tree/main/src/main/java/net/tfminecraft/tlibs/character/estate).
It only defines the API. RPCharacters decides each estate and registers an
`EstateService`; SimpleFactions registers an `EstateFallback` that answers guild
questions; every plugin that moves records for a dead character registers an
`EstateParticipant`. All three are Bukkit `ServicesManager` services, so no plugin
needs a hard dependency on another. The API was added in TLibs 2.6.0 and builds on
the [character identity API](character-identity.md).

Every call runs on the main thread. The `Estates` facade throws
`IllegalStateException` from any other thread. Values are immutable records, so
they can be handed to background work.

## Probing

A server may run an older TLibs. Plugins that take part in estates check for the
API once, with `Class.forName("net.tfminecraft.tlibs.character.estate.Estates")`
inside `try/catch (ReflectiveOperationException | LinkageError)`, and keep every
call to it behind a bridge class. Without TLibs 2.6.0 the plugin does not register
a participant and its records stay with the dead owner.

## The decision

`EstateDecision` is written once per death and never re-derived. It holds the
`deathId`, the testator's `CharacterRef`, when it died (`diedAt`, empty for deaths
saved before death times were kept), `decidedAt`, the living will heir if any, the
death guild's incarnation and its realm, the four part recipients and a
`revision`. Resolving a waiting part or a staff assignment writes a new revision;
nothing else changes a decision.

Each part has its own allowed recipients, and the record refuses any other:

| Part | Recipients |
| --- | --- |
| `money` | `ACCOUNT(accountId)`, `FROZEN` |
| `property` | `CHARACTER(ref)`, `WAITING`, `FROZEN` |
| `guildLocks` | `CHARACTER(ref)`, `WAITING`, `FROZEN` |
| `letters` | `CHARACTER(ref)` (the will heir), `SENDER` |

`Recipient` is a sealed type. Build values with `Recipient.account(id)`,
`Recipient.character(ref)` and the constants `WAITING`, `FROZEN` and `SENDER`.
`kind()` gives a stable name for storage, `character()` and `account()` return the
destination when there is one, and `isCharacter()`, `isWaiting()` and `isFrozen()`
answer the common questions. Write the record type as `Recipient.Character`, since
importing it would hide `java.lang.Character`. `anyWaiting()` on the decision says
whether property or guild locks still wait for the death guild.

Realms are identified by the incarnation of their ruling guild. That is the value
in `deathRealm` and in the `realm` fields below, so looking a realm up with
`guild(realm)` returns its treasury account.

## Participants

A participant implements `id()`, `settle(decision)` and, optionally,
`describe(characterId)`. The ID is stable and unique, such as `denareconomy`,
because estate records store it. `describe` returns `Holdings`: counts per kind and
a few short labels, for the will screen and staff. The default is `Holdings.NONE`.

`settle` makes the plugin's records match the decision and returns an `Outcome`:

| Outcome | Meaning |
| --- | --- |
| `done(counts, movedIds)` | Everything is where the decision says. `movedIds` names every record moved, so staff can restore them by hand. `done()` means there was nothing to move at this revision. |
| `retry(reason)` | Not yet; RPCharacters calls again within the hour. |
| `AT_RESTART` | The participant moves its records at the next restart. |
| `blocked(reason)` | Listed for staff and not retried until staff clear it. |

A participant acts only while `Estates.guardHolds(decision)` holds: the testator is
`DEAD` with the decision's `deathId`, and that estate is `DECIDED`, not reverted,
at the decision's revision. A revival, a later death, a staff revert or a newer
revision all fail the guard. Participants leave `WAITING` and `FROZEN` parts where
they are and must be idempotent: settling the same revision twice moves nothing
twice, and a plugin whose moves touch more than one store keeps its own journal and
replays it at boot.

Each participant also reconciles over `Estates.decided()` at boot and hourly, and
reports with `Estates.report(deathId, participantId, revision, outcome)`, giving
the revision it answered. A `DONE` for an older revision does not count. `report`
returns false when no estate service received it; report again at the next
reconcile.

## Guild answers

`EstateFallback` only reads; it never creates a guild or treasury. Call it through
the facade, which answers `UNAVAILABLE` when SimpleFactions has not registered one.
`UNAVAILABLE` means "cannot tell now". Callers postpone; they never read it as "no
guild" or "gone".

| Method | Answers |
| --- | --- |
| `deathGuild(characterId, deathId)` | `DeathGuild.UNAVAILABLE`, `DeathGuild.NONE` (no guild at death), or `DeathGuild.guild(incarnation, live, leader, realm)` |
| `guild(incarnation)` | `GuildLookup.UNAVAILABLE`, `GuildLookup.GONE`, or `GuildLookup.live(GuildRef)` |
| `guildByName(name)` | The same, matching the name without regard to case |

`GuildRef` carries the incarnation, name, realm, leader and treasury account
(`guild:<incarnation>`). Leaders are character IDs and may be dead; callers check
them with `Characters.info`.

## Estate service

| `Estates` method | Returns |
| --- | --- |
| `available()` | Whether RPCharacters has registered its estate service. |
| `decision(deathId)` | The current decision for that death, decided or reverted, or empty. |
| `decided()` | Every `DECIDED` estate at its current revision, as an immutable list; reverted estates are left out. |
| `stateOf(characterId)` | `OPEN`, `HELD`, `CANCELLED`, `DECIDED` or `REVERTED` for the character's latest death, or empty. |
| `participants()` | Every registered participant, as an immutable list. |
| `fallback()` | The registered `EstateFallback`, or empty. |

The facade looks services up on every call, so it follows registration and
unregistration without any work from the caller. Without an estate service,
lookups return empty, `decided()` returns an empty list and reports are dropped.

## Events

`EstateDecidedEvent(decision)` fires after a decision, or a later revision of it,
has been saved. `CharacterRevivedEvent(character, previousDeathId)`, in
`net.tfminecraft.tlibs.character`, fires after a dead character has been saved as
alive again, and not if that save fails. Both are synchronous and cannot be
cancelled. They are wake-ups only: delivery is not durable, so consumers also
reconcile after a restart, through `Estates.decided()` and `Characters.deathId`.
