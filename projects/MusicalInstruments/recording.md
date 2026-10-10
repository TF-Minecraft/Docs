# Recording songs and playing discs

[MusicalInstruments](README.md) adds a recording studio to the live instrument
controls on Paper 1.21.10 / Java 21. Recording captures resolved instrument sample
triggers and their timing. Playback reuses the existing sounds from the server's
resource pack; a new song does not need a new audio file or pack update. Players
must have the samples installed to hear custom instruments.

## Record through the studio interface

Staff can open `/music studio` anywhere with `instruments.studio` (default: op),
without looking at a jukebox. Player entry through a dedicated station is pending.
The plugin no longer claims sneak-right-click on jukeboxes, leaving that gesture
available to MMOItems. Ordinary jukebox right-click still inserts/ejects discs.
There is no configurable station identifier or MMOItems station integration yet.

Click an existing song, or **Create a new song** to enter its title and open
its editor. Each project has independent saved tracks, pending take, tempo and
metronome. The library fills its 36 gray slots from slot 9, left to right and
top to bottom, with purple borders above and below. The 36-project limit also
applies to `/music new`. When full, creation asks you to delete an old project.
Right-click a song and confirm its deletion to free a slot. Deleting removes
only that editable project; other songs and published discs remain valid.

1. Click **Project settings** or the song title to open a dedicated 27-slot
   inventory. **Title** opens a text field for renaming. **Tempo** changes BPM
   by +5 on left-click or -5 on right-click; shift-click changes it by 1.
   **Metronome** toggles the recording click. Only the recording player hears it,
   and clicks are never captured in the song. The count-in always plays.
   BPM changes the click rhythm, without retiming existing notes.
2. Put an instrument in your off-hand and click **Record track** in its row.
   The inventory closes so you can play with keys 1-8. Wait for the count-in;
   recording time and note count then appear above your hotbar.
3. Reopen `/music studio`, select the current project and click **Stop recording /
   preview**. Click **Listen to take** in that row to audition it with the other
   saved tracks, then **Keep take** or **Discard take**. The previous saved take
   stays intact until its replacement is accepted.
4. Repeat for other tracks. Saved, audible tracks play privately as backing while
   you record; the track being replaced is excluded. Every track starts at the
   same song time, so wait before playing for a later entrance.
5. Left-click **Volume** to add 25%, right-click to subtract 25%, or shift-click
   to reset to 100%. Volume ranges from 0% to 200%. **Audible / Muted** toggles
   silence; **Listen to track** auditions one saved track. **Listen to full mix**
   auditions the complete song; **Stop recording / preview** ends either preview.
6. Pick up exactly one music disc from your inventory and place it on **Publish
   full song**. Ordinary, blank and already-recorded music discs are accepted.
   No blank-disc preparation is required. A recorded disc needs a second click
   within 10 seconds to confirm overwriting; changing the project or disc requires
   a fresh confirmation. The same material and other item metadata are preserved,
   while its title, lore and edition ID are replaced. The result returns to the
   cursor. Keep or discard pending takes first; the mix must have audible notes.
7. Insert the published disc into an empty jukebox with an ordinary right-click
   to hear the layered song. Copying remains available through `/music copy`, with
   the recorded disc in the off-hand and one blank disc in the main hand.

The editor has six chest rows. Each middle row belongs to one track; recording,
volume and mute occupy columns 2-4, followed directly by saved-track listening
and take listening/keep/discard in columns 5-8. Gray labels mark unavailable take
controls. Projects with more than four tracks have another editor page.
The bottom bar holds full-mix preview, stop, a centered recording guide,
publication and **Project settings**. The top-left arrow returns to the library.
**Clear this project** in settings confirms before clearing only the selected
project's tracks and pending take. Settings contain no blank, publish or copy
controls and no duplicate song-settings form.

Native title fields and deletion/reset confirmations accept one response from
the opening player, expire after two minutes and recheck permissions and project
identity before saving. Physical station sessions also recheck station distance.
Closing a menu does not stop recording or preview. Normal clicks and drags within
the player's inventory are allowed so a disc can be picked up. Menu item transfers,
number-key swaps, double-click collection and bottom-inventory shift-clicks are
blocked. Publication accepts a single-target deposit on its slot, cancels vanilla
movement and writes the edition before replacing the cursor item. Changed cursors,
closed menus, permission revocation and failed writes leave the physical disc intact.

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
One player can own multiple editable projects. Commands operate on the selected
project. `/music new <title>` creates and selects another project; `/music projects`
lists titles and IDs, and `/music open <project-id>` selects one. Changing projects
or creating another song while recording requires stopping the current take
first. Reopening the current project during recording is allowed so the player
can reach Stop. `/music reset confirm` clears only the selected project's editable
tracks and pending work; other projects and published discs remain valid.

## Commands and permissions

All commands are player-only. `/recording` is an alias for `/music`.

| Command | Behavior |
| --- | --- |
| `/music new <title>` | Create and select another project, preserving existing songs. |
| `/music projects` | List this player's project titles and IDs. |
| `/music open <project-id>` | Select one of this player's projects for commands. |
| `/music title <title>` | Rename the editable project; maximum 64 ordinary characters. |
| `/music studio` | Staff: open the project library anywhere, without a physical station. |
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

`instruments.studio` grants command access without a station and defaults to op.
It also requires `instruments.record`. Dedicated player station access is pending.
`instruments.record` grants recording, editing, blank and publication commands; `instruments.copy` grants copying; `instruments.play` grants insertion
of recorded discs into jukeboxes. All three default to true. Removing a disc does
not require playback permission. Existing `/instruments` permissions are preserved.

## Editions, playback and storage

Publishing requires at least one audible sample and no pending take. Each
publication receives a new UUID and freezes its title, author, tracks, gain and
mute state. Editing or resetting the project does not change existing discs.
Copies reference the same edition and consume a physical blank disc. Command
controls replace a single blank disc in the main hand. The publish slot instead
rewrites exactly one music disc on the cursor, preserving its material. Overwriting
one recorded disc creates a new edition; other physical copies still reference
the previous edition. Stacks are rejected before writing an edition. A failed
publication never consumes the input disc.

Right-click an empty jukebox with the recorded disc in either hand. The plugin
removes the vanilla `jukebox_playable` component from a detached single disc
before insertion, applies the jukebox block state, and plays all tracks from the jukebox's center in the `RECORDS` sound category.
Nearby players hear the same shared song clock. A player arriving mid-song hears
future samples; already-started samples are not sought or reconstructed.
New blank/published/copied discs also omit that vanilla component. Previously
issued recording discs are upgraded on insertion without changing their edition,
material or unrelated metadata; they do not need to be recorded again.
Insertion and ejection send a stop event for that jukebox position to clear any
stale vanilla client playback, including after the custom song has finished.

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

Projects are stored in `plugins/MusicalInstruments/studio/projects/<player-uuid>/<project-uuid>.yml`.
The original `studio/projects/<player-uuid>.yml` remains a snapshot of the selected
project. Existing single-song files are read and archived before another project
can replace that selection. The library includes the original song and its pending
take. The selected project survives restarts; immutable editions stay in
`studio/songs/<edition-uuid>.yml`. Back up these directories with the
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

The project library has a fixed 36-project limit, matching its gray slots.
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
Menu tests cover library capacity/deletion, horizontal track controls, track
pagination, inventory settings, staff access without a station, stale selections,
deferred clicks, cursor publication/overwrite confirmation and item preservation
when storage fails. They also check permissions, blocked menu transfers and
station distance rechecks. Form edits preserve the latest notes and pending take.
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
   files, vanilla discs and hopper insertion/extraction. Publish onto several
   vanilla disc types, insert an older recorded disc, and confirm no vanilla
   song starts alongside the custom mix. Eject during and after playback;
   verify the other jukebox remains audible.
8. Verify ActivityTF only counts performed notes, including recording, and never
   advances from private previews or jukebox playback.
9. Create two projects from the library and complete songs using only the inventory controls.
   Switch between projects, restart, and verify each song's tracks and pending take.
   Check the title form, tempo and metronome controls, automatic status updates,
   cursor publication, overwriting a recorded disc, full inventories, the
   36-project cap, delete confirmation and clear-project confirmation. Check track pages 5-8.
   Try item drags, number keys,
   bottom-inventory shift-clicks and moving away before using a form response.

This procedure describes required runtime checks, not evidence that a release
has passed them.
