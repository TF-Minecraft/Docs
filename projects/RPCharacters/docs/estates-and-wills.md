# Estates and wills

When a character dies for good, what it owned passes on 24 hours later. RPCharacters keeps the clock,
decides who receives each part and records the result; the plugins that hold the property move it.
A character can name an heir in a will, in game or on the website. This guide covers the estate
record, the decision, revival, the stored body, wills and the staff tools.

Estates need TLibs 2.6.0. On an older TLibs the plugin still enables and deaths still save, but no
estate is created; once TLibs is updated, the hourly reconcile creates the missing records.

## The estate record

Every death has one record, `plugins/RPCharacters/data/estates/<deathId>.json`. It is created inside
the permanent kill, straight after the death save, and holds the will as it stood at death, whether the
character was being played, the cause and the killer. Both the death save and every record write are
durable (temporary file, fsync, atomic rename, directory fsync), so a crash cannot leave a death
without its record or a record that says more than happened.

Two logs sit beside the records: `audit.log` (records opened, decided, revised, cancelled, revived and
every staff change, with the staff member's name) and `collections.log` (every batch of items handed
over, with a hash of each stack).

A record that cannot be read is logged and left alone. Its death never gets a second record; staff
repair the file and restart.

| State | Meaning |
|---|---|
| `OPEN` | Created at death. It falls due one wait after the death. |
| `HELD` | Staff stopped the clock. Releasing it restarts the clock with the time that was left. |
| `CANCELLED` | The character was revived while the estate was open or held. |
| `DECIDED` | Recipients are fixed and the participants move things. |
| `REVERTED` | Staff stopped all further movement. |

The wait is `estates.wait-hours` in `config.yml`, 24 by default and read at startup. Fractions work
for rehearsals (`0.05` is three minutes).

Deaths from before death records were kept have a stable death ID derived from the character ID and no
death time. The reconcile at startup, and every hour after, gives every dead character's latest death
a record if it has none; such legacy deaths fall due one wait after the reconcile that found them.
The reconcile also reopens a cancelled record whose character is still dead with that death.

## The decision

When a record falls due, RPCharacters reads the will heir, asks SimpleFactions for the guild the
character died in, and fixes four parts:

| Case | Money | Property | Guild locks | Letters |
|---|---|---|---|---|
| Heir; guild live with a leader | heir's bank | heir | leader | heir |
| Heir; guild live, no leader | heir's bank | heir | waiting | heir |
| Heir; guild gone, or no guild | heir's bank | heir | heir | heir |
| No heir; guild live with a leader | guild treasury | leader | leader | senders |
| No heir; guild live, no leader | guild treasury | waiting | waiting | senders |
| No heir; guild gone, realm live | realm treasury | frozen | frozen | senders |
| No heir; guild and realm gone | frozen | frozen | frozen | senders |
| No heir; no guild | frozen | frozen | frozen | senders |

The heir counts only if it is alive when the estate passes. A leader counts only if alive and not the
dead character. Property means private and public locks, doors, personal vehicles, shops, Research
stations and the stored body.

Some answers make the decision wait rather than guess, and it is tried again every minute: the dead
character's or the heir's account cannot be read, SimpleFactions has not answered, or it cannot say
whether the realm still exists. RPCharacters and SimpleFactions start in a cycle, so decisions due at
startup usually wait for SimpleFactions; they run again when SimpleFactions enables and when it fires
its ready event. If SimpleFactions started late, Thievery has already made its lock pass, and the
locks move at the next restart. An estate that has waited six hours is logged and shows under
`/estate list postponed`.

The decision is written once and never worked out again. Waiting parts are checked every hour: when
the death guild has a living leader they go to that leader; when the guild is gone, guild locks go to
the heir if there is one and everything else waiting is frozen. Each such change, and each staff
assignment, is a new revision. RPCharacters calls every participant again for it, and the record keeps
each participant's answer with the revision it answered.

## Participants

Participants register with TLibs. RPCharacters calls each one right after the decision, then every hour
for any that answered "retry" or has not answered the latest revision. A participant that is "blocked"
is listed for staff and not called again until staff clear it. A participant that moves things at
restart (Thievery) answers "at restart" until its startup pass reports. Each answer is stored with its
counts and the IDs of the records it moved, and the owner's website roster is updated.

RPCharacters' own participant is `rpcharacters-body`, below. Money, vehicles, locks, shops, stations
and letters are covered in their plugins' guides.

## The stored body

The body participant moves the dead character's whole stowed body: inventory, armour, offhand and
ender chest. After a death that left a grave, the stowed inventory is already empty, so only the ender
chest passes; after a death without a grave, or a kill of a character not being played, everything
does. It runs only with character bodies enabled, and only when the property goes to a character;
waiting or frozen property leaves the body untouched until staff assign it.

It answers "retry" while the dead character has no stowed body, or while the account's activation
lease still names the character (the body is still in the player's data until the respawn stows it).
A legacy dead character's body appears at the account's next join.

The strip is written in steps so that a crash at any point is safe:

1. The record is saved as `STRIPPING` with the body revision it read and the list of stacks to hand over.
2. The body is rewritten empty as the next revision, with the reason `estate:<deathId>`.
3. The record is saved as `COLLECTABLE`.

On replay, a body still at the read revision is stripped again; a body one revision later with the
estate reason only needs step 3; anything else, or a corrupt body, is blocked for staff. If the record
was lost but the body was stripped by this estate, the stacks are taken again from the previous
revision (`.body.prev`), but only when that revision is exactly one earlier and belongs to the same
character. The `.body.prev` of a stripped body still holds the items: do not restore it.

### Collecting

The recipient character collects with `/estate collect`, or by clicking the line shown when its session
starts ("You have an inheritance to collect"). Each collect fills free storage slots, one stack per
slot. The rest of the collection is saved before any item is given and the player data is saved after,
so a crash can lose at most the batch just handed over and can never duplicate it. Each batch is
logged with stack hashes in `collections.log`, which is how staff restore a lost batch by hand.

If the recipient dies before collecting, the collection follows the recipient's own estate: it is
re-addressed to that estate's property recipient when it is decided. While that estate's property is
waiting or frozen, the collection is parked for staff, who take it with `/estate collect <deathId>`.

## Revival

Staff revive from the Character Info screen as before: the owner must be online with a free living
slot. The revive is now a guarded transition. It saves the character as alive durably first, then
updates the estate, fires `CharacterRevivedEvent` and pushes the website roster. If the save fails the
character stays dead and nothing fires.

- An open or held estate is cancelled; the character keeps everything.
- A decided estate holds the revive back until nothing is waiting and every registered participant
  has finished the latest revision (or staff waived it). The refusal lists what is outstanding, such
  as "thievery moves its records at the next restart", and offers a one-use **[Force revive]** link for
  ten minutes. A forced revive records the time and "parts not yet moved stay with the character";
  from then on no participant moves anything for that death. Staff move anything back by hand.
- A forced revive in the middle of a body strip follows the body: a strip that never reached the body
  discards the collection, one that did stays collectable.

The character keeps its death ID after a revive. A later death has a new death ID and its own estate.

## Wills

A will names one heir, or none. Any living character other than the testator can be named, on any
account, including the player's own. Only the testator's account can change the will, and only while
the testator is alive. Nobody is told they were named.

The will lives on the character file as `will-heir`, `will-revision`, `will-updated-at-ms` and
`will-last-request`; each change bumps the revision and is saved durably. An older RPCharacters drops
these keys on its next save, so back up `characterdata/` before rolling back.

In game, `/will` or the **Will** button on the Character Info screen opens a dialog for the character
being played. It shows the heir, what the estate holds today (from each participant) and that pets and
animals are not included yet. **Name an heir** takes a name; one match asks for confirmation with name,
race, short ID and "on your account" where it applies, several matches give a list to choose from, and
characters played by players within 16 blocks are offered as buttons. Every click checks that the same
character is still being played; the buttons work once and expire after ten minutes.

On the website, the owner changes or revokes the will on the Profile page. RPCharacters pulls waiting
requests for its own realm every 15 seconds and acknowledges each one with the realm in the body. A
request is applied when the account owns the character, the character is alive, the request was made
from the current will revision and the heir is valid. The answers are `applied`, `stale` (changed in
game since the page was opened), `invalid heir`, `invalid` (unknown character or account) and
`character dead`. A request whose ID is already the character's `will-last-request` is answered
`applied` again, so a lost acknowledgement is safe. A request for an account that cannot be read, or
whose owner is still joining, waits for a later pull. Without a realm from TFMCWeb nothing is pulled;
a failed pull or acknowledgement backs off up to ten minutes.

## Website roster

Each roster row carries `died_at`, `death_id`, `will_heir_id`, `will_heir_name`, `will_revision` and,
when the latest death has a record, an `estate` object: state, due and decided times, revision, the
record's last write time, the heir's name, the recipient of each part, the money moved (from
DenarEconomy's answer) and each participant's answer and counts. RPCharacters pushes the owner's
roster on death, decision, revision, revive, collection and every participant answer that changes the
record, so the memorial updates while the owner is offline.

## Staff commands

All staff commands need `rpchar.estate.admin` (operators by default) and are written to `audit.log`.
An estate can be named by death ID, by character ID (its latest death) or by the dead character's name.

| Command | Effect |
|---|---|
| `/estate list [open\|held\|waiting\|frozen\|retry\|postponed\|empty]` | One line per estate: state, due time, recipients and each participant's answer. Estates that hold nothing appear only under `empty`. |
| `/estate show <estate>` | One estate in full: will, cause, killer, postponement, recipients, every participant's answer with counts and moved IDs ("awaiting restart" for Thievery), the body collection, and before the decision what each participant says the character holds. |
| `/estate hold <estate>` / `/estate release <estate>` | Stop an open estate's clock, or restart it with the time that was left. |
| `/estate decide <estate> --no-guild` | Decide a due estate without SimpleFactions' answer, as if the character had no guild. |
| `/estate assign <estate> <money\|property\|guildlocks\|all> <character>` | Give waiting or frozen parts to a living character (by name or ID; money goes to its bank). Makes a new revision and calls every participant again. |
| `/estate assign <estate> money guild <name\|incarnation>` | Send frozen money to a live guild's treasury. When two guilds share the name, use the incarnation ID. |
| `/estate collect <estate>` | Take a collection parked for staff into your own inventory, one batch at a time. |
| `/estate retry <estate> <participant>` | Clear a blocked answer once the cause is fixed, and call the participant again. |
| `/estate waive <estate> <participant> <note>` | Record a blocked participant as handled by hand, so it no longer holds back a revive. |
| `/estate revert <estate>` | Stop every further movement for a decided estate. Nothing is moved back. |

Money corrections use DenarEconomy's `/deco account` and `/deco move`; lock problems use
`/thievery locks quarantine`.

## Rollback notes

- Keep `data/estates/` for the record when rolling back.
- Stripped bodies stay stripped. The collection, or the batches in `collections.log`, is the source for
  restoring items by hand.
- Restore wills from a backup of `characterdata/` after re-upgrading (an older jar drops them).
