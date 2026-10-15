# Character membership

Membership, leadership, councils, votes, mercenary enrollment and stored member
references use character UUIDs. Two characters played by one Minecraft account
can belong to different guilds, including rival realms. A player without a ready
character session has no membership. Menus capture the opening character session
and close when that session is stale.

## Migration and readiness

SimpleFactions waits for RPCharacters' reviewed legacy heir map and DenarEconomy's
ledger before loading faction state. During that wait commands report startup, timers and persistence
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

## Member prestige

The Members prestige line has a headcount part, `(heads + 4)^1.8 + 5`, and a
playtime part, where each counted member character adds `2^(online hours / 100)`
with the exponent capped at `max-prestige-playtime-exponent` (32 at the default 5).

Each account adds at most one head in total. It is split between the account's
living characters by how long each was played over the last
`member-share-window-days` (30) UTC days, including characters outside any
faction. An account with no play in that window splits by lifetime playtime,
and evenly when that is zero too. A member with no share adds neither headcount
nor playtime, so an alt that is not played adds nothing. Dead characters take
no share. A member the character directory cannot place, or that is missing
from its account's character list, counts as one head.

SimpleFactions credits the current character of each online player every
minute and saves the counts to `Cache/recent-playtime.json`. An unreadable file
is left in place and not overwritten until it loads at a later startup; counts
from that run are lost, with a warning at shutdown.

## Plugin APIs

`FactionManager.getByMember`, `getByLeader`, `getGuildByMember` and
`getGuildByLeader` accept a `Player`, a character `UUID`, or a stored member-key
`String`. UUID arguments are character IDs. Nullable lookups cannot distinguish
startup unavailability from absence: check `SimpleFactionsApi.ready()` before
making persistence decisions. Player and UUID lookups are unavailable until
startup recovery completes. The same player and UUID lookups on
`SimpleFactionsApi` return `Optional` values and remain empty until ready.

`Members.key(player)` resolves the active character. `Members.display(key)` is
its display name; `Members.online(key)` resolves only an online player currently
playing that character. Use those helpers instead of passing stored member keys
to Bukkit's account-name lookup methods.

A guild's immutable `getIncarnationId()` identifies its treasury across renames.
`Bank.accountId()` exposes the ledger account name for transactional callers.
Disbanding and recreating a guild with the same name gives it another incarnation.

### Lock guilds

`SimpleFactionsApi.lockGuild(UUID characterId)` returns the live guild that a
character's GUILD and FACTION locks follow, as an `Optional<Guild>`:

| Character | Answer |
|---|---|
| Alive, including revived | `getGuildByMember(characterId)`, the first matching guild. A revived character left every guild at death, so their old guild has no access until they rejoin. |
| Dead | The guild they belonged to at death, while that incarnation still exists. |
| Missing, deleted, unknown or on a quarantined account | Empty. |

The answer is empty until `SimpleFactionsApi.ready()`; treat that as
unavailable rather than guildless. Compare guilds by incarnation. A disbanded
guild recreated under the same name does not inherit access, and a guild keeps
its incarnation when it changes realm.

Each death journal records `lockGuildIncarnation` when the death is captured,
including deaths first found by the startup reconcile. It also records that
guild's realm as `lockGuildRealm` for [estates](estates.md#death-guild). It is the first guild
`getGuildByMember` would have answered at that moment. A member moved into a
civil war's rebel main guild records the guild untangle would return them to,
resolved at death:

| Rebel main guild member | Recorded guild |
|---|---|
| Moved, origin guild still in the host or among the rebel guilds | The origin guild |
| Moved, origin guild gone | The host's main guild |
| Not moved (joined during the war or was already a member) | The rebel main guild, which keeps its incarnation when the host absorbs it |

The wanted leader is recorded like any moved member, even though untangle
returns a living wanted leader to the main guild after an attacker victory. An
origin guild disbanded after the death leaves the answer empty.

SimpleFactions keeps the dead characters' guilds in memory. It builds that
index at startup, after the death reconcile and before it reports ready, from
each character's most recent journal. Two journals at the same moment give no
answer. Journals written before the field existed use the first guild listing
the character in their rights snapshots, without the civil-war mapping. Each
new death updates the index, and a death outside any guild removes the
character's entry.

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
Persisted memberships, leadership and invitations require that recorded
character's current session. Reviewed legacy expansion and held-slot recovery
are described in [warband character authority](warbands.md).
`BattleStartedEvent.getParticipants()` and `BattleEndedEvent.getParticipants()`
return the captured character references, including participants who have since
disconnected. `getParticipantIds()` remains available for account-scoped callers.

## Death and succession

Committed character deaths, startup reconciliation and hourly reconciliation
use the same durable death journal, keyed by RPCharacters' authoritative death
ID. Cleanup removes the deceased character's membership, offices, council and
voting rights, movement participation and captured warband participation. It
also ends a council session hosted by that character. Another character on the
same Minecraft account keeps its own rights.

Cleanup saves each affected faction or warband before acknowledging that step.
Fixed wages and the captured per-member dividend amount become payable claims
only after the original payout rights are durably removed. They survive guild
or faction dissolution and remain payable to the deceased character's bank.
Daily settlement records actual cents paid, including partial payments.

An ordinary guild leader's successor is the first living remaining member in
its original join order. When no living member is left to succeed, the guild
stays open without a leader (see [leaderless guilds](#leaderless-guilds)). A
completely empty realm is removed while its ledger treasury remains. If the
ruling guild empties but another guild still has members, the realm and its
treasuries remain: elective governments start the normal election; a
nonelective ruler remains vacant for staff resolution. Unresolved quarantined leaders block succession
and disbanding. A later staff appointment is preserved during replay.

Dead warband leaders pass leadership to the captured first living participant,
or leave a vacant seat when none is available. Pending rejoin records still
identify the deceased character if its session ended before the death event.

Replay acts only on the life its journal belongs to. A revived or re-dead
character's unfinished journal is closed without running its remaining steps,
and a living seat holder is never replaced; see
[revived and re-dead characters](estates.md#revived-and-re-dead-characters).

See [treasury recovery](treasuries.md) for journal paths and coordinated backup
requirements.

### Leaderless guilds

A leaderless guild keeps its treasury, branches and settlements. Menus and the
public map show its leader as "Name (dead)". The guild file records the dead
leader as `dead leader`, the death time as `leaderless since`, when it was last
left with no members as `empty since`, and any standing offer as
`leader offer`; filling the seat by any route clears them all. It cannot be
evicted or elevated, and when its realm releases its guilds it stays with the
realm.

The realm leader offers the seat with `/guild appoint <guild> <name>` to a
living member of the realm who leads no guild. The guild list shows the command
to the realm leader, and both the realm leader and the offered character are
reminded when they start playing that character. The offered character accepts
with `/guild lead <guild>` or declines with `/guild decline <guild>`, through the
chat buttons or by typing. Accepting moves the character out of their current
guild, makes them leader and saves the realm durably. If that save fails,
nothing changes and the offer stands (see below). A new offer replaces the old one; an offer
to a character who dies is withdrawn. Staff can fill the seat with any living
realm member who leads no guild, using `/guild forceleader <guild> <name>`, even
when the guild has no members.

Estates treat a leaderless guild as live with no leader: money goes to its
treasury, guild locks go to the realm leader, and property waits until a leader
is appointed (see [estates and wills](../../RPCharacters/docs/estates-and-wills.md#the-decision)).

The hourly reconcile starts the 30-day clock when it finds a leaderless guild
with no members, stops it when the guild has members again, and removes the
guild once the clock runs out. Estate parts still waiting for its leader then
follow the rules for a guild that has gone.

An older SimpleFactions jar keeps a leaderless guild with a blank leader but
drops the four fields on its next save, and its `/guild forceleader` only picks
existing guild members, so an empty leaderless guild cannot be filled there.
Back up `Data/` before rolling back and restore the fields from the backup when
upgrading again.

If a leadership save fails, the change is undone and saved again. When that
second save also fails, the player is told staff may need to check the guild and
the server log names the realm file, which may hold either state. While a
closed guild's removal is not yet saved, estates treat the guild as unanswered
and wait; the hourly check retries the save.
