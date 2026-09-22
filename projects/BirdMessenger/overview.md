# BirdMessenger


Right-click the mailbox to send letters. Ordinary left-clicks are protected;
sneak-break to remove the mailbox deliberately.

The default `letter: ia.iasurvival:letter` accepts blank, sealed and opened
letter variants, including for existing configurations. Custom legacy values
still match only that item. An optional `letters` list overrides `letter`:

```yaml
letters:
  - ia.iasurvival:letter
  - ia.iasurvival:letter_written_letter
  - ia.iasurvival:letter_open_letter
```

Build with Maven and a JDK compatible with your dependency JARs (JDK 25 for the
pinned TLibs). Spigot API comes from Maven. Install TLibs into Maven using the
[shared installer](../TLibs/README.md). Set `tfmc.rpcharacters` and `tfmc.itemsadder` to their JAR paths,
and `tfmc.builds` to an output directory. Run `mvn package` with these `-D` properties.

Before deployment, verify on a test server with ItemsAdder:

- Left-click the model and solid hitbox in survival and creative: the mailbox stays.
- Sneak-break: the mailbox can be removed, subject to existing region protection.
- Right-click and send sealed and opened letters: pages and delivery stay intact.
- Unrelated items and ordinary books are rejected; other furniture breaks normally.
