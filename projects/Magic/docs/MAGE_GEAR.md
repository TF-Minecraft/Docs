# Mage gear

Magic owns mage-weapon assembly, enchanted charges, station orb runs, weapon
resonance requirements, Rift and revision refresh. The implementation is in
[the gear package](https://github.com/TF-Minecraft/Magic/tree/main/src/main/java/net/tfminecraft/magic/gear).

## Configuration

| File | Purpose |
| --- | --- |
| `charges.yml` | Charge item paths and aura caps by item tier |
| `gear/archetypes.yml` | Weapon templates, melee behavior and socket groups |
| `gear/part-types.yml` | Part categories |
| `gear/parts.yml` | Part compatibility, costs and socket contributions |
| `gear/socket-colours.yml` | Socket colour prefixes by resonance band |
| `gear/orbs.yml` | Hitscan, orbit, capture, Rift and difficulty settings |
| `skills.yml` | Skill-to-element bindings used for cast checks |
| `config.yml` | Station and alignment settings |

Archetypes include staff, wand and sword. Selected parts determine socket count,
clamped to four. MMOItems supplies templates, gemstones and skill combinations;
TLibs supplies socket groups.

## Charges and station use

Charges implement the shared aura-vessel interface. They gather aura through
eligible shrine, sacrifice and admin-fill paths, and display element tier bands.
They are excluded from meditation and artifact care/muffle handling.

1. Right-click an empty station and select an archetype and its parts.
2. Confirm assembly. Materials are consumed and the prepared weapon stays on the
   station, with its provenance and state persisted.
3. Apply a filled charge. Blank charges and concurrent runs are refused. A charge
   above the player's resonance band requires confirmation.
4. Hit the station's good orbs and avoid bad ones. The charge is consumed when
   the run begins; the captured result is written when the run ends.
5. Sneak-right-click with an empty hand to eject the weapon. Ejection is blocked
   while a run is active.

The station does not need to be at a shrine. Difficulty uses the charge item's
tier, not its displayed aura band. A disconnect or shutdown finishes with the
captured result rather than refunding the charge.

## Orb results and weapon state

Capture is clamped to 0–1 from good hits divided by the tier's `good_target`,
minus missed-good-orb penalties. Bad hits add Rift up to its configured cap.
A later recharge can reduce existing Rift once per completed run.

Weapon requirements are stored per element. Applying captured aura uses the
higher of the existing and incoming requirement; values do not add. A new element
adds its own requirement. The first charge selects socket colours from the
captured band. Requirements display as tier bands.

## Cast checks

Checks use held mage gear, preferring the main hand and otherwise the offhand.
For a skill bound to an element:

- Missing weapon requirement or insufficient player resonance refuses the cast
  before mana and cooldown are spent.
- After that check, a cast wears the weapon. Rift rolls a flat fumble chance;
  holding more than one staff forces an overload fumble. A fumble spends mana
  and cooldown and cancels the spell.
- Alignment is a configurable bonus derived from the weapon's band. It is
  synchronized when held gear or the relevant resonance changes.

Armor does not gate spells. Skills cast without mage gear retain their normal
behavior. Refusal and alignment derive from live session and weapon state.

## Refresh and recycling

Provenance records parts and revisions. Refresh reconciles socket layouts while
preserving applied runes. A rune that no longer fits marks the weapon broken;
its data is retained for reclamation. Disable configured IDs instead of deleting
them from persisted item definitions.

The Recycler provider returns configured part materials and discards weapon
resonance. Check refresh and reclamation after changing parts or archetypes.

## Validation

Use the exact source and dependency set intended for release. Check station
persistence, material consumption, blank/over-tier charge handling, ejection
locks, perfect and missed orb runs, multi-element highest-only merging, Rift
at 0 and 100, refusal without cost, alignment resync, rune preservation and
recycling. Record results with the run or PR.
