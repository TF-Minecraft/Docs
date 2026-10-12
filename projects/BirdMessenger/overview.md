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
RPCharacters has registered its sessions.

## Mail recovery

Mail is stored in `plugins/BirdMessenger/in_flight_mail.yml` and
`plugins/BirdMessenger/pending_mail.yml`.

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
