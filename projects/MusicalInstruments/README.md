# MusicalInstruments

[Source repository](https://github.com/TF-Minecraft/MusicalInstruments) · [All projects](../../README.md)

Technical documentation is maintained here. Run commands from the source checkout unless a guide says otherwise.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

- [Project overview](overview.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.

## Playback events

MusicalInstruments emits `net.tfminecraft.musicalinstruments.events.InstrumentPlayEvent` after playing a configured note.
Listeners can read `getPlayer()`, `getInstrument()` and `getSoundKey()`. The event
is informational and is not cancellable. It is emitted before the note particle
and hotbar reset, only when an instrument and sound mapping have been found.

Maven consumers declare `net.tfminecraft.musicalinstruments:musicalinstruments`
with `provided` scope and use the shared installer.
