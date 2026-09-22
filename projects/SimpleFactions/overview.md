# SimpleFactions
The name stems from its original concept of a simple nation system, but it has since grown far beyond that.

This plugin adds factions (nations) to the game that can interact with each other through a complex diplomacy and economy system.

You will not be able to run this as a standalone program, as it depends on other plugins and the TFMC Minecraft 1.21.10 server environment.

## Why This Project Is Interesting
This plugin implements strategy-game-style diplomacy between nations and a fully original map/border system using a REST connection to a Python program I wrote myself:  
[ProvinceSystem](https://github.com/TF-Minecraft/ProvinceSystem)

Highlights include:

- **Nested Relationships** -- Factions can have subjects, and those subjects can have their own subjects.
- **Tax Simulation** -- When a player (or faction) earns money, their faction (or overlord) can automatically tax their income.

I drew heavy inspiration from strategy games by Paradox Interactive and leveraged my experience with object-oriented programming to implement parts of their systems. The project contains many interconnected classes that must remain consistent to avoid desynchronization.

This project also demonstrates cross-language integration through **ProvinceSystem**, requiring careful planning to keep server state synchronized between the Java plugin and the Python backend.

## Features
- Faction objects that function as nations in-game  
  ([Faction.java](https://github.com/TF-Minecraft/SimpleFactions/blob/ad9b048ec42c1842b277f4657f490b25691f854d/src/main/java/net/tfminecraft/simplefactions/objects/Faction.java))
- Faction relationships  
  ([RelationManager.java](https://github.com/TF-Minecraft/SimpleFactions/blob/ad9b048ec42c1842b277f4657f490b25691f854d/src/main/java/net/tfminecraft/simplefactions/managers/RelationManager.java))
- Titles (Kingdom, Duchy, etc.) connected with the REST server and the TitleManager  
  ([ProvinceSystem](https://github.com/TF-Minecraft/ProvinceSystem),
  [TitleManager.java](https://github.com/TF-Minecraft/SimpleFactions/blob/ad9b048ec42c1842b277f4657f490b25691f854d/src/main/java/net/tfminecraft/simplefactions/managers/TitleManager.java))

## Technical Overview
- Runtime target: TFMC Minecraft **1.21.10**; follow the [shared platform baseline](../../PLATFORM.md).
- Build with JDK 21 and Maven. The POM targets Java 21 bytecode (`maven.compiler.release=21`) and resolves `org.spigotmc:spigot-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope.
- Supply the authorized private JARs in `libs/` using the repository’s dependency preparation script and checksum file. Install matching Java 21 TLibs, RPCharacters, DenarEconomy, VehicleFramework and VFBuilders builds in local Maven before `mvn clean verify`. The shared baseline explains release status and dependency cycles.

### Architecture
- The main class initializes managers and overall plugin setup  
  ([SimpleFactions.java](https://github.com/TF-Minecraft/SimpleFactions/blob/ad9b048ec42c1842b277f4657f490b25691f854d/src/main/java/net/tfminecraft/simplefactions/SimpleFactions.java))
- Configuration files (and titles from JSON) are loaded and stored via the Loader classes  
  ([Loaders](https://github.com/TF-Minecraft/SimpleFactions/tree/ad9b048ec42c1842b277f4657f490b25691f854d/src/main/java/net/tfminecraft/simplefactions/loaders))
- `FactionManager` handles faction creation, lookups, member/leader queries, and database calls  
  ([FactionManager.java](https://github.com/TF-Minecraft/SimpleFactions/blob/ad9b048ec42c1842b277f4657f490b25691f854d/src/main/java/net/tfminecraft/simplefactions/managers/FactionManager.java))
- The `Inventory` package contains the extensive GUI classes players interact with  
  ([Inventory](https://github.com/TF-Minecraft/SimpleFactions/tree/ad9b048ec42c1842b277f4657f490b25691f854d/src/main/java/net/tfminecraft/simplefactions/managers/inventory))
- `MapSystem` is the primary interface for REST communication, while `RestServer` manages the actual requests and responses  
  ([MapSystem.java](https://github.com/TF-Minecraft/SimpleFactions/blob/ad9b048ec42c1842b277f4657f490b25691f854d/src/main/java/net/tfminecraft/simplefactions/map/MapSystem.java),\
  [RestServer.java](https://github.com/TF-Minecraft/SimpleFactions/blob/ad9b048ec42c1842b277f4657f490b25691f854d/src/main/java/net/tfminecraft/simplefactions/rest/RestServer.java))

## Key Challenges Solved

### Map System
Most Minecraft plugins that work with territory rely on the game's built-in region system (chunks). Chunks are small, perfectly square units, which makes borders look artificial. Since our world uses a fixed 4096×4096 coordinate grid, I realized I could generate an image of the same resolution and map each world coordinate directly to a pixel.

By drawing irregular “blobs” of unique RGB colors on this image, I created natural-looking provinces where:

> **province = the color of the pixel at your current coordinate**

The Minecraft plugin handles the coordinate and faction logic, while the external Python service (**ProvinceSystem**) processes the image and exposes province/border data on our website:  
https://www.tfminecraft.net/

A major challenge was keeping both systems synchronized efficiently. The Python service can take several minutes to redraw the full map, so regenerating unchanged regions was wasteful. To solve this, I implemented a queued update system that tracks exactly which provinces or borders changed in the Minecraft server state, and sends only incremental updates to the Python service. This dramatically reduced processing time and ensured consistent, near-real-time synchronization between the two systems.

---

### Money Flow and Taxation
Introducing a virtual economy requires strong guarantees against exploits (e.g., infinite money loops). One of the biggest challenges was implementing **nested taxation**:

- A faction can tax its members.
- A faction can be a subject to an overlord, which may also have its own overlord.
- Foreign income can be taxed depending on diplomatic relations.

The system needed to propagate tax values through these nested relationships without ever allowing the combined tax rate to exceed 100% - otherwise it would generate money that never existed. I solved this by implementing a clamped, hierarchical taxation model that guarantees consistency and prevents exploitable edge cases.

## AI Tools
I used **ChatGPT** primarily for troubleshooting and generating small amounts of code, such as the logic for loading titles from JSON.

For architecture, class design, and the overall structure of the plugin, I relied on my own judgment. In my experience, AI struggles to maintain coherent object-oriented structure in larger projects, so all high-level design, class relationships, and system architecture were created and implemented manually.

Most of the plugin was written without AI assistance to maintain control over the design and ensure consistency. **ChatGPT** was also used to help format and refine this README.

