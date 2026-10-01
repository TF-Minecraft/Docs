# Recording songs and playing discs

[MusicalInstruments](README.md) adds a recording studio to the live instrument
controls on Paper 1.21.10 / Java 21. Recording captures resolved instrument sample
triggers and their timing. Playback reuses the existing sounds from the server's
resource pack; a new song does not need a new audio file or pack update. Players
must have the samples installed to hear custom instruments.

## Record through the studio interface

Sneak-right-click an empty jukebox to open the 54-slot recording studio. If you
have no project, the studio creates an **Untitled** project automatically. You
can also look at an empty jukebox within five blocks and use `/music studio`.
Stay near that jukebox while using its controls.

1. Click **Song settings** or the song title. Enter a title, adjust the tempo
   slider, choose whether to use the private metronome, and click **Save**.
2. Put an instrument in your off-hand and click a **Track** card. The inventory
   closes so you can play with keys 1-8. Wait for the count-in; recording time
   and the note count then appear above your hotbar.
3. Open the same station again and click **Stop**. Click **Listen to new take**
   to audition it with the other saved tracks, then **Keep take** or **Discard
   take**. Your previous saved take stays intact until you accept its replacement.
4. Repeat for the other tracks. The saved, audible tracks play privately as
   backing while you record; the track being replaced is excluded. Every track
   starts at the same song time, so wait before playing for a later entrance.
5. Use the controls directly below each track to mix it: left-click **Volume**
   to add 25%, right-click to subtract 25%, or shift-click to reset to 100%.
   Volume ranges from 0% to 200%. Click **Audible / Muted** to toggle silence.
   **Listen to saved mix** auditions your changes; **Stop** ends the preview.
6. Put an ordinary music disc in your inventory and click **Prepare a blank
   disc**, then **Publish song**. These controls find discs in your storage
   inventory; you can keep the instrument in your off-hand. If using a stack,
   leave a free inventory slot for the resulting disc. Publication requires
   at least one audible note and no pending take.
7. Insert the published disc into an empty jukebox with an ordinary right-click
   to hear the layered song. To copy it, hold that recorded disc in your off-hand,
   put a blank disc in your inventory, and click **Copy a recorded disc**.

The track cards show saved instruments, duration and note count. Their colors
distinguish empty, saved, recording and pending states. The title card shows
current activity, and the open menu updates as recording and playback progress.
Separate buttons control the saved mix and the pending take. **Tempo** has
quick +/-5 BPM clicks; shift-click opens the settings form. **Metronome** toggles
the recording click. **New song** opens a confirmation before clearing your
editable tracks and pending take; published discs remain valid.

The settings form uses Minecraft's title field, slider and checkbox. It accepts
one response from the player who opened it, expires after two minutes, and checks
the station and project again before saving. Closing a menu does not stop a
recording or preview. The studio prevents item transfers, number-key swaps,
double-click collection and dragging while its inventory is open.

## Record with commands

1. Create your editable project with `/music new Tavern Song`.
2. Hold a configured instrument in your off-hand and run `/music record 1`.
3. Wait for the count-in, then play using the usual hotbar controls.
4. Run `/music stop`. The new take is pending, and the previous saved track is
   preserved. `/music preview take` auditions the pending take with the mix.
5. Use `/music keep` to replace that track, or `/music discard` to retain its
   previous version.
6. Record track 2, 3 or 4 in the same way. During each take, the saved, audible
   tracks play privately for the recording player. The track being replaced is
   excluded from this backing mix. Every track begins at the same song time;
   wait before playing to create a later entrance.
7. Use `/music preview` to hear the saved mix. Adjust gain with
   `/music volume 2 0.5` or toggle silence with `/music mute 2`.
8. Hold one ordinary vanilla music disc in your main hand and run `/music blank`.
   This replaces it with a blank recording disc. Hold that blank and run
   `/music publish` to turn it into a record of the saved mix.

An empty take leaves the previous track intact. A take automatically finishes at
the duration or note limit. Re-recording replaces a whole track after acceptance.
One player owns one editable project. `/music reset confirm` explicitly clears
the editable project, including pending work; published discs remain valid.

## Commands and permissions

All commands are player-only. `/recording` is an alias for `/music`.

| Command | Behavior |
| --- | --- |
| `/music new <title>` | Create a project if none exists. |
| `/music title <title>` | Rename the editable project; maximum 64 ordinary characters. |
| `/music studio` | Open the empty jukebox you are looking at. |
| `/music status` | Show saved tracks, duration, tempo and pending take. |
| `/music record <track>` | Begin a count-in and record a take. |
| `/music stop` | End the current recording or stop the private preview. |
| `/music keep` / `/music discard` | Accept or discard the pending take. |
| `/music preview [take]` | Privately audition the saved mix or pending take with the mix. |
| `/music volume <track> <0-2>` | Set gain; 1 preserves the captured volume. |
| `/music mute <track>` | Toggle a saved track's silence. |
| `/music remove <track>` | Remove a saved track from the project. |
| `/music bpm <40-240>` | Set metronome tempo; recorded timing is preserved. |
| `/music metronome <on\|off>` | Enable or disable the private recording click. |
| `/music blank` | Convert one ordinary music disc into a blank disc. |
| `/music publish` | Replace the held blank disc with a new immutable edition. |
| `/music copy` | Copy the recorded disc in the off-hand onto the blank in the main hand. |
| `/music reset confirm` | Clear the editable project. |
| `/music help` | Display the available commands. |

`instruments.record` grants studio, recording, editing, blank and publication
commands; `instruments.copy` grants copying; `instruments.play` grants insertion
of recorded discs into jukeboxes. All three default to true. Removing a disc does
not require playback permission. Existing `/instruments` permissions are preserved.

## Editions, playback and storage

Publishing requires at least one audible sample and no pending take. Each
publication receives a new UUID and freezes its title, author, tracks, gain and
mute state. Editing or resetting the project does not change existing discs.
Copies reference the same edition and consume a physical blank disc. The command
controls replace a single disc held in the main hand. The menu controls use one
disc from the storage inventory, replacing it in place when it is a single item
or splitting a stack into a free slot. A full inventory can still use a single
disc, and an unsplittable stack is rejected before any edition is written.
Publication writes the edition successfully before replacing the blank.

Right-click an empty jukebox with the recorded disc in either hand. The plugin
inserts one disc, applies the jukebox block state, stops its base vanilla song,
and plays all tracks from the jukebox's center in the `RECORDS` sound category.
Nearby players hear the same shared song clock. A player arriving mid-song hears
future samples; already-started samples are not sought or reconstructed.

Right-click to eject the disc. Removing the item, replacing or breaking the
block, unloading its chunk/world, or disabling the plugin cancels future notes.
After normal completion the disc remains inside and can be ejected and
reinserted. Sessions do not automatically resume after a reload. Ordinary discs
retain their vanilla interactions. Automated hopper insertion of recording and
blank discs is blocked; hopper extraction is allowed.

Sample tails finish naturally when playback or monitoring stops. The plugin
does not issue broad sound-stop packets that could cut off another instrument
or nearby jukebox using the same sound key. Gain affects new triggers, and each
sample's audio file determines its duration. Recording voice, importing audio,
sample trimming, time stretching and sustained note control are outside this
sequencer's controls.

Projects are stored in `plugins/MusicalInstruments/studio/projects/<player-uuid>.yml`;
immutable editions are in `studio/songs/<edition-uuid>.yml`. Back up both with the
world/item data: a disc contains its edition ID, and its music remains in the
server's song file. Keep published editions while discs referencing them exist.
Unknown formats, corrupt files and missing editions are reported rather than
silently overwritten or substituted. Error details appear in the server log.

Projects save after each edit. Active takes produce immutable background
checkpoints and save completely on stop, disconnect and orderly plugin shutdown.
A hard crash can lose work since the last completed checkpoint. Writes use a
temporary file and atomic replacement where supported; final writes wait for
older checkpoints to avoid overwriting accepted work with an earlier take.

## Configuration and timing

`studio.yml` is separate from the existing instrument definitions in `config.yml`.
Restart after editing it; `/instruments reload` reloads instrument mappings only.
Captured notes retain their original sound key, volume and pitch across config
reloads. Replacing sound assets in the resource pack can still change their timbre.

| Setting | Default | Accepted range |
| --- | --- | --- |
| `max-tracks` | 4 | 1-8 |
| `max-duration-seconds` | 180 | 1-600 |
| `max-notes-per-track` | 1500 | 1-12000 |
| `max-notes-per-song` | 6000 | 1-12000 |
| `max-sessions` | 32 | 1-128 combined recordings, previews and jukeboxes |
| `jukebox-radius` | 32 | 1-128 blocks; client sample attenuation still applies |
| `count-in-seconds` | 3 | 1-10 |
| `sample-tail-seconds` | 3 | 0-10 seconds before a normal playback session closes |
| `checkpoint-ticks` | 200 | 20-1200 ticks between background checkpoint attempts |

Settings outside their ranges are clamped. Persisted data also has hard bounds:
8 tracks, 600 seconds and 12000 notes per song, finite gains of 0-2, captured
volumes of 0-16, and pitches of 0.5-2. At most 32 notes per player per tick are
captured. A pending take is validated against the prospective song's note limit.

Capture, overdub monitoring and playback share one main-thread scheduler clock.
Timing has one-tick granularity (50 ms at 20 TPS). Low server TPS slows playback
and the metronome while samples continue running on the client. BPM changes the
metronome only. Existing samples with randomized variants may choose different
variants on replay. No claim of sample-accurate audio mixing is made.

Private previews, backing tracks and jukebox playback do not emit
`InstrumentPlayEvent` or increment live instrument metrics. ActivityTF continues
to count actual player performances, including notes played during recording.
The existing event constructor and accessors remain compatible.

## Validation

Run `mvn clean verify` from MusicalInstruments. Automated tests exercise note
overlap, replacement/acceptance, immutable editions, YAML recovery, checkpoints,
duration bounds, item preservation on storage errors, nearby playback, jukebox
snapshot updates, cancellation, permissions and vanilla interaction preservation.
Menu tests cover deferred clicks, mixing, settings, blocked item transfers, station
distance and permission rechecks. Form edits preserve the latest notes and pending
take; inventory publication preserves items when storage fails or space is missing.
These tests use mocked Bukkit objects and do not verify audible output on a client.

Before deployment, on a Paper 1.21.10 test server with the instrument resource pack:

1. Record two different instruments with overlapping notes, preview the pending
   mix, keep both tracks, and verify their synchronization.
2. Re-record a track, discard it, and confirm the saved version is unchanged.
3. Publish a disc, edit the project, copy the original disc, and check that both
   discs still reproduce the original edition.
4. Insert using each hand, then eject, break the block and unload the chunk while
   playing. Check that exactly one physical disc exists and no new notes follow.
5. Join the listening radius mid-song, use two nearby jukeboxes, and verify that
   stopping one leaves the other's sample tails intact.
6. Stop recording by disconnecting and by orderly restart. Confirm recovery of
   the pending take and playback of previously published discs.
7. Test protected blocks, denied permissions, full inventories, missing edition
   files, vanilla discs and hopper insertion/extraction.
8. Verify ActivityTF only counts performed notes, including recording, and never
   advances from private previews or jukebox playback.
9. Complete a song using only the inventory controls. Check the title form and
   tempo slider on a client, automatic status updates, inventory-based publication,
   full inventories, and the new-song confirmation. Try item drags, number keys,
   bottom-inventory shift-clicks and moving away before using a form response.

This procedure describes required runtime checks, not evidence that a release
has passed them.
