# Spiders - Behaviour, commands and tools

Spiders draws procedurally animated Cinderweaver spiders and mimics with
vanilla display entities. Spiders are staff-operated test entities: they have no
health, loot, eggs, nests or hostile AI, and pounces and hits do no damage.

## Access

Only **`tfmc.spider.staff`** grants access to every `/spider` command and tool
(default: server operators). The
permission is checked on commands, use of copied or borrowed tools, held-item
steering, saddle interactions and actual mounting. Riders lose control and
dismount when the permission is removed. Granting access to other staff is a
server policy choice; operators need no permission-manager changes.

Hitting a spider (see [Getting hit](#getting-hit)) is open to everyone.

## Spawning and sizes

```text
/spider spawn hatchling|hunter|broodmother
/spider spawn <scale>
/spider spawn hunter at <world> <x> <y> <z>
/spider scale <scale>
/spider list
/spider remove [<id>|all]
```

Aim at a solid surface within 32 blocks when spawning. The console and staff can
spawn at coordinates in an already loaded chunk. Hatchling, hunter and
broodmother scales are 0.35, 0.8 and 1.5; any scale from 0.25 to 2.5 is
accepted, and `/spider scale` resizes a spawned spider within the same range. Up
to six spiders may be active at once.

Commands that act on one spider use the spider linked to the Summoning Seal in
the sender's hand, otherwise the nearest spider in the sender's world. Console
commands act on the first spider, so run console scripts with no other spiders
active.

## Movement

**Walls and ceilings.** `/spider climb on` (or the Clinging Charm) lets the
targeted spider walk up walls, across ceilings and over ledges; `/spider climb off`
lets it drop back to the floor. Aiming `/spider spawn` or the Summoning Seal at a
wall or ceiling spawns the spider clinging to that face with climbing already on.
Climbing applies to both gaits.

**Gait.** `/spider gait gallop` or `/spider gait walk` (or the Hunting Instinct
tool) switches the targeted spider's gait. A rider can also hold the sprint key
while moving to gallop, returning to a walk when they let go.

**Speed.** `/spider speed gallop <blocks/s>` and `/spider speed walk <blocks/s>`
set the targeted spider's top speed (0.5–20); without a number they show the
current speed. Strides lengthen with speed so the legs keep up. Very small
spiders fall short of the higher settings.

## Pounce

```text
/spider pounce <player> [blocks/s]
/spider pounce at <x> <y> <z> [blocks/s]
/spider pounce stop
```

The targeted spider gallops at the player and leaps the last few blocks, landing
on them. The optional number sets the gallop speed first. The sender is told
where it landed, or why it gave up: the player left, logged off, went into
spectator, moved more than 96 blocks away, or 20 seconds passed. `pounce at`
targets a spot in the spider's world instead, for staged scenes or console use.
A climbing spider pounces along its wall or ceiling and drops onto a player
below. Tune the leap with
`/spider options spider_options.pounce.leapRange|leapBoost|leapLift|giveUpTicks`.

## Getting hit

Anyone can hit a spider, staff or not, and so can mobs and dispensers. Arrows,
spectral arrows and tridents strike its actual body and legs and bounce off;
snowballs and eggs break on it; wind charges burst on it. Players can also hit it
by swinging at it within their reach. Each hit pushes the spider, plays its hurt
sound and breaks its shroud. From weakest to strongest: snowball or egg, arrow,
sword or fist (scaled by attack charge), trident, wind charge. A barely drawn bow
or a spammed swing only glances off. Projectiles pass through the hidden saddle
seat, and hitting the seat counts as hitting the spider. A rider's own shots and
swings pass through their mount.

## Shroud

The Shroud Charm or `/spider shroud on|off` shrouds the targeted spider. The
shroud copies whatever lies behind each part of the spider as seen by the nearest
player within 48 blocks (spectators excluded), including water and lava
surfaces. With nobody near, it copies the ground below. It uses blocks at their
true colour, lit like the world around them. The older dimmed matching, which
looks washed out with bright gamma, is available with
`/spider options spider_options.cloak.allowCustomBrightness set true`.

## Mimic

```text
/spider mimic place
/spider spawn mimic
/spider mimic wake
/spider mimic sleep
/spider mimic place|wake at <world> <x> <y> <z>
```

`/spider mimic place` (or `/spider spawn mimic`) puts a dormant mimic on the
floor the sender aims at, facing them. A dormant mimic is a real chest block
tagged `tfmcspiders:mimic` in its block entity data, so it looks exactly like a
chest and survives restarts. It can't be opened, emptied by hoppers or blown up,
and only staff can break it (in creative mode, to remove it).

Anyone who right-clicks or hits it wakes it. The chest bursts open with a double,
full-volume screech that every player within 80 blocks hears from its direction,
rises on four long legs, turns its back on whoever woke it and gallops away at
7 blocks/s, lid flapping. It keeps running directly away from that player (around
obstacles if it gets stuck) until it is 250 blocks from them, then sits back down
as a chest. The plugin keeps the chunks it runs through loaded, but it stops
early rather than enter terrain that has never been generated. Anything hoppered
or stuffed inside is spat out.

Woken by the console, with no player to flee, it stays put and settles back into
a chest after 20 idle seconds. `wake` and `sleep` do the same by command; the
console uses the `at <world> <x> <y> <z>` forms. Awake mimics count towards the
six-creature limit and take the usual staff steering, gait and pounce commands;
they stay chest-sized and don't climb. A mimic that is awake when the server
stops drops back into a chest where it stands.

## Tools and riding

`/spider tools` opens a menu listing every staff tool with what it does and how
to use it. Clicking a tool's button gives a fresh one and keeps the menu open;
each tool carries the same instructions in its lore. Right-click the Summoning
Seal to create or recall its linked spider. Hold the Brood Guide (a redstone
torch) and aim at terrain to guide the spiders; no marker is drawn where it
points unless `/spider options global.showLaser set true`. Hold the Broodcall
Whistle to call them.

A tool works only if it is the exact item the menu handed out: its tag *and*
item type must match, so an ordinary green dye, torch or carrot on a stick does
nothing. Tools never do their vanilla job either: the guide can't be placed,
charms don't dye signs or sheep, and the whistle doesn't steer pigs. Arrow Brood
Guides from older builds no longer work; take fresh tools. Spiders follow the nearest
staff beacon in the same world, using the upstream steering system. The other
tools inspect joints, switch gait or wall climbing, or show the animation debug
view.

A saddle on a spider's hidden seat lets staff mount it and drive with the
movement keys; sneak to dismount. On a wall or ceiling the rider steers by
looking: forward is the look direction flattened onto the surface.

Seals that still contain a clockwork Cinderweaver from older builds receive the
organic appearance and sounds while keeping their scale and edited leg rig. Take
fresh tools from `/spider tools` for the current names and item appearances.

## Rendering and persistence

All visuals are vanilla display entities. Cinderweavers need no resource pack,
client mod or other plugin. Awake mimics draw the vanilla chest and its planks
through the item-model pack in the source repository's `resourcepack/` folder:
copy its `assets/` into the server's `ItemsAdder/contents/tfmc_spiders/resourcepack/`
and run `iazip` (any server pack works), or awake mimics show missing models.
`tfmc_spiders:mimic_chest` is the vanilla `minecraft:chest` special model, whose
first custom model data float picks the lid openness (0 to 1 in 40 steps);
`tfmc_spiders:mimic_wood` is a cube of the chest plank texture for the legs. The
renderer tags its entities with `tfmc_spider_render`.
Removing a spider or stopping the server cleans up its displays and seats, and
spiders do not survive a restart; dormant mimics do.

This is experimental multiplayer software. Test movement and client performance
with a few spiders before raising any limits.

## Options and debugging

```text
/spider options <group.path>
/spider options <group.path> set <value>
/spider options <group.path> reset
/spider splay [delay]
/spider fall <height>
/spider items
```

`/spider options` reads, sets or resets an option by path, with tab completion
for paths and values. The `spider_options` group holds the targeted spider's
gait, body, pounce, cloak and debug options; `global` holds plugin-wide settings.
`splay` plays the upstream splay animation, `fall` (a debug command) moves the
spider up by the given height, and `items` opens the inventory of every plugin
item.
