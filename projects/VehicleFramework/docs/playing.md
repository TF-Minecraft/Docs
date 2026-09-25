# Playing, commands, and upkeep

VehicleFramework adds modeled vehicles to a Paper server. Players right-click a vehicle to board it. Owners fuel it, repair it, and decide who else can ride. Admins spawn vehicles and lay train track.

This page covers a running server. Model bones are in [Models](models.md). YAML for a new vehicle is in [Configuration](configuration.md).

## Requirements

The plugin targets **Minecraft 1.21.10** and **Java 21**. `plugin.yml` requires these plugins:

- ModelEngine
- ProtocolLib
- TLibs
- NBTAPI

MythicMobs and CoreProtect are optional. MythicMobs is used only when `mythicmob` in `config.yml` names a mob. CoreProtect is used when it is installed, so block changes from vehicle explosions can be logged.

The plugin declares Folia support.

Item paths in the shipped configs use TLibs. `v.` is a vanilla item, `m.` is an MMOItems item, and `ia.` is an ItemsAdder item. Point those paths at items that exist on your server.

## Files

On first start the plugin creates `plugins/VehicleFramework/` and copies these files if they are missing:

- `config.yml`
- `fuel.yml`
- `trains.yml`
- `templates/armor/`, `templates/roles/`, `templates/death/`, and `templates/weapons/`

It also creates empty `vehicles/` and `ammunition/` folders, plus `data/` for the save database and track files. It does not overwrite a file that is already there, and it does not copy the example vehicles. Copy the vehicle and ammunition YAML you want from [`src/main/resources`](https://github.com/TF-Minecraft/VehicleFramework/tree/main/src/main/resources) into those folders, then run `/vf reload`.

Live vehicles are stored in `data/vehicles.db`. They load when a player is near and unload past `despawn-distance` (default 160 blocks).

## Commands

| Command | Who | What it does |
| --- | --- | --- |
| `/vf keybinds` | Anyone in a vehicle | Lists the keys for the current state |
| `/vf findvehicles` | Any player | Lists vehicles you own and where they are |
| `/vf spawn <id>` | `vehicleframework.spawn` or `vf.admin` | Spawns that vehicle id at your feet |
| `/vf ammo` | `vehicleframework.spawn` or `vf.admin` | Gives a stack of every loaded ammunition item |
| `/vf kill <radius>` | `vehicleframework.spawn` or `vf.admin` | Removes vehicles inside that radius |
| `/vf takeover` | `vf.admin` | Your next right-click claims that vehicle |
| `/vf reload` | `vf.admin` | Reloads configs, templates, vehicles, ammunition, and track data |
| `/vf track ...` | `vf.admin` | Track tools. See [Trains](using-trains.md) |

`/vf spawn gunboat` uses the root key in the vehicle file, not the display name.

## Boarding

Right-click the vehicle with an empty hand to open the seat menu. The menu is 27 slots. One slot opens ownership settings for the owner, and one slot leaves the seat, so keep the seat list short enough to fit.

Seat types:

| Type | Who uses it |
| --- | --- |
| `captain` | Drives. State keybinds apply here. |
| `gunner` | A seat meant for a weapon. The weapon still binds by bone name, so a `passenger` seat can fire too. |
| `mechanic` | Can repair while seated, including while the vehicle is moving. |
| `passenger` | Rides. |
| `entity` | Holds a mob from `entity-seat-whitelist`. |
| `harness` | Horse, donkey, or mule hitch point. |
| `towing` | Created by the towing block, not listed under `seats`. |

The first player to use an unowned vehicle becomes the owner. `/vf findvehicles` lists what you own.

From the seat menu, the owner can open ownership settings:

- Turn the whitelist on or off.
- Add a player by typing their name in chat (`cancel` aborts).
- Remove someone from the whitelist.
- Drop ownership.
- Turn tickets on or off for this vehicle. On a train, tickets follow the locomotive.

`allow-whitelist` and `whitelisted-by-default` in `config.yml` control whether new vehicles start with a whitelist. When the whitelist is on, other players need to be listed before the seat menu opens.

Tickets use `ticket-item` (paper in the shipped config). The owner, or someone with `vf.admin`, right-clicks the vehicle with a blank ticket item while tickets are enabled. That writes a ticket for this vehicle. While tickets are on, a passenger seat requires that ticket unless the player is the owner or on the whitelist. A matching ticket also opens the seat menu when the whitelist would refuse the player. Captain, gunner, and mechanic seats do not ask for a ticket once the menu is open.

## Items in the main hand

These paths are in `config.yml`. Change them to items on your server.

| Config key | Shipped path | Right-click does |
| --- | --- | --- |
| `repair-item` | `m.utils.vehicle_repair` | Opens the repair menu |
| `skin-item` | `m.utils.vehicle_skin` | Opens the skin menu |
| `destroy-item` | `v.blaze_rod` | Deletes the vehicle |
| `ticket-item` | `v.paper` | Mints a ticket when tickets are enabled |

A name tag prompts for a new name in chat.

A fuel item fills the tank. The fuel's `item` path must match the item, and the engine's `fuel` id must match the fuel entry. Refueling is refused outside the engine's `refuel-states`, and while the throttle is not zero, unless that fuel sets `refuel-while-running: true`.

Repair from outside the vehicle only works on the ground, or while floating, and only when the vehicle is nearly stopped. A player in a mechanic seat can repair while it is moving. You cannot repair a vehicle that is flying unless you are in a mechanic seat.

## Towing and animals

Sneak and right-click a vehicle marked `towable: true` to select it, then sneak and right-click a vehicle that has a `towing` block to attach it. Sneak and right-click the tower again to release.

Sneak and right-click works the same way for train cars. See [Trains](using-trains.md).

Right-click a harness vehicle while leading a horse, donkey, or mule to hitch it. Right-click with a lead to unhitch.

## What players see while driving

`/vf keybinds` prints the keys for the state the vehicle is in (`ground`, `floating`, or `flying`). Those keys come from that state's `keybinds` block. Weapon seats use the weapon's own keybinds instead.

Looping animations such as `forward` and `engine_active` play from the current state. Death plays the animation that matches the death type (`explode`, `sink`, `crash`, or `die`).
