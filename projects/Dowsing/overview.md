# Behavior, configuration, and operations

[Dowsing documentation](README.md) · [All projects](../../README.md)

## System model

Dowsing assigns discoverable resources to chunks and turns configured
ItemsAdder furniture into production nodes. A node has a block definition, an
active type, a level, and one production method for each slot. SimpleFactions
guilds own ordinary nodes; special nodes begin unclaimed and may apply
additional title or tier restrictions.

Active nodes periodically consume configured inputs and produce configured
drops. Natural chunk yield, upgrades, guild membership, and selected production
methods can alter the cycle time, output, efficiency, prestige, wealth, and
upkeep calculations.

## Configuration files

The plugin copies its defaults into `plugins/Dowsing/` on first start.

| File | Purpose |
| --- | --- |
| `config.yml` | Dowsing item, cycle length, guild capacity, natural-yield switch, capacity price, membership requirements, and efficiency tuning. |
| `blocks.yml` | Furniture identifiers, available node types, break/transfer policy, special-node behavior, tier, and optional title requirement. |
| `types.yml` | Node timers, resource class, natural-yield effects, slots, levels, upgrade costs, effects, drops, and biome filters. |
| `slots.yml` | Inventory slot positions and the ordered production methods offered by each slot. |
| `production_methods.yml` | Menu presentation, selection weight, prerequisites, input costs, and production effects. |

Cross-file identifiers must resolve in this order: block definitions reference
types, types reference slots, and slots reference production methods. Item paths
use the prefixes understood by TLibs and the installed item providers.

Run `/dowsing reload` after editing these files. Reloading temporarily caches
the live nodes, reloads all definitions, restores the cached state, and
recalculates faction node benefits.

## Natural resources

When `enable-natural-yields` is true, a player can right-click while holding
the MMOItems item configured by `dowsing_item`. The plugin reports the current
chunk's configured resource and yield, or reports that nothing was found.

Administrators with `dowsing.admin` can manage resource entries:

| Command | Effect |
| --- | --- |
| `/dowsing createresource <id> <resource> <yield>` | Save an entry for the player's current chunk under `Resources/<id>.txt`. |
| `/dowsing deleteresource <id>` | Delete the matching resource entry. |
| `/dowsing reload` | Reload configuration and recalculate node benefits. |

Resource identifiers become filenames, while the resource and numeric yield are
stored as the entry value. Treat identifiers as trusted administrator input.

## Ownership and faction effects

Guild ownership controls access, transfer, capacity, and production. Capacity
starts with the plugin's base allowance and can be influenced by membership and
purchased upgrades. Active nodes publish their configured prestige and wealth
modifiers to SimpleFactions, and the ledger queries Dowsing for each guild's
total node upkeep.

The node menus expose type, production-method, upgrade, transfer, activation,
and deletion actions when the node definition and player permissions allow
them. Inputs are read from the node inventory and outputs are dropped at the
node.

## Persistence and shutdown

- Resource assignments are individual text files under
  `plugins/Dowsing/Resources/`.
- Nodes are individual JSON files under `plugins/Dowsing/Nodes/`.
- Purchased guild capacity is stored in
  `plugins/Dowsing/guild_capacity.json`.

On a normal plugin disable, Dowsing rewrites the node JSON files and saves guild
capacity. Back up the complete `plugins/Dowsing/` directory before changing
identifiers or migrating configuration, and stop the server cleanly before
copying live state.

## Validation

For a server-side change, verify the following on Paper 1.21.10 with the pinned
dependency set:

1. Start with both an empty data directory and a copy of representative existing
   node data.
2. Confirm all definitions load without unresolved type, slot, production, item,
   or Magic artifact paths.
3. Discover a configured chunk resource with the dowsing item.
4. Place, claim, configure, activate, transfer, and remove representative
   ordinary and special nodes.
5. Exercise production inputs, outputs, level upgrades, natural-yield effects,
   capacity limits, prestige, wealth, and ledger upkeep.
6. Restart cleanly and confirm node ownership, selections, progress, efficiency,
   and purchased capacity are restored.
