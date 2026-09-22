> This page is public; linked jars, models and configurations remain in the private server-assets repository and require access. The full ItemsAdder contents archive was removed from server-assets on 2026-09-22; historical lab notes below describe the original snapshot. The existing manifest/materializer may still expect that archive.

# Jar inventory

60 distinct plugin/API jar binaries, plus Paper 1.21.10 build 130.

## Tested runtime

| Jar | Plugin version | SHA-256 |
| --- | --- | --- |
| [ItemsAdder.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/runtime/plugins/ItemsAdder.jar) | 4.0.18 | `5a01b37bd7442fb0f2c809cadac82ba70f75173956e04efac3336595cc070368` |
| [MMOCore.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/runtime/plugins/MMOCore.jar) | 1.13.1-SNAPSHOT | `81d511d0830951f988615b6533cc93e82d00a83fb31e8ccbb36441ae3e8157ef` |
| [MMOItems.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/runtime/plugins/MMOItems.jar) | 6.10.1-SNAPSHOT | `a37f7789fcdcd11c9e5890a2fac742aa4501749588af23182991953e06ee1d17` |
| [ModelEngine.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/runtime/plugins/ModelEngine.jar) | R4.1.1 | `44ee292392dd86b4aa4824c2e11668a9dee0333b83ae013987e1ba78d19f51a0` |
| [MythicLib.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/runtime/plugins/MythicLib.jar) | 1.7.1-SNAPSHOT | `e89a612e566e9b7dc4f43228adb8f6e560f293ea4107bae259c6dfd6732d7a70` |
| [MythicMobs.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/runtime/plugins/MythicMobs.jar) | 5.13.1-SNAPSHOT-88530541 | `6df72b5b331d5d8881f2b0ab99cbaa236dd941cbbbaf69fbd05dcb412bffb7f6` |
| [NBTAPI.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/runtime/plugins/NBTAPI.jar) | 2.15.5 | `94056a0c9252cb3cd81ff2fe4dc96e674b51098c86b162b861b7dca1d2d33921` |
| [ProtocolLib.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/runtime/plugins/ProtocolLib.jar) | 5.4.0 | `ee2e7ab9b5386f2d103081c4d108e61b1035df2ca692b53d6e2409fb1f5caccf` |
| [TLibs.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/runtime/plugins/TLibs.jar) | 1.0 | `bbac27e3055d135a4a7f6164ace5e32b7e6275cc8387575a8c8e1809fdc555fd` |
| [VehicleFramework.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/runtime/plugins/VehicleFramework.jar) | 1.1.12 | `9dcf9d18721c6541a6134d5a0d23496edb09280e16bb1f60e3f4755cf0a5b564` |

## Other supplied, compile-time and historical jars

These are retained references, not an alternative tested runtime set. Build aliases
are recorded separately in `manifest.json`. All source filenames are preserved there.

| Jar | Roles | SHA-256 |
| --- | --- | --- |
| [MythicMobs-5.8.0-SNAPSHOT.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/575aa30aee8e/MythicMobs-5.8.0-SNAPSHOT.jar) | build | `575aa30aee8ef723ad36229eb6c4223bca6e4037d271ddccc8f23cf6faa69747` |
| [gson-2.10.1.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/4241c14a7727/gson-2.10.1.jar) | build, supplied-reference | `4241c14a7727c34feea6507ec801318a3d4a90f070e4525681079fb94ee4c593` |
| [item-nbt-api-plugin-2.15.0.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/a5f593d6214b/item-nbt-api-plugin-2.15.0.jar) | build, supplied-reference | `a5f593d6214b8dff79d5d304b3a813160836be4b0b714f1e0f79a9e0de0b9ee1` |
| [joml-1.10.8.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/bf1951014517/joml-1.10.8.jar) | build, supplied-reference | `bf19510145178df82cd3bd37edd514c13f411531ec5545299fd3abcbc98fe7c2` |
| [json-simple-1.1.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/2d9484f4c649/json-simple-1.1.jar) | build, supplied-reference | `2d9484f4c649f708f47f9a479465fc729770ee65617dca3011836602264f6439` |
| [spigot-api.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/b7156eab5677/spigot-api.jar) | build | `b7156eab567772f9fdac0bf696b209111790c3f69149ab9a742e3dd030ec4b10` |
| [AngelChest-11.1.2.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/70751fb0e5d2/AngelChest-11.1.2.jar) | supplied-reference | `70751fb0e5d2a2625480ee60e3a69a573489a83245ef1918e2648e69d9551cd8` |
| [api-5.4.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/086e3971ea63/api-5.4.jar) | supplied-reference | `086e3971ea63c0b5ad567881b2dfd955acbbffa24fe85ceac8abf54b114ce986` |
| [BungeeCord.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/3bc6fa2477eb/BungeeCord.jar) | supplied-reference | `3bc6fa2477eb30f840d14c6b9e7074d8326ef9a100add8a6db89e85ecf53a3f2` |
| [ConditionalEvents-4.74.1.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/f9041933e7af/ConditionalEvents-4.74.1.jar) | supplied-reference | `f9041933e7af3ba97a410cd07e7cd35f36a8542de0d17abede8f9754805180cf` |
| [CustomCrops-3.6.49.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/0aa5d3cb6bad/CustomCrops-3.6.49.jar) | supplied-reference | `0aa5d3cb6bad9b36f0ef4b47dbcf6e40dbbad44470ec7fa7606c30d4d815a94b` |
| [CustomFishing-2.3.27.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/7d3083bd0599/CustomFishing-2.3.27.jar) | supplied-reference | `7d3083bd05998d8cafd7114ced74a6fa2ec1c4d36f75dbbaee9f20d499a7c3ad` |
| [ItemsAdder_3.4.0-beta-r11.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/a48d49f1edf3/ItemsAdder_3.4.0-beta-r11.jar) | supplied-reference | `a48d49f1edf3ad90e6dfcb682ca0ae9c90b1c3c9cb4a8bfe75b235326985ec9f` |
| [ItemsAdder_3.4.1c.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/69a333cda333/ItemsAdder_3.4.1c.jar) | supplied-reference | `69a333cda333553141998883a504ede0aae6eb207233580f7b04c22e9aca4d23` |
| [ItemsAdder_3.5.0-r2.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/0116d714822b/ItemsAdder_3.5.0-r2.jar) | supplied-reference | `0116d714822b6f0cfebfe833a5df2e4754797b637d0fe709afb762c56da463a3` |
| [json-20220320.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/1edf7fcea79a/json-20220320.jar) | supplied-reference | `1edf7fcea79a16b8dfdd3bc988ddec7f8908b1f7762fdf00d39acb037542747a` |
| [MCPets-3.1.1.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/239abafd0630/MCPets-3.1.1.jar) | supplied-reference | `239abafd0630959c77ce7e0103a180e4776ca0d836c6a409b6785eb3a1eaae2f` |
| [MMOCore-1.11.3.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/d52cc0c734a9/MMOCore-1.11.3.jar) | supplied-reference | `d52cc0c734a9bb942428a403bb3630123596bcd9c94d3a77ea2782046b113af5` |
| [MMOCore-1.13.1.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/14850d745437/MMOCore-1.13.1.jar) | supplied-reference | `14850d7454374d7312305d3e84a391be720301e5964963f869b27ae97f6264eb` |
| [MMOCore-1.9.2-385.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/beb0afc05932/MMOCore-1.9.2-385.jar) | supplied-reference | `beb0afc059324e68d23e20f6700e47b18d129ba1c17c0d7f4edb3c62cde87db2` |
| [MMOInventory-2.0-20260330.113858-32.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/f97dcbbb2c4b/MMOInventory-2.0-20260330.113858-32.jar) | supplied-reference | `f97dcbbb2c4b257825afccde0b81550de9e636bf0e75468233134c0590b69c68` |
| [MMOItems-6.10.1-20250521.175300-22.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/8ff714bd3f48/MMOItems-6.10.1-20250521.175300-22.jar) | supplied-reference, historical | `8ff714bd3f486de26e9869462d4696eece5958287ce75a013cb30eb6bebd5e88` |
| [MMOItems-6.10.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/c84700df5942/MMOItems-6.10.jar) | supplied-reference | `c84700df5942fd969d3e8c2f1ad2c3ebeb17987ef88b426408d1306e49c4aada` |
| [MMOItems-6.7.2-833.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/d40fb9ee06b1/MMOItems-6.7.2-833.jar) | supplied-reference | `d40fb9ee06b14c7b9d2e7cab6d9fa98a91bd0589ba498ee1f78aa06bfa0b60c6` |
| [MMOItems-6.8.1.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/4f1a3bea3917/MMOItems-6.8.1.jar) | supplied-reference | `4f1a3bea39177ff9dd26f9f45fe1881b71787e7e733ec84e09eef5b3b5b9103d` |
| [MMOItems-6.9.1.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/ad8f89a8b23a/MMOItems-6.9.1.jar) | supplied-reference | `ad8f89a8b23a6d70d71962f318a67e981cd6ddb05f0d126fec1d2080577b9562` |
| [MMOItems-6.9.3.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/79f68e5cf811/MMOItems-6.9.3.jar) | supplied-reference | `79f68e5cf8113ff4e1c35bf6d7a43313696e2d0e1e607c26ea13ba28133f0cf6` |
| [MMOItems-6.9.4.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/7deced7e18f1/MMOItems-6.9.4.jar) | supplied-reference | `7deced7e18f1f29f9835354e27b83a33d24f8fd44f5b151a3c3bf27a9800056a` |
| [ModelEngine-3.1.8.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/d0d55dee639a/ModelEngine-3.1.8.jar) | supplied-reference | `d0d55dee639ad5088922ae1d997314a8217081aa28586accd88bb27cbc1c9d3d` |
| [ModelEngine-4.0.8.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/a31541f5285b/ModelEngine-4.0.8.jar) | supplied-reference | `a31541f5285bc92a826633f63e78e6607f69c6f180fea367ba3e0008a5b96a84` |
| [MythicLib-1.3.1-229.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/e4706c62fa67/MythicLib-1.3.1-229.jar) | supplied-reference | `e4706c62fa678eb483c710c723102bac59f843d4282a3c9c9349d99bea0a52f1` |
| [MythicLib-1.4.1.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/8af05503d87c/MythicLib-1.4.1.jar) | supplied-reference | `8af05503d87ceef3faa9dbc2b5568e508f2c1a574157ee801f4ed081d51301c1` |
| [MythicLib-1.5.2.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/4baaa2bb1897/MythicLib-1.5.2.jar) | supplied-reference | `4baaa2bb1897a85b924b7f7a43ae2637f644dbfb8ed240776094ba0b060f32fa` |
| [MythicLib-1.6.1.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/028339a7e584/MythicLib-1.6.1.jar) | supplied-reference | `028339a7e584b9b4e0f06c56dcf3dc0e44562a79fe6cbc5a769eca47ad8542bf` |
| [MythicLib-1.7.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/660ff2a6ec86/MythicLib-1.7.jar) | supplied-reference | `660ff2a6ec86bc8d7779948cf65c1637e271a16e1ef812d6a273f4a5c5eec73c` |
| [MythicLib-dist-1.7.1.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/a3f86a50d382/MythicLib-dist-1.7.1.jar) | supplied-reference | `a3f86a50d38296dd0a91d375f0a9433192e6e8d3e9dcae2751c801e67d24d9cd` |
| [MythicMobs-5.0.3-4094.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/7221e5921a63/MythicMobs-5.0.3-4094.jar) | supplied-reference | `7221e5921a6390a85da5cb7ee6adaa737979fc34d228d8456797563ea78b596a` |
| [MythicMobs-5.3.1.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/a13629c86fa3/MythicMobs-5.3.1.jar) | supplied-reference | `a13629c86fa3c2e62c92b6408fc762938ce321bf7374046c27ed16b93db0993d` |
| [MythicMobs-5.3.5.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/6428ea0a2a52/MythicMobs-5.3.5.jar) | supplied-reference | `6428ea0a2a52b22c76bfd21d165118bf092b6fc47a5075c8756b307c93ec61ba` |
| [MythicMobs-5.4.0.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/baf16e1dc917/MythicMobs-5.4.0.jar) | supplied-reference | `baf16e1dc9176023a1dfc03352d9f2a97c182548bf29b74e8768a610fa8c3f5b` |
| [MythicMobs-5.8.0-SNAPSHOT.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/5f9313dd9cb6/MythicMobs-5.8.0-SNAPSHOT.jar) | supplied-reference | `5f9313dd9cb693603488299ff6ac84b8e99288c783878243f465ed35fe1d21ba` |
| [OpenRP.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/f79ff44d86b2/OpenRP.jar) | supplied-reference | `f79ff44d86b2d683a4e9e59ad0e553c05dc771a25f359774fd63e22b50e41c4d` |
| [spigot-api.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/c96a8a27e27a/spigot-api.jar) | supplied-reference | `c96a8a27e27a68d205217d25a2897251dbeb0bf287200c7429f83c7fdbfd6910` |
| [spigot-api-1.21.10.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/153770f6243d/spigot-api-1.21.10.jar) | supplied-reference | `153770f6243d321dbcc821584eb36bf04bbc1b406f43652f627f962ef938a4d7` |
| [worldguard-bukkit-7.0.14-dist.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/707255ab7106/worldguard-bukkit-7.0.14-dist.jar) | supplied-reference | `707255ab71069cda98dd1217ed1f16f88f3e40505e16416794f32d0e2666ebd3` |
| [ModelEngine-4.1.0-FREE.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/d24b7d4e865f/ModelEngine-4.1.0-FREE.jar) | historical | `d24b7d4e865f5453cb2947ec87bd3549e571c7d7927cd22e0c6927b03426090d` |
| [NBTAPI-2.15.2.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/148a5f180235/NBTAPI-2.15.2.jar) | historical | `148a5f1802354d73c49b017caa2740960e05ebb5f71ec0ff26fee12cabd865ba` |
| [TLibs-1.0.3.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/d8062cdca816/TLibs-1.0.3.jar) | historical | `d8062cdca816392d29275a96d53a912d27300a098bebc3727fcb6c983fe1ed37` |
| [NBTAPI.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/a65899d60458/NBTAPI.jar) | historical | `a65899d60458c790c176b4581721695203ab8eb59b485f8bd81350857392fef7` |
| [ProtocolLib.jar](https://github.com/TF-Minecraft/server-assets/blob/a8a0efde5c58ef77d5ca085e422aa2c3e9565c5e/jars/355f7117af95/ProtocolLib.jar) | historical | `355f7117af95b3f8e3cb63440fcf8a3bb9808bc89ac6ac5c57142327480e9437` |
