# BirdMessenger

[Project index](README.md)

Right-click the mailbox to send letters. Ordinary left-clicks are protected;
sneak-break to remove the mailbox deliberately.

The default `letter: ia.iasurvival:letter` accepts blank, sealed and opened
letter variants and the items listed in `letters-config.yml`. A custom `letter`
value matches only that item. An optional `letters` list overrides `letter`:

```yaml
letters:
  - ia.iasurvival:letter
  - ia.iasurvival:letter_written_letter
  - ia.iasurvival:letter_open_letter
```

## Recipient opt-out

Players can use `/rpcharacter mail off` in RPCharacters to hide their active
character from the recipient list, or `/rpcharacter mail on` to restore it. If a
recipient opts out before a sender confirms, the letter is returned; already-sent
mail still arrives.

## Character sessions

Sending from a mailbox needs a character in play. The letter slot, recipient
picker and head refresh belong to the character that opened the mailbox;
switching away and back closes them instead of bringing them back.

When a character stops being played, its menus close and any unsent letter goes
back to that character's inventory before RPCharacters saves it. A player who
logs out, or is online when the plugin stops, gets the letter in their inventory
if there is room; otherwise it waits in pending mail for that character. A death
that empties the inventory (keepInventory off for that death) drops the letter at
the player's feet instead, including a permadeath that ends the character.
Letters that cannot go straight back wait in pending mail and arrive with the
`unsent-returned` message the next time that character is played.

If a send fails while the character is still in play, the letter goes straight
back to the player. If mail storage refuses a letter for a character no longer
in play, BirdMessenger keeps it in memory and tries again whenever a character
starts. The log names the letter's item type, amount, display name, character and
owner; a letter still held when the plugin stops is lost, so staff can use that
entry to replace it.

Editing, signing and opening a letter also check, on the next tick, that the same
character is still in play before the item changes. While RPCharacters is running
but the player has no character in play, edits and signatures are refused with the
`letter-needs-character` message from `letters-config.yml` and the typed text is
not kept; sealed letters can still be read without breaking the seal. Without
RPCharacters, letter editing works on its own, unless RPCharacters starts in the
tick between the edit and the save.

In-flight mail belongs to the recipient character and survives character changes.
Delivery needs the stored owner to be playing the stored character. Pending
letters are handed over one at a time, checking the character before each; a
switch part-way leaves the rest queued, and the file is saved once afterwards.
Character IDs match regardless of letter case and are kept as written. Malformed
IDs and mail for another owner stay in the file and are not delivered to the
current character.

RPCharacters provides character sessions through the TLibs character API, as well
as the opted-in recipient list, head textures and flight destinations.
BirdMessenger requires TLibs 2.3.0 or newer; sending and delivery wait until
RPCharacters has registered its sessions. Estates need TLibs 2.6.0; on an older
TLibs letters for dead characters simply keep waiting.

## Letters after a death

New letters record the character that wrote them (`sender-character`) as well as
the account, both in flight and in the pending queue, and keep the mail's ID.

With TLibs 2.6.0, BirdMessenger is the `birdmessenger` participant in
RPCharacters estates. When a dead character's estate is decided, the letters
waiting in its pending queue move once, while the character is still dead with
that death and the estate is decided at the current revision:

- **With a will heir**, every waiting letter, including the dead character's own
  unsent letters, is re-keyed to the heir's character and account and delivered
  as ordinary mail when the heir is next played.
- **Without a will**, each letter goes back to whoever wrote it:
  - a letter that records its writer's character goes into that character's
    queue and arrives with the `returned-recipient-died` message ("Returned: the
    recipient has died");
  - an older letter that records only the writer's account goes into
    `returned_mail.yml` and arrives with the `returned-to-sender` message at that
    account's next character session, whichever character is played;
  - a letter whose writing character is dead or unknown, a letter with no
    sender, and the dead character's own unsent letters stay in its queue.
    `/estate show` lists them with their writer's character name, and staff deal
    with them by hand. A held letter goes back on its own if its writer is
    revived. Only moved letters are counted in the estate result.

Letters still in flight are left alone; they land in the dead character's queue
and the hourly reconcile moves them. Each moved letter keeps a stored ID (letters
queued before IDs were kept get one, saved, before anything moves), and
`plugins/BirdMessenger/estates/<deathId>.yml` lists every ID the estate has
planned before the queue changes. The outcome sent to the estate carries every
moved letter's ID, which `/estate show` displays; to undo a move by hand, find
those IDs in the receiving queues. The will screen and `/estate show` list a
character's waiting letters and who wrote them. BirdMessenger settles decided
estates on the first tick after start-up and every hour, and reports only
changed answers. A move is all or nothing: if a queue cannot be saved, every
queue is put back as it was and the estate is told to try again within the hour.

## Mail recovery

Mail is stored in `plugins/BirdMessenger/in_flight_mail.yml`,
`plugins/BirdMessenger/pending_mail.yml` and, for letters returned to an account,
`plugins/BirdMessenger/returned_mail.yml`. Each file is written whole: a flushed
temporary file replaces it, so a crash leaves the old or the new file. An estate
move saves `returned_mail.yml`
before it drops the letter from `pending_mail.yml`; if the server stops in between,
the next start keeps the account's copy and drops the other, logging a warning.
An older BirdMessenger ignores `returned_mail.yml` (keep it for re-upgrading) and
drops the new `id`, `sender-character` and `recipient-died` keys from the queue
when it next saves, so returned letters then arrive as ordinary mail.

If a mail file or one of its entries cannot be decoded, BirdMessenger preserves
the original file beside it as `<filename>.corrupt-<uuid>` before later saves can
replace it. These recovery copies include unreadable entries and should be kept
until the affected mail has been recovered. If the copy cannot be created,
startup fails and the affected file cannot be overwritten by the store.

Unsent letters on their way back to their writer are kept in `pending_mail.yml`
with `returned: true`.

## Build and verification

Follow [build and dependencies](README.md#build-and-dependencies) to prepare the
pinned shared and private dependencies, then run `mvn clean verify` with Java 21.

Before deployment, verify on a test server with ItemsAdder:

- Left-click the model and solid hitbox in survival and creative: the mailbox stays.
- Sneak-break: the mailbox can be removed, subject to existing region protection.
- Right-click and send sealed and opened letters: pages and delivery stay intact.
- Unrelated items and ordinary books are rejected; other furniture breaks normally.
- Switch characters from both the letter slot and recipient picker: the outgoing
  character keeps the unsent letter and the next character receives no stale menu.
- Switch away and back while a picker refresh or letter edit is queued: old work
  cannot change the current inventory.
- Die with the recipient picker open and keepInventory off: the letter drops at
  the death spot. With keepInventory on, it stays in the inventory.
- Log out with a full inventory while the picker is open: the letter returns with
  the `unsent-returned` message when that character is next played.
- Receive several pending letters, switching during delivery: remaining letters
  wait until their stored owner plays their stored character.
- Restart with pending and in-flight mail: delivery resumes without changing
  recipient opt-out behaviour or stored character IDs.
