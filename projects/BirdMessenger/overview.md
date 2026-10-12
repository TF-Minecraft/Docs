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

Mailbox sending requires a ready character. The letter slot, recipient picker,
queued picker opening and skin refresh belong to the same player connection and
character activation. Switching away and back does not revive an old menu.
Ending that session closes its menus and returns unsent letters to the outgoing
inventory before RPCharacters saves it. Plugin shutdown also returns letters from
current sessions. When that inventory is no longer safe to use, the letter is
queued for its captured owner and character instead. Storage errors are logged;
failed unsent refunds remain in memory for retry on character start and plugin
shutdown. Repair a reported storage problem before stopping the plugin.

Letter editing, signing and opening preserve the original item checks and also
verify the captured session before changing an item on the next tick. While a
character provider is registered but no character is ready, edits and signatures
are refused; sealed books remain readable without rewriting the item. Standalone
letter editing remains available without a provider, provided one has not arrived
before the delayed write.

In-flight mail belongs to the recipient character and survives session changes.
Delivery requires a ready session for the stored owner and character. Pending
mail is removed one letter at a time, checking the same session between letters;
a switch during delivery leaves the rest queued. Existing UUID text is preserved,
including uppercase spelling. Malformed character IDs and mail for another owner
are retained and are not delivered to the current character.

The shared TLibs API supplies session identity. RPCharacters still supplies the
mail-specific opted-in recipient list, head textures and flight destinations.
BirdMessenger requires TLibs 2.3.0 or newer; missing provider registration blocks
sending and delivery until it becomes available.

## Mail recovery

Mail is stored in `plugins/BirdMessenger/in_flight_mail.yml` and
`plugins/BirdMessenger/pending_mail.yml`.

If a mail file or one of its entries cannot be decoded, BirdMessenger preserves
the original file beside it as `<filename>.corrupt-<uuid>` before later saves can
replace it. These recovery copies include unreadable entries and should be kept
until the affected mail has been recovered. If the copy cannot be created,
startup fails and the affected file cannot be overwritten by the store.

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
- Receive several pending letters, switching during delivery: remaining letters
  wait for a ready session of their stored owner and character.
- Restart with pending and in-flight mail: delivery resumes without changing
  recipient opt-out behavior or stored character IDs.
