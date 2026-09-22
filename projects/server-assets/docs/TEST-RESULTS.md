> Canonical documentation: [TF-Minecraft/docs](https://github.com/TF-Minecraft/docs). [Source snapshot](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/docs/TEST-RESULTS.md). Commands and plain-text code/config paths refer to the source repository unless stated otherwise.

> This page is public; linked jars, models and configurations remain in the private server-assets repository and require access. The full ItemsAdder contents archive was removed from server-assets on 2026-09-22; historical lab notes below describe the original snapshot. The existing manifest/materializer may still expect that archive.

# Minecraft lab interactive tests — 2026-09-22

Tested on CachyOS with Paper 1.21.10 build 130, the supplied ModelEngine R4.1.1,
TLibs and MMOItems stack, and VehicleFramework source commit
`bfdb59ba651723200b364b132c0b6969244389ef`. No VehicleFramework Java code was
changed during these checks. The earlier build passed 369 tests; that build was
not repeated for these runtime checks.

## Passing checks

| Check | Evidence |
| --- | --- |
| Car fuel, boarding and driving | Normal Minecraft client consumed one Arcane Fuel, reported 100/500 fuel, opened Select Seat, started the engine, drove, steered and entered reverse. HUD and rendered model captured in `car-seat-menu.png` and `car-driving.png`. |
| Track-layer tool | Actual left/right block interactions created straight rail sections of 64 and 96 blocks, with matching ItemsAdder rail visuals. |
| Fresh train coupling and movement | Shift/right-click selected a coal car and reported `Connected car to train`. Fresh locomotive moved from z=130.5 to 135.8999; coal car moved from z=124.7756 to 130.1755. Both stayed on x=400.5, retained approximately 5.7244 blocks spacing, and stopped after equal forward/backward input. See `train-fresh-consist.png`. |
| Artillery reload and fire | Cannonball inventory count decreased on reload; chat confirmed the ammunition. Space fired the weapon and subsequent empty fire reported `No ammo`. Projectile trail, muzzle sound and impact effects were received by the protocol client. |
| Artillery damage | After clearing prior fire/cloud effects and resetting the isolated target, the console read 100 health before firing and 72 afterward. This matches fixed_artillery's configured 28 projectile damage. See `artillery-impact.png` and `server.log` at 13:44:34–13:44:35 (server-local time). |
| Full client rendering | The isolated Minecraft 1.21.10 client displayed textured cars, artillery, a seated driver, a coupled train and the rail resource-pack assets. |

## Failed check: restored vehicle state

Some older/restored vehicles did not retain usable live ModelEngine state. An
older car could open the seat menu but had no visible seat/model entities;
starting it threw `NoSuchElementException` at `CustomEffect.sound:130` when
resolving its sound bone. The supplied small_car blueprint contains that bone.

An older locomotive successfully coupled a fresh coal car, but moving the
locomotive from z=145.1 to 150.5 moved that car only from z=124.4732 to 124.4786.
The fresh train control on a separate track passed. This establishes a runtime
failure associated with the older/restored instances, not its exact cause.
The setup is usable for fresh-vehicle testing; restoration is not signed off.
No workaround was hidden in the supplied vehicle configs or Java source.

## Reproduction and artifacts

Lab root: `/home/ryan/.local/share/blightfront-test-runner/vehicleframework/`.
Raw evidence is under `artifacts/e2e/`; `events.jsonl` records protocol actions,
chat, sampled entities and the final weapon packet capture. Node timestamps are
UTC; server log timestamps use the PC's local timezone.

The bot controller is `run/e2e-controller.cjs`; the bounded, isolated graphical
client helper is `run/e2e-visual.py`. Both passed syntax checks. Early bot attempts
in the raw log include harness failures: mounted Mineflayer tick/look waits,
circular passenger serialization, and incomplete sneak/tick-end handling. The
controller was corrected before the final fresh train and controlled weapon
checks. Those earlier attempts are retained, not counted as passing evidence.

Test locations: original rail x=100, z=100–164; fresh passing rail x=400,
z=100–196; fresh artillery near (600, -60, 200), impact platform near z=224.
The normal client drove a fresh small_car from the area near (300, -60, 300).
Test vehicles, tracks and impact scenery remain in this disposable world.

The bot was deopped and disconnected, the test graphical client was closed,
and the server was left running with its existing four-hour lifetime. Use
`Play Minecraft.desktop` or `./bin/lab play` to reopen the isolated client.
VehicleTester was returned to creative mode near the fresh train.
