> This page is public; linked jars, models and configurations remain in the private server-assets repository and require access. The full ItemsAdder contents archive was removed from server-assets on 2026-09-22; historical lab notes below describe the original snapshot. The existing manifest/materializer may still expect that archive.

# Integration notes from the CachyOS lab

## Match the running server, not legacy dependency filenames

The main TFMC server reported Paper 1.21.10 build 130, ModelEngine R4.1.1,
ProtocolLib 5.4.0 and NBTAPI 2.15.5. The lobby can run a different stack.
The POM's ModelEngine-4.0.8.jar filename is only a build path: the successful lab
build uses the supplied R4.1.1 runtime there. Likewise, compile-time NBTAPI 2.15.0
does not work as the 1.21.10 runtime. Use the private assets manifest's runtime
and build mappings, not whichever similarly named jar appears first.

The public TLibs download lacked the SQLite API needed by VehicleFramework
1.1.12. The supplied TLibs binary includes it. MMOItems build 22 failed against
the supplied MythicLib; MMOItems build 59 with MMOCore build 59 and MythicLib
build 107 enabled successfully. Matching plugin names is insufficient.

## Assets and item definitions are separate dependencies

ModelEngine blueprints, generated client models, MMOItems definitions and
ItemsAdder server item registrations are all needed. A cached resource pack
alone cannot create fuel or track tools on the server. The supplied UTILS item
definitions and custom item-types.yml resolve TLibs's `m.utils.arcane_fuel` and
the other vehicle item paths. The installed train recorder path needed its
`recoder` typo corrected to `recorder`.

The ItemsAdder multipart RAR must be extracted starting at part 1 with both
parts present. The lab installs five rail definitions and preserves their
original custom model IDs to match the cached TFMC pack. The complete contents
archive is retained privately for later integrations.

The cached TFMC ZIP has unusual local entry names: Java ZipFile can read it,
but Python's normal ZIP extraction rejects some entries. Preserve its bytes.
The local generated ModelEngine pack takes priority over the cached TFMC pack.
The separate fishingboat model still has no supplied vehicle configuration.

## Protocol bots need explicit mounted input handling

Minecraft 1.21.10 uses `player_input` flags. The lab sends them explicitly for
vehicle controls, with bounded holds and a reset. Holding backward after braking
can enter reverse; releasing all keys does not necessarily zero the throttle.
The car starts through forward input rather than a separate ignition command.

Mineflayer's physics tick waits and look-before-interaction helpers can stall
while mounted. Use bounded wall-clock waits for this harness and direct protocol
interaction packets; send `use_item` for mounted reload. The latest controller
also sends `tick_end` for ModelEngine's client-tick synchronisation. Sneaking
must be represented in entity-interaction packets as well as player input.
Serialise passenger IDs, not entire entity objects, to avoid circular JSON.

Measure the vehicle base's displacement independently of the bot's cached
mounted position. Confirm models and UI in the full Minecraft client. A bot
connection smoke test is not a vehicle control or rendering test.

## Separate fresh-vehicle success from restored-state failures

Fresh car, rail, train and artillery tests passed. Older/restored instances
showed missing live model/seat state and incorrect train following. The supplied
car model does contain its referenced sound and ground-probe bones. That does
not establish the lifecycle defect's exact cause; retain both failing and fresh
control evidence before changing model-loading or persistence code.

For damage checks, clear earlier fire/cloud effects and establish stable target
health immediately before firing. The final controlled cannon shot changed an
iron golem's health from 100 to 72, matching the configured 28 damage.

See TEST-RESULTS.md for the tested commit, runtime evidence and remaining limits.
