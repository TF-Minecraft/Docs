# Failure recovery and troubleshooting

[DrinkBuilder documentation](README.md) · [All projects](../../README.md)

How DrinkBuilder recovers from partial failures when it publishes, migrates or removes drinks, and what operators should and should not change by hand. Paths are relative to the DrinkBuilder data folder (`plugins/DrinkBuilder/`) unless stated otherwise.

## BreweryX custom-item hooks

An optional-dependency cycle can make BreweryX cache its MMOItems and ItemsAdder hooks as disabled. One tick after plugin startup and after every `/drinkbuilder reload`, [BreweryCompatibility](https://github.com/TF-Minecraft/DrinkBuilder/blob/main/src/main/java/net/tfminecraft/drinkbuilder/pack/BreweryCompatibility.java) re-enables any hook whose plugin is enabled, re-registers BreweryX's default plugin items, and reloads cauldron ingredients and recipes, including existing drinks. The `MMOItems:ID` ingredient format (no type prefix) is used for both the website catalogue and in-game recipes.

BreweryX is reached by reflection rather than a compile-time dependency; the reflective calls were verified against BreweryX 3.7.0 on Paper 1.21.10. If a step fails partway (for example, registration or the live reload throws), the server log shows `[brewery] compatibility repair failed`. Unfinished steps are remembered for that BreweryX instance and retried on the next DrinkBuilder reload.

## Legacy potion effect names

Legacy effect names are translated to their current names when drinks are published, for example `CONFUSION` becomes `NAUSEA`, `SLOW` becomes `SLOWNESS` and `DAMAGE_RESISTANCE` becomes `RESISTANCE`. The same migration runs over existing entries in BreweryX `recipes.yml` during the hook recovery above:

- Before the file is changed, the original is copied to `recipes-before-effect-migration-<random>.bak` in the BreweryX folder (`paths.breweryx-folder` in `config.yml`, default `plugins/BreweryX`). The migrated file is then written to a temporary file and moved into place.
- If `recipes.yml` is not valid YAML, it is left untouched and the server log reports `[brewery] recipe effect migration skipped`.

## Recipe write lock

Effect migration, drink publication and drink removal share one lock around the complete read-modify-replace of `recipes.yml`. Concurrent DrinkBuilder operations therefore cannot overwrite each other's changes, and migration cannot restore a recipe that was deleted in the meantime.

## Ingredient quantities

Ingredient quantities from the website JSON are written to BreweryX as exact positive integers (`<brewery_token>/<amount>`). Whole numbers written in decimal form, such as `3.0`, are accepted. Missing, fractional, zero or negative quantities, and ingredients with no `brewery_token` in `ingredients.yml`, fail the drink before its texture is published or its existing recipe is replaced.

## Retired ingredients

The bundled `ingredients.yml` allowlist omits retired herbs that have no active acquisition source, even when MMOItems still defines them. DrinkBuilder only writes `ingredients.yml` when the file is missing, so an existing server keeps its current list. To retire ingredients there:

1. Remove the retired entries from `ingredients.yml`.
2. Run `/drinkbuilder reload` or `/drinkbuilder catalog sync` to push the catalogue to the website.

Pruning the allowlist does not change previously approved drinks. Recipes that use a retired ingredient need their creators to choose an available replacement.

## Texture publication

Publishing a drink texture writes the PNG, the `tfmc_drinks` `configs/items.yml` entry and the pinned potion model ID, then assigns the model ID on the website ([IaDrinksWriter](https://github.com/TF-Minecraft/DrinkBuilder/blob/main/src/main/java/net/tfminecraft/drinkbuilder/pack/IaDrinksWriter.java)).

- Before writing any files, DrinkBuilder records the model ID reservation in `pending-writes/<drink id>.yml`.
- If any step fails, the previous local files are restored.
- If the failure happened before the website was asked to assign the ID, the reservation is released.
- Once the website may have accepted the ID, even if its response was lost, `pending-writes/` keeps the reservation. The next pull retries with the same ID, including after a restart.

Do not delete `pending-writes/` records or reset `cmd-state.yml` to work around an error. Doing so can reuse a model ID that is already assigned to another drink.

`cmd-state.yml` stores the allocator's next ID and freed IDs within the configured `cmd.min`/`cmd.max` range. If the file exists but is unreadable or has no valid `next` counter, DrinkBuilder fails to enable rather than restarting allocation from the beginning of the range. Restore the file from a backup instead of deleting it.

## Drink deletion

`/drinkbuilder drink delete <id>` removes the BreweryX recipe, revokes the drink on the website, then removes the ItemsAdder entry and frees the model ID when the texture is no longer shared ([DrinkDeleteRunner](https://github.com/TF-Minecraft/DrinkBuilder/blob/main/src/main/java/net/tfminecraft/drinkbuilder/pack/DrinkDeleteRunner.java)). Each failure is reported separately:

| Message | State |
|---------|-------|
| `recipe cleanup failed ... Website record retained.` | Nothing was revoked; the website record still exists. |
| `Local recipe cleanup done but API revoke failed` | The recipe was removed locally; the website still lists the drink. |
| `revoked, but IA cleanup failed ... CMD retained; manual cleanup required.` | The website revoked the drink, but local ItemsAdder cleanup failed. The model ID stays reserved and an ItemsAdder refresh is queued for any partial change. |

The command message and the server log (`[drink-delete]`) identify the failed step. A successful website revocation is never reported as a successful local cleanup.
