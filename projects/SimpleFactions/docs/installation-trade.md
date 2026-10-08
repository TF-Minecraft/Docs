# Installation trade

[Project index](../README.md)

Ports, airports and train stations carry a guild's trade and production further, and so do the sea lanes and railways between them. Trade can board a line at any province along it, and it is strongest on and off at installations.

A guild uses installations in its own realm fully. An embargo or a war closes them. Otherwise access is the better of the trade agreement and the two realms' economy laws. An isolationist host stays closed to foreigners without an agreement.

| Economy law | Grants to foreign guilds | Own guilds' reach abroad |
|---|---|---|
| Free trade | 50% | +10% |
| Decentralized | 35% | 0 |
| Mercantilism | 15% | +20% |
| Protectionism | 10% | 0 |
| Isolationism | 0 | -25% |

Config keys:

- `installation-trade.transport` — rail, sea, and air, each with `trade`, `production`, and `kept-per-1000-blocks`
- `installation-trade.corridor-share`
- Relation types: `installation-access` and `blocks-installations`
- Law modifier: `installation_access`


Construct installations with `/faction construct <fort|port|airport|train_station> <name>`.

## Source references

- [Transport configuration](https://github.com/TF-Minecraft/SimpleFactions/blob/main/src/main/resources/config.yml)
- [Diplomatic access](https://github.com/TF-Minecraft/SimpleFactions/blob/main/src/main/resources/diplomacy.yml)
- [Economy laws](https://github.com/TF-Minecraft/SimpleFactions/blob/main/src/main/resources/laws.yml)
- [Trade graph](https://github.com/TF-Minecraft/SimpleFactions/tree/main/src/main/java/net/tfminecraft/simplefactions/guild/network)
