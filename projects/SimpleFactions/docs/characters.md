# Character membership

Membership, leadership, councils, votes, mercenary enrollment and stored member
references use character UUIDs. Two characters played by one Minecraft account
can belong to different guilds, including rival realms. A player without a ready
character session has no membership. Menus capture the opening character session
and close when that session is stale.

## Migration and readiness

SimpleFactions waits for RPCharacters' reviewed legacy heir map before loading
faction state. During that wait commands report startup, timers and persistence
are inactive, and dependent plugins must defer loading or saving faction-owned
state. `SimpleFactionsApi.ready()` reports availability and
`SimpleFactionsReadyEvent` signals startup completion.

`migrations/character-v1.json` records progress for each store. Originals are
backed up under `migrations/backup/`; interrupted writes restore their backup and
replay. Legacy aliases resolving to one heir are merged. Unresolved records keep
their original JSON, role and amounts in quarantine, with stable record IDs.
Unresolved leaders block succession and disbanding.

Staff commands:

```text
/f admin quarantine list
/f admin quarantine assign <recordId> <characterId>
```

Assignments take effect on the next startup. Back up faction data together with
RPCharacters and DenarEconomy data before a coordinated cutover or rollback.

## Plugin APIs

`FactionManager.getByMember`, `getByLeader`, `getGuildByMember` and
`getGuildByLeader` accept a `Player`, a character `UUID`, or a stored member-key
`String`. UUID arguments are character IDs. Nullable lookups cannot distinguish
startup unavailability from absence: check `SimpleFactionsApi.ready()` before
making persistence decisions. The same player and UUID lookups on
`SimpleFactionsApi` return `Optional` values and remain empty until ready.

`Members.key(player)` resolves the active character. `Members.display(key)` is
its display name; `Members.online(key)` resolves only an online player currently
playing that character. Use those helpers instead of passing stored member keys
to Bukkit's account-name lookup methods.

A guild's immutable `getIncarnationId()` identifies its treasury across renames.
`Bank.accountId()` exposes the ledger account name for transactional callers.
Disbanding and recreating a guild with the same name gives it another incarnation.

## Public map data

The nation export uses an explicit public projection. Leader display fields,
member display names and counts, provinces, banners, public relations and guild
branches remain available. Character member keys, account balances, loans,
ledgers, elections, espionage and other private saved state are excluded.

See [the character identity API](../../TLibs/README.md) and
[DenarEconomy](../../DenarEconomy/README.md) for the shared providers.

## Combat identity

Warbands and battle roster IDs remain Minecraft account UUIDs for live combat.
Each enrollment also captures its character reference. Rejoining restores only
that character's former participation; switching characters does not inherit it.
`BattleStartedEvent.getParticipants()` and `BattleEndedEvent.getParticipants()`
return the captured character references, including participants who have since
disconnected. `getParticipantIds()` remains available for account-scoped callers.
