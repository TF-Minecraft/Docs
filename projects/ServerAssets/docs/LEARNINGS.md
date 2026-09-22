# Test lab integration notes

## Dependency selection

Build TFMC plugins from `main` using the versions in their POMs and the
[shared installer](../../../PIPELINES.md#build-dependencies). Use the private
asset manifest and checksum files for third-party binaries. Inspect embedded
plugin versions: a build alias such as `ModelEngine-4.0.8.jar` can select a
different runtime version. Validate the whole plugin set together.

## Assets and item definitions

ModelEngine blueprints, generated client models, MMOItems definitions and
ItemsAdder item registrations are separate inputs. A cached resource pack alone
cannot create server-side fuel or track tools. Check UTILS item definitions and
`item-types.yml` for `m.utils.arcane_fuel` and `m.utils.train_track_recorder`.

Preserve the ItemsAdder rail definitions' model IDs to match the cached TFMC
pack. The repository contains the rail subset. Keep the cached pack's bytes
intact: its unusual ZIP entry names are rejected by some extraction tools.
Select the generated ModelEngine pack above it in the client.

## Mounted protocol input

Protocol harnesses need explicit `player_input` flags, bounded holds and a reset.
Holding backward after braking can enter reverse; releasing keys does not
necessarily zero the throttle. Mineflayer's physics-tick waits and
look-before-interaction helpers can stall while mounted. Use bounded waits and
direct interaction packets where needed; mounted reload uses `use_item`.

Send `tick_end` for ModelEngine client-tick synchronisation. Represent sneaking
in interaction packets as well as input flags. Serialize passenger IDs rather
than whole entity objects. Inspect current entity IDs on every run.

Measure the vehicle base's displacement separately from the bot's cached mounted
position. Confirm models and UI in the full Minecraft client.

## Persistence and damage checks

Compare fresh vehicles with vehicles restored after unload or restart. If seats,
models or train following differ, retain both cases as evidence before changing
persistence or model-loading code.

For damage checks, clear fire/cloud effects and establish stable target health
immediately before firing. Compare the observed change with the configured damage.
See the [lab validation checklist](LAB.md#validation).
