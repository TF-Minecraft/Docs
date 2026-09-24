# BirdMessenger


Right-click the mailbox to send letters. Ordinary left-clicks are protected;
sneak-break to remove the mailbox deliberately.

The default `letter: ia.iasurvival:letter` accepts blank, sealed and opened
letter variants, including for existing configurations. The default also accepts letter variants configured by the transferred sealing
feature. Custom legacy values still match only that item. An optional `letters` list overrides `letter`:

```yaml
letters:
  - ia.iasurvival:letter
  - ia.iasurvival:letter_written_letter
  - ia.iasurvival:letter_open_letter
```

Build with Maven and **JDK 21**, using the Minecraft **1.21.10** API. Install
the matching TLibs and RPCharacters Maven dependencies (see the
[shared installer guide](../TLibs/README.md)), populate `libs/ItemsAdder.jar`
with the checksum-pinned dependency, then run `mvn clean verify`. See
[build and dependencies](README.md#build-and-dependencies) for the current coordinates
and dependency preparation workflow.

Before deployment, verify on a test server with ItemsAdder:

- Left-click the model and solid hitbox in survival and creative: the mailbox stays.
- Sneak-break: the mailbox can be removed, subject to existing region protection.
- Right-click and send sealed and opened letters: pages and delivery stay intact.
- Unrelated items and ordinary books are rejected; other furniture breaks normally.
