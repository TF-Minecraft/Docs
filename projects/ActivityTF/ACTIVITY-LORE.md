# Activity descriptions

[ActivityTF](README.md) · [All projects](../../README.md)

Activity `description` lines support three local placeholders:

| Placeholder | Config value | Meaning |
| --- | --- | --- |
| `%every%` | `every` | Count required for one completion/award |
| `%points%` | `points` | Points earned per completion |
| `%daily-cap%` | `daily-cap` | Maximum awards per day; zero means uncapped |

Values come from the loaded activity definition whenever the GUI renders.
After changing settings, reload ActivityTF and reopen the menu. Single strings
and lists both work; colours and unknown placeholders retain their existing
behaviour. These placeholders do not require PlaceholderAPI.

`every` uses the tracked activity's unit: minutes for playtime, Denar for market
sales/card profit, XP for professions, output items for vanilla crafting,
and completed recipes for MMOItems stations. Station output stack sizes do
not affect credit. Configured `station-actions` aliases retain their credit
amounts (for example, the bulk Coal recipe counts as 16 standard crafts).

The daily cap limits awards, not raw actions or points. The shared daily bar,
voting share and weekly bar may limit the points actually credited further.
Tasks must be revealed before their actions count.

## Existing server configs

The plugin does not overwrite existing descriptions. To prepare the audited
wording for an existing config, install PyYAML and run
[`tools/update-activity-descriptions.py`](https://github.com/TF-Minecraft/ActivityTF/blob/main/tools/update-activity-descriptions.py)
from the source checkout:

```sh
python3 tools/update-activity-descriptions.py config.yml config-updated.yml
```

Review the resulting diff before deployment. This writes a separate file and
changes only active activity descriptions, preserving commented-out activities,
other settings, rewards and state. It refuses unknown activity types rather
than inventing instructions. Rerunning it is safe, but replaces custom active
descriptions with the audited templates. Its tests run with
`python3 -m unittest discover -s tools -p 'test_*.py'`; CI does not run them.

## What Main's activities count

The audited templates describe Main's 37 active activities, checked on 2026-09-30
against their event handlers and the live MMOItems recipes. Commented-out
activities are not covered. Recheck this table when activities or recipes change.

| Activities | Correct explanation/unit |
| --- | --- |
| vote | Real votes; `/vote` links remain |
| playtime | Active minutes; idle minutes excluded when AFK checks are enabled |
| geiger | Collect the source with a Trace Detector; finding it alone does not count |
| archaeology_find | Recover finds, rather than merely start/finish a project |
| instrument | Notes played |
| market_sale | Denar earned, per award |
| casino_win | Positive card-game profit above stake before tax |
| ic_chat | Substantial in-character messages; short/repetitive/OOC chat excluded |
| injured | Receive an injury as the target, rather than injure someone else |
| vehicle_build | Finished vehicles at construction stations |
| battle_joined | Participation credited when a faction battle ends |
| advcraft_item | Completed Advanced Crafting items or alloys; five per award, two awards/day |
| cook_dish | Finished dishes at pots/stations/boards; trough feed is separate |
| profession_upgrade | Purchased profession upgrades |
| profession_crafter, profession_forager, profession_herborist | Profession XP |
| ingot_flint, ingot_coal | Standard recipe crafts at a Blast Furnace; bulk Coal aliases still count |
| tool_iron_pickaxe, tool_iron_axe, tool_iron_hoe, tool_iron_shovel | Named recipe crafts at a Crafting Table |
| forester_arrow, forester_oak_log, forester_spruce_log | Named recipe crafts at a Fletching Table |
| alchemy_coal, alchemy_powder | Named recipe crafts at a Brewing Stand |
| instrument_lute | Lute recipe crafts at a Jukebox |
| research_scribe_paper | Unknown Research Paper recipe crafts at a Cartography Table |
| medicine_herb_mixture, medicine_splint | Willow-Bark Tincture/Splint recipe crafts at a Medicine Station |
| engineer_fuel | Arcane Fuel recipe crafts at an Engineer Station |
| fishing_rod | Basic Fishing Rod recipe only; other rods do not count |
| fishing_iron_hook | Iron Hook recipe crafts at a Fishing Station |
| animal_universal_feed | Collect finished trough feed, with an empty-hand right click |
| animal_llama | Llama Spawn Egg recipe crafts at an Animal Station |

Descriptions count recipe crafts rather than output totals: Flint/Coal produce
four per standard craft, forester recipes produce 64, powder produces two,
tincture/splint produce eight and fuel produces 16. Placeholder craft counts
remain correct if those outputs change.
