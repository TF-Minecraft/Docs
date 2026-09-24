# ProvinceSystem documentation

**tfminecraft.net** is the TFMC web hub: interactive political maps, donator cosmetics (skins and drinks), character creation, and identity services backed by a FastAPI backend and Next.js frontend.

The game integration target is Minecraft **1.21.10**; see the [shared platform baseline](../../../PLATFORM.md). ProvinceSystem itself uses the web runtimes described in [architecture.md](architecture.md).

This section is the product and technical reference for **ProvinceSystem**. Technical documentation for TF-Minecraft repositories is maintained together in [TF-Minecraft/Docs](../../../README.md).

## Reading order

1. [architecture.md](architecture.md) - stack, routes, data layout
2. Product areas (pick what you need):
   - [map/overview.md](map/overview.md) - map platform goals and layers
   - [cosmetics/skins.md](cosmetics/skins.md) - skins upload and review
   - [cosmetics/drinks.md](cosmetics/drinks.md) - BreweryX drink builder
   - [characters/creator.md](characters/creator.md) - web character creator
   - [identity/tfmcweb.md](identity/tfmcweb.md) - Discord link, tokens, gate
3. [flows/journeys.md](flows/journeys.md) - end-to-end player and staff journeys
4. [ops/local-dev.md](ops/local-dev.md) - run the site locally
5. [ops/sheet-render.md](ops/sheet-render.md) - 3D review-sheet renderer (prod deploy + smoke)
6. [ops/dev-config.md](ops/dev-config.md) - dev-only flags and shortcuts

Schema assets: [assets/map-export-schema.json](assets/map-export-schema.json) (SF map export contract).

## Components

| Component | Path | Role | Docs |
|-----------|------|------|------|
| **ProvinceSystem** | `ProvinceSystem/` | Website + FastAPI: maps, skins, drinks, characters, identity | This folder |
| **TFMCWeb** | `tfmcweb/` | MC ↔ web gate: Discord link, scoped tokens, Survival Discord freeze, warn/ban mirror | [identity/tfmcweb.md](identity/tfmcweb.md) |
| **SimpleFactions** | `simplefactions/` | Map bridge: nation JSON upload, queue, regen, province lookup | [integrations/simplefactions.md](integrations/simplefactions.md) |
| **ArmourShop** | `armourshop/` | Skins pack writer + apply | [integrations/armourshop.md](integrations/armourshop.md) |
| **DrinkBuilder** | `drinkbuilder/` | Donator BreweryX drinks + `tfmc_drinks` IA | [cosmetics/drinks.md](cosmetics/drinks.md) |
| **RPCharacters** | `rpcharacters/` | Characters + freeze loop; Discord gate via freeze reason | [characters/creator.md](characters/creator.md) |
| **ItemsAdder** | Server `plugins/ItemsAdder/` | Resource packs: `tfmc_submissions`, `tfmc_armorshop`, `tfmc_drinks` | [integrations/armourshop.md](integrations/armourshop.md) |
| **tfmc_bot** | `tfmc_bot/` | Red-DiscordBot: skins/drinks review, link, ban/warn DMs | [integrations/discord-bot.md](integrations/discord-bot.md) |

## Locked platform decisions

- **Name:** TFMC = TF Minecraft. "TF" has no expansion.
- **No site logins** - skins, drinks, and characters use TFMCWeb-issued UUID-bound codes; redeem → API session (8h default; character Remember me = 30d).
- **Shared cosmetic mint cooldown** - skin + drink share one clock on **TFMCWeb** (not ProvinceSystem).
- **Discord link** - in-game `/linkdiscord` + Discord `/linkdiscord <code>`; required before upload.
- **SQLite + disk** for skins/drinks metadata and pending files on the API.
- **SimpleFactions = map only**; **ArmourShop = skins pack writer**; **TFMCWeb = identity + web transport**.

## Ops references

- Deployment and QA checklists: [STAGING.md](../STAGING.md)
- Production deploy guide: [UPDATE.md](../UPDATE.md)
