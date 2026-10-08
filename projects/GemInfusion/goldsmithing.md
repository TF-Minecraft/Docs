# Goldsmithing and finishing rules

[GemInfusion documentation](README.md) · [All projects](../../README.md)

Project definitions live in `goldsmithing/projects.yml` inside the plugin's data
directory. See the [bundled definitions](https://github.com/TF-Minecraft/GemInfusion/blob/main/src/main/resources/goldsmithing/projects.yml)
for the available projects and their metal recipes.

## Gem projects

Projects with `gem: 1` need an infused gem before work begins. Recipe accuracy,
tool work, project tier, finishing quality, and the crafter's configured attribute
influence determine how much of the gem's stat reaches the finished jewellery.
The required tool hits come from the materials actually deposited.

## Gem-free projects

Projects with `gem: 0`, such as the bundled Golden Key, need only the configured
metals. They return the configured item without adding a gem stat or quality.

Finishing before the `min-hit-percent` threshold in `goldsmithing.yml` asks the
player to keep working and leaves the project intact. Once that threshold is
met, a gem-free project succeeds only with the exact recipe and required hits.
Missing hits, extra hits, or hits with unneeded tools ruin the piece and consume
the deposited metals without producing an item.

## Feedback and material recovery

The branding tool's status reports material counts and whether a required gem is
present. It does not reveal recipe or hit percentages while the project is in
progress. Those percentages appear after a piece is completed or ruined.

Every finished piece records the metal materials actually used. Compatible
recycling uses those recorded inputs instead of assuming the listed recipe was
followed. This applies to both jewellery and gem-free items.
