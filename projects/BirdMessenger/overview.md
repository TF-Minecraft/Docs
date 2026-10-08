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
