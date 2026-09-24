# Named reward pools

Configuration changes can be applied with `/activity reload`.

Example (replace the sample rewards with your own):

```yaml
rewards:
  multiplier: 1
  drops:
    drop_1: pool_prologue
    drop_2: pool_prologue
    drop_3: pool_end
  pools:
    pool_prologue:
      - weight: 65
        display: "#50d990x2 #7f7d80Ignitium"
        items:
          - item: m.materials.ignitium
            amount: 2
    pool_end:
      - weight: 1
        display: "Netherite Ingot"
        items:
          - item: NETHERITE_INGOT
            amount: 1

daily-reward:
  groups:
    vip: pool_end
    default: pool_prologue
```

Groups use the existing `group.<name>` permissions, with the first matching group
winning. Daily rewards draw once; milestone rewards draw `multiplier` times.
`drop_N` selects the Nth configured milestone, so only define drops that exist.

Named pools use the `pool_` prefix and are case-insensitive. Lists directly under
`rewards.pool_prologue`, etc. also work; definitions under `rewards.pools` take
precedence. The default `pool` uses `rewards.pool`. Missing or empty
pools pay nothing, warn, and leave the claim available. An omitted default pool
does not inherit the example rewards bundled inside the jar. If a claim spans
several milestones and any required pool is empty, fix it before claiming.

# Universal feed

`activities.animal_universal_feed` has no `station:`; it counts feed collected
from a full Cooking trough, which Cooking reports as `DishCookedEvent` with
method `trough`.
