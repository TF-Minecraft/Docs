# TF-Minecraft Docs

> The technical home for TF-Minecraft's plugins, website, and shared systems.

Explore how TF-Minecraft's projects fit together, from crafting and roleplay to
vehicles, trade, and server administration. This repository collects the guides
for setup, architecture, configuration, integrations, testing, and operations.
Each source repository's README introduces what that project does; its technical
guides live here.

TFMC runs **Minecraft 1.21.10 on Java 21**. The [shared platform and build baseline](PLATFORM.md) defines common runtime, toolchain and validation conventions, with the current build declarations for each plugin.

## Start here

| Looking for… | Go to… |
| --- | --- |
| Java and Minecraft targets | [Shared platform baseline](PLATFORM.md) |
| A project's guides | [Browse the projects below](#projects) |
| Build and release conventions | [Builds and releases](PIPELINES.md) |
| The server test environment | [Minecraft test lab](projects/ServerAssets/docs/LAB.md) |
| The website and backend | [Web hub documentation](projects/ProvinceSystem/docs/README.md) |
| Documentation contribution guidance | [Maintaining the documentation](MAINTAINING.md) |

## Projects

Choose a project to open its technical documentation and source repository link.

### Crafting and professions

| Project | What it does |
| --- | --- |
| [AdvancedCrafting](projects/AdvancedCrafting/README.md) | TF-Minecraft crafting stations, alloys, ingredient conversion and lifecycle APIs |
| [Archaeo](projects/Archaeo/README.md) | Archaeology, hidden ruins, excavation, and fragile finds. |
| [Cooking](projects/Cooking/README.md) | Interactive cooking stations and custom food crafting. |
| [GemInfusion](projects/GemInfusion/README.md) | Gem infusion and jewellery crafting mechanics. |
| [Woodworking](projects/Woodworking/README.md) | Woodworking stations, crafting projects, and material quality. |

### Roleplay and activities

| Project | What it does |
| --- | --- |
| [ActivityTF](projects/ActivityTF/README.md) | Daily activity tasks, weekly progress, and player rewards. |
| [BirdMessenger](projects/BirdMessenger/README.md) | Bird-delivered letters and interactive mailboxes. |
| [Games](projects/Games/README.md) | Tabletop games, card games, and wagering. |
| [GeigerCounters](projects/GeigerCounters/README.md) | Geiger counter treasure hunts with proximity signals and tiered loot. |
| [Magic](projects/Magic/README.md) | Magic, resonance, artifacts, and shrines. |
| [MusicalInstruments](projects/MusicalInstruments/README.md) | Playable instruments, notes, and chords for live music. |
| [RPCharacters](projects/RPCharacters/README.md) | Roleplay characters, professions, chat channels, and player identity. |
| [Surgery](projects/Surgery/README.md) | Interactive surgery, diagnosis, and patient vitals for medical roleplay. |
| [Thievery](projects/Thievery/README.md) | Pickpocketing, robbery, and theft mechanics. |

### Trade and customisation

| Project | What it does |
| --- | --- |
| [ArmourShop](projects/ArmourShop/README.md) | Custom armour and weapon cosmetics. |
| [BarterShops](projects/BarterShops/README.md) | Sign-based player shops and item trading with DenarEconomy integration. |
| [DenarEconomy](projects/DenarEconomy/README.md) | Currency and economy systems. |
| [DrinkBuilder](projects/DrinkBuilder/README.md) | Website-integrated custom drink creation and recipe syncing. |
| [InteractibleFurniture](projects/InteractibleFurniture/README.md) | Interactive furniture and a shared furniture API. |
| [MarketBlock](projects/MarketBlock/README.md) | Market trading, item categories, and demand-based pricing. |
| [Recycler](projects/Recycler/README.md) | Configurable item recycling and material recovery. |

### World, vehicles, and combat

| Project | What it does |
| --- | --- |
| [GunsAndGadgets](projects/GunsAndGadgets/README.md) | Configurable firearms, ammunition, and gadgets. |
| [SimpleFactions](projects/SimpleFactions/README.md) | Nations, diplomacy, taxation, and ProvinceSystem map integration. |
| [VehicleFramework](projects/VehicleFramework/README.md) | Configurable vehicles, movement physics, turrets, and weapons. |
| [VFBuilders](projects/VFBuilders/README.md) | Vehicle construction stations and blueprints for VehicleFramework. |
| [WorldBorder](projects/WorldBorder/README.md) | Configurable world borders, player warnings, and border damage. |

### Web and shared services

| Project | What it does |
| --- | --- |
| [AACommandsFiller](projects/AACommandsFiller/README.md) | Configurable command trees and permission-aware tab completion. |
| [CoreProtect](projects/CoreProtect/README.md) | TFMC-maintained CoreProtect source for block logging, rollbacks, and anti-griefing on Minecraft servers. |
| [PermCleaner](projects/PermCleaner/README.md) | Permission inspection and cleanup with LuckPerms integration. |
| [ProvinceSystem](projects/ProvinceSystem/README.md) | TFMC web hub with interactive political maps, character creation, cosmetics, and identity services. |
| [ServerAssets](projects/ServerAssets/README.md) | Private server binaries, tested configurations, models, resource packs, and test-lab assets. |
| [TFMCCore](projects/TFMCCore/README.md) | Shared gameplay systems, server utilities, and plugin integrations. |
| [TFMCWeb](projects/TFMCWeb/README.md) | Website integration, Discord account linking, and player identity services. |
| [TLibs](projects/TLibs/README.md) | Shared Java utilities and integration APIs. |

### Archived projects

AdvancedGunpowder, AdvancedResearch, Goldsmithing, Nutrition and PointShop were
briefly reopened for their Java 21 / Minecraft 1.21.10 migrations. Those changes
are merged, their main-branch builds passed, and all five repositories are
archived again. BreedingBuddies remains archived for historical reference.

| Project | What it does |
| --- | --- |
| [AdvancedGunpowder](projects/AdvancedGunpowder/README.md) | Musket and gunpowder weapon mechanics. |
| [AdvancedResearch](projects/AdvancedResearch/README.md) | Research stations, notes, and progression. |
| [BreedingBuddies](projects/BreedingBuddies/README.md) | Animal breeding, care, ownership, and mount stats. |
| [Goldsmithing](projects/Goldsmithing/README.md) | Goldsmithing tables and jewellery crafting. |
| [Nutrition](projects/Nutrition/README.md) | Food groups, diet variety, and player nutrition. |
| [PointShop](projects/PointShop/README.md) | Points-based shops and configurable player rewards. |

## Documentation

Technical documentation is maintained in [TF-Minecraft/Docs](https://github.com/TF-Minecraft/Docs).

This repository is public. Private source repositories and licensed binaries
retain their existing access restrictions. Licenses, contribution policies, and
code/API comments remain with their source projects.
