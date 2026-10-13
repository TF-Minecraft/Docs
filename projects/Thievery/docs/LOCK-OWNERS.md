# Lock owners

Every Thievery lock belongs to a character. Chests, barrels and other containers,
locked doors, armour stands, item frames and lockable furniture record the owning
character's ID, and only that character, played in a current session, counts as the
owner. Another character on the same account is a stranger: it cannot open a private
lock, rotate the lock state, clear a private lock's clues or merge a chest onto it. Staff with
`thievery.admin` keep their override.

## Who owns a lock

Placing a container, display or lockable furniture piece gives it to the character
you are playing, with a PUBLIC lock. Opening an unowned container claims it for that
character, and a sneak toggle claims an unowned display. Locking a door with a
master key records the character as the door's owner; the key stays the credential
for opening, unlocking and breaking the door.

Without a current character session, placing still works but leaves the block or
display unowned (any stale record left at that spot by a container that was blown up
is removed), while claims, rotations and door locking
are refused with "Play a character to claim or change locks." Staff without a
current character are the exception for placement and door locking: the lock is
stamped as a **server** lock, starts PRIVATE and opens only through the staff
override. Server hoppers may move items between server containers, so staff
automation keeps working. Server locks cannot be picked.

## Access

PUBLIC and unowned locks are open to everyone. A PRIVATE lock opens for the owning
character only. A GUILD lock opens for characters in the guild the owner's locks
follow, compared by guild incarnation, so a disbanded and recreated guild with the
same name does not inherit access. A FACTION lock opens for characters whose guild
is in the same faction as that guild.

The guild a lock follows comes from SimpleFactions' `lockGuild`: the owner's current
guild while they live, and the guild they belonged to when they died afterwards. A
dead owner's GUILD and FACTION locks therefore keep working for that guild until
their estate moves them (see [Estates](#estates)). A
revived character lost their guild at death, so their guild has no access until they
rejoin. When SimpleFactions is not ready, or is older than 4.1.0 and has no
`lockGuild`, GUILD and FACTION locks deny everyone except staff.

Both halves of a double chest are read together. Opening fills an unowned half from
its owned partner, and a wholly unowned double chest is claimed for the opener. An
unreadable half is never copied onto its partner; the chest is listed for staff. When
the halves have two different owners, nothing is synced: opening still needs access
to both halves, nobody can rotate the chest (staff included), thieves cannot pick it,
and staff see it in the quarantine list until they set one owner with
`/thievery locks setowner`.

## Automation

A block hopper moves items only to and from containers with exactly its own owner,
checking both halves of a double chest. An unowned half goes with its owned
partner. Hoppers on another character's chest stop, including an alt's hopper under
its main's chest.

A hopper minecart has no owner. Its moves are cancelled whenever the source or
destination is an owned container that is not PUBLIC, including either half of a
double chest. Owners cannot drain their own private storage with a hopper minecart;
use a block hopper, or make the chest PUBLIC. A block hopper that pushes into an
entity container, such as a chest minecart, is unaffected.

## Picking and clues

Thieves pick character locks as before. With `lockpicking.require-owner-online: true`,
a lock needs a member of its lock guild online, or, without a guild, the owning
character in play, or an open lockpick window. The messages never name the owner or
the guild: "Cannot lockpick - this lock's owners are away." A dead owner with no
lock guild is never online, so their lock can only be picked while a window is open.
Server locks, quarantined locks and unreadable records cannot be picked.

Clue bookkeeping keys a lock's victim as `guild:<incarnation>`, otherwise
`player:<characterId>`, and a pickpocket's victim by the character they are playing.
Clue keys written before character locks age out.

Clue clearing on a PUBLIC or unowned container is open to anyone. A PRIVATE container
needs the owning character, and a GUILD or FACTION container anyone that lock lets in.
On a door, the owning character or a member of its lock guild may clear clues.

## Estates

When RPCharacters decides a dead character's estate, their
locks pass at the next restart. Locks move only in the startup pass described below,
never while players are online.

| Record | New owner |
|---|---|
| Container, armour stand or item frame, PRIVATE or PUBLIC | the estate's property recipient |
| Container, armour stand or item frame, GUILD or FACTION | the estate's guild-locks recipient |
| Locked door | the property recipient |
| Lockable furniture | as for containers, on the first interaction after the decision |

Only the owner changes. The lock state and the thief cooldowns stay, so a GUILD
chest given to the death guild's leader is still a GUILD chest. A door's owner passes
but its keys do not; staff can make the recipient a key. A part that is waiting for
a guild leader, or frozen for staff, stays with the dead owner and keeps the rules
above until a later revision of the estate gives it a recipient; it then moves at
the following restart.

A lock moves only while the estate's guard holds: the owner is still dead with the
same death, and the estate is decided and not reverted. The halves of a double chest
move together. A bare owner value of the dead character's that the migration marks
in the same pass moves at the next restart, and so do the chests beside it.

After the pass, Thievery reports each decided estate to RPCharacters from what is
left on disk. It answers DONE, with counts per store and every moved file path, only
when the dead owner holds nothing more in a part that goes to a character. If locks
remain to be moved it answers that they move at restart, and if the estate planner
failed it answers RETRY. Between restarts Thievery answers "at restart" whenever an
estate gains a part going to a character for which the dead owner still held locks,
so a revive of that estate waits for a restart. The log line
`Estate <deathId> (revision N): locks DONE, … moved in all, … still with the testator.`
records each report.

Estates need TLibs 2.6.0. On an older TLibs Thievery logs a warning, takes no part in
estates and a dead owner keeps their locks.

## Staff commands

Both commands need `thievery.admin` and are written to the server log and to
`plugins/Thievery/logs/locks-audit.log`.

`/thievery locks quarantine` shows whether locks are running or frozen (and why),
then the quarantined records with a count for each stored owner, unreadable records,
files missing after a migration replay, and double chests with two owners. The full
list is in `plugins/Thievery/migrations/quarantine.json`.

`/thievery locks setowner <character|uuid|server>` sets the owner of the container
(both halves of a double chest), locked door, lockable armour stand or item frame, or
lockable furniture piece you look at within 5 blocks. It keeps the lock state, except
that an unreadable record becomes PRIVATE and a lock given to `server` always becomes
PRIVATE, as server placements are; the reply says so. A door keeps its key, which
still opens it after it is given to `server`. Staff without a character cannot
enter the world when character bodies are on, so this is how they make a server lock.
The thief cooldowns of an unreadable container are kept when they can still be read. A UUID must be a known living
character's ID; a dead character is refused, because their locks pass through their
estate. A name must match exactly one living character; names
need TLibs 2.5.0, and without it use the UUID. A door whose record has lost its key or
its strength cannot be repaired this way, so the lock is never weakened: break the
door in Creative to remove it. Fixed records leave the quarantine list straight away.

## Storage

Lock files keep the owner as a bare UUID and add `ownerKind`, which is `CHARACTER`
or `SERVER` (stored as the nil UUID):

| Store | Path | Owner fields |
|---|---|---|
| Containers | `plugins/Thievery/data/<chunkX>_<chunkZ>/<x>_<y>_<z>.json` | `owner`, `ownerKind` |
| Doors | `plugins/Thievery/door-data/<chunkX>_<chunkZ>/<x>_<y>_<z>.json` | `ownerUUID`, `ownerKind` |
| Entities | `plugins/Thievery/entities/<entityUuid>.json` | `owner`, `ownerKind` |
| Furniture | InteractibleFurniture variables | `thievery.owner`, `thievery.ownerKind` |

Every write goes to a temporary file in the same directory and is then moved into
place atomically. A record is written only when it changed; owner, kind and state
changes are forced to disk, while thief cooldown changes in `accessMap` are not.
Thief cooldowns stay keyed by account.

A record that cannot be read loads locked, with an unresolved owner: an empty,
truncated or `null` file, a bad UUID, an owned record with a missing or unknown lock
state, an unknown `ownerKind`, or garbage furniture variables. Such a lock denies
everyone except staff, cannot be picked, is never overwritten by ordinary play, and
is listed for staff. An error inside a lock listener cancels the event, including a
linkage error from a changed SimpleFactions or TLibs API.

A bare UUID without `ownerKind` is classified once whenever its record is loaded: a
known character ID is a character, an account with a reviewed heir is a legacy
owner, the nil UUID is the server, and anything else is unresolved. Legacy and
unresolved owners deny everyone except staff on non-PUBLIC locks and cannot be
picked. A classification made while character identity is unavailable is never
written back.

Furniture is upgraded on first interaction instead of at startup: a bare character ID
gains its marker, a legacy account moves to its reviewed heir, and a dead owner's
piece passes through a decided estate. Furniture values
written by older jars stay readable until stage 7.

## Startup, guard mode and the migration

Thievery registers its listeners in guard mode at the start of `onEnable`. In guard
mode the lock stores are frozen: the container, door and entity data managers save
nothing, and deletions (for example an item frame knocked off its wall) wait in a
queue. Players see "Locks are starting up. Try again shortly." when they try to
place or break a lockable, rotate or claim a lock, pick a lock, lock or unlock a
door, or clear clues. Owned, non-PUBLIC containers and displays stay shut to
players, and staff see a read-only copy of a container. PUBLIC and unowned
containers open normally without being claimed. Key holders can still open locked
doors. Block hoppers and hopper minecarts touching an owned container stop.
`resetcooldowns`, `setowner` and `testpick` on a container are refused.

At the end of `onEnable` Thievery checks its gates in order. TLibs must offer the
reviewed-heir lookups (2.4.0 or later). Every store's `data-version` must be one this
jar understands. Character heirs must be ready, which is normal because RPCharacters
is a hard dependency and registers first. If any gate fails, locks stay in guard mode
until the server restarts, and the log says why with a SEVERE line. If everything
passes, the migration runs, the owner cache is cleared, queued deletions are applied
and locks switch to normal operation.

The migration runs on the main thread before anyone can join. It scans every
container, door and entity file, classifies each distinct bare owner once and
rewrites the files it can settle: character IDs gain `ownerKind: CHARACTER`, the nil
UUID gains `SERVER`, and an account with a reviewed heir moves to that heir character.
Accounts without a heir, and values that cannot be classified yet, stay as they are
and go on the quarantine list, which every boot retries. A bare value written later,
for example by an older jar, goes through the same journalled pass on the next boot.
The same pass moves the locks of decided estates (see [Estates](#estates)). The log
line `Lock migration: … N moved for M decided estates, in N ms` records the counts
and duration.

Each pass that rewrites files first archives every lock file it scanned to
`plugins/Thievery/migrations/backup/locks-NNNN.zip` (a pass that only moves estate
locks archives just the files it rewrites), then writes
`migrations/journal-NNNN.json` with each file's original hash and the hash of the
exact bytes it will write. Each entry is marked `"kind": "migrate"` or
`"kind": "estate"`, and estate entries carry their `deathId`. It rewrites the files by atomic move, forces every
directory it wrote into, marks the journal completed and writes `data-version` into
each store. If the server stops during the pass, or the pass throws (locks then stay
frozen until a restart), the next boot replays the unfinished journal: files already
at their new hash are done, files at their original hash are rewritten, a torn file
is taken from the archive and rewritten, and a missing file is listed for staff and
never restored. An estate entry is replayed only while its estate still applies;
otherwise the file keeps (or gets back from the archive) its original bytes and the
entry is marked `"skipped": true`. A journal is never archived twice, and a completed journal is never
replayed.

## Rolling back

Stop the server and roll back the whole stage 6a set together. Thievery's part is the
offline tool [`tools/thievery_rollback.py`](https://github.com/TF-Minecraft/Thievery/blob/main/tools/thievery_rollback.py)
in the source checkout. It needs only Python 3 and runs against the plugin folder:

```sh
python3 tools/thievery_rollback.py /path/to/plugins/Thievery
python3 tools/thievery_rollback.py /path/to/plugins/Thievery --apply --report rollback.json
```

Without `--apply` it is a dry run that writes nothing. It processes every
`migrations/journal-NNNN.json` newest first and restores a file from that journal's
archive only if the file's current SHA-256 still equals the journal's `newHash` and
the archived copy matches `originalHash`. Files changed or deleted since the migration,
and archive copies that do not match, are listed and left alone. With `--apply` it then
deletes the journals, `data-version` in `data/`, `door-data/` and `entities/`, and
`migrations/quarantine.json`, so a later upgrade starts clean; the archives are kept.
If a journal or archive cannot be read it stops with exit code 2 and writes nothing.
`--report` saves the per-journal result as JSON.

To undo only estate moves, keeping the character-lock migration, add `--estate-only`:

```sh
python3 tools/thievery_rollback.py /path/to/plugins/Thievery --estate-only --apply
```

It restores only entries marked `"kind": "estate"`, on the same conditions, and keeps
the journals, `data-version` and `quarantine.json`. Entries marked `skipped` moved
nothing and are left out in both modes. Revert the estate (`/estate revert`) or put
back the previous Thievery jar first, or the next boot moves the locks again. A
Thievery older than 1.8.0 that completes an unfinished journal rewrites it without
`kind` and `deathId`; those entries can then only be undone by a full rollback.

Then put back the previous jars.

Under the old jars, lock files left unrestored, furniture upgraded since the
migration and server locks hold values the old code cannot match, so they deny
everyone except staff. That is expected and fails closed. Running an older Thievery
on migrated stores without this procedure is unsupported.
