# Prosthetic fuel

## Purpose

Fuel burn, refuel, and powered/depowered transitions for arcane prosthetics.

## Burn tick

- `ProstheticFuelService` runs on the healing tick interval
- For each online active character with fueled prosthetic:
  - Every `burn-interval` from fuel template, subtract `burn-rate` from `trait-state.fuel`
  - Clamp to 0
  - On cross 0: `character.update()` + integrator refresh (depowered)
  - On refuel cross > 0: powered refresh

## Refuel

`ProstheticRefuelListener`:

- Right click with fuel template item while holding/using prosthetic context:
  - Match `FuelTemplateLoader.resolveForItem`
  - Prosthetic must reference that template
  - Add `amount-per-item`, clamp to capacity
  - Consume one item from hand
  - Message: fuel current/capacity
  - Sound (bucket fill style, match VehicleFramework)

**Interact priority:** distinguish refuel (fuel item) vs install (blaze rod) by item path.

## Powered / depowered

- Same trait id throughout
- `TraitEffectResolver` resolves the powered or depowered block for name, lore, modifiers, potions
- Inventory trait list shows depowered name when empty

## Creator

- Arcane prosthetic from creator starts `fuel = capacity`
- Stage info + trait lore disclaimer (no em dashes): e.g. "Requires arcane fuel to stay powered."

## Acceptance

- [ ] 50 fuel, burn 1/hour, online active only
- [ ] At 0 fuel, depowered modifiers apply
- [ ] Refuel with `m.miscellanea.arcane_fuel` adds 50 up to cap
- [ ] Offline does not burn fuel

## Implementation

- `FuelTemplateLoader.resolveForItem(ItemStack)` for held-item matching
- `ProstheticFuelService` proportional burn tick (1m cadence, online active only), integrator refresh on powered/depowered cross
- `ProstheticRefuelListener` refuels matching prosthetics, consumes one fuel item, bucket fill sound
- Registered before `ProstheticInstallListener` in `RPCharacters`
