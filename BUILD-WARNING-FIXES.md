# Build warning fixes

Follow-up to the [latest-build warning audit](BUILD-WARNINGS.md), collected on 22 September 2026. Scope: the latest Build workflow for each of the 39 repositories, plus warnings exposed by compiling with deprecation diagnostics enabled.

35 Java repositories pass local Java 21 `mvn clean verify` with tests enabled. The 113 private dependency declarations in 29 repositories retain their exact checksum-pinned bytes and use hash-qualified Maven versions with `provided` scope. This also covers DenarEconomy, whose property-based `systemPath` did not produce a warning in the original log.

Six shaded JARs were inspected: dependency manifests and module descriptors are excluded, plugin manifests remain present, and CoreProtect retains `Multi-Release: true` and its mapping namespace. Mockito loads through an explicit test agent; SLF4J providers are test-only. Integer model data uses component snapshots while retaining the original float rounding, null reset, and empty-component behavior.

ProvinceSystem: 1,100 backend tests passed, 1 skipped; 1,568 frontend tests passed, 1 skipped. The local frontend run used Node 22 and a 15-second test timeout because the catalogue-link test exceeded 5 seconds on this host. The production build passed. GitHub CI keeps its ordinary timeout.

## Retained warnings and compatibility boundaries

- Expected warning messages from negative tests remain: malformed configuration, rejected operations, unavailable optional integrations, and invalid test inputs are intentionally exercised.
- ProvinceSystem still encounters an upstream Starlette/AnyIO deprecation (`iscoroutinefunction`). There was no compatible released upstream fix at verification time; application startup itself now uses FastAPI lifespan.
- A first build without a saved Next.js cache can still report a cold cache. CI now restores and saves it.
- Deprecated APIs needed for legacy text formatting, stored Bukkit metadata, historical CoreProtect migrations, older-server adapters, or upstream APIs without equivalent replacements have documented method/local-variable exceptions. These are retained compatibility uses, not completed API migrations. Raw json-simple 1.1 test fixtures have similarly narrow unchecked exceptions. Compiler diagnostics remain enabled globally.

## Per-repository changes

PR links show current review and merge state. Each repository remains independently buildable; no shared parent POM or runtime data migration was introduced.

| Repository | Changes | Validation | PR |
| --- | --- | --- | --- |
| AACommandsFiller | API/type warnings and documented compatibility uses | Maven verify; no unit-test suite | [PR #14](https://github.com/TF-Minecraft/AACommandsFiller/pull/14) |
| activity-tf | Verified Maven inputs; API/type warnings and documented compatibility uses | Maven verify; 741 tests, 0 failures/errors | [PR #70](https://github.com/TF-Minecraft/ActivityTF/pull/70) |
| AdvancedCrafting | Verified Maven inputs; Model-data component API; API/type warnings and documented compatibility uses | Maven verify; no unit-test suite | [PR #12](https://github.com/TF-Minecraft/AdvancedCrafting/pull/12) |
| advancedgunpowder | Verified Maven inputs | Maven verify; no unit-test suite | [PR #13](https://github.com/TF-Minecraft/AdvancedGunpowder/pull/13) |
| advancedresearch | Verified Maven inputs; Model-data component API; API/type warnings and documented compatibility uses | Maven verify; no unit-test suite | [PR #13](https://github.com/TF-Minecraft/AdvancedResearch/pull/13) |
| armourshop | Verified Maven inputs; Mockito test agent; API/type warnings and documented compatibility uses | Maven verify; 9 tests, 0 failures/errors | [PR #19](https://github.com/TF-Minecraft/ArmourShop/pull/19) |
| bartershops | Verified Maven inputs; API/type warnings and documented compatibility uses | Maven verify; no unit-test suite | [PR #16](https://github.com/TF-Minecraft/BarterShops/pull/16) |
| birdmessenger | Verified Maven inputs; Mockito test agent | Maven verify; 5 tests, 0 failures/errors | [PR #20](https://github.com/TF-Minecraft/BirdMessenger/pull/20) |
| cooking | Verified Maven inputs; Model-data component API; API/type warnings and documented compatibility uses | Maven verify; 167 tests, 0 failures/errors | [PR #24](https://github.com/TF-Minecraft/Cooking/pull/24) |
| CoreProtect | Shade metadata; API/type warnings and documented compatibility uses | Maven verify; no unit-test suite | [PR #12](https://github.com/TF-Minecraft/CoreProtect/pull/12) |
| denareconomy | Verified Maven inputs; API/type warnings and documented compatibility uses | Maven verify; 17 tests, 0 failures/errors | [PR #21](https://github.com/TF-Minecraft/DenarEconomy/pull/21) |
| Docs | Build-input guidance and audit reports | Link checker tests, navigation/links, strict MkDocs build | — |
| drinkbuilder | Verified Maven inputs; Shade metadata | Maven verify; no unit-test suite | [PR #18](https://github.com/TF-Minecraft/DrinkBuilder/pull/18) |
| games | Verified Maven inputs; API/type warnings and documented compatibility uses | Maven verify; 37 tests, 0 failures/errors | [PR #18](https://github.com/TF-Minecraft/Games/pull/18) |
| geiger-counters | Shade metadata; API/type warnings and documented compatibility uses | Maven verify; no unit-test suite | [PR #18](https://github.com/TF-Minecraft/GeigerCounters/pull/18) |
| geminfusion | Verified Maven inputs; API/type warnings and documented compatibility uses | Maven verify; no unit-test suite | [PR #20](https://github.com/TF-Minecraft/GemInfusion/pull/20) |
| goldsmithing | Verified Maven inputs; Model-data component API; API/type warnings and documented compatibility uses | Maven verify; no unit-test suite | [PR #13](https://github.com/TF-Minecraft/Goldsmithing/pull/13) |
| gunsandgadgets | Verified Maven inputs; Model-data component API; API/type warnings and documented compatibility uses | Maven verify; no unit-test suite | [PR #19](https://github.com/TF-Minecraft/GunsAndGadgets/pull/19) |
| interactiblefurniture | Verified Maven inputs | Maven verify; no unit-test suite | [PR #20](https://github.com/TF-Minecraft/InteractibleFurniture/pull/20) |
| magic | Verified Maven inputs; Model-data component API; API/type warnings and documented compatibility uses | Maven verify; no unit-test suite | [PR #18](https://github.com/TF-Minecraft/Magic/pull/18) |
| Marketblock | Verified Maven inputs | Maven verify; no unit-test suite | [PR #18](https://github.com/TF-Minecraft/MarketBlock/pull/18) |
| musical-instruments | Model-data component API; Shade metadata; API/type warnings and documented compatibility uses | Maven verify; no unit-test suite | [PR #15](https://github.com/TF-Minecraft/MusicalInstruments/pull/15) |
| nutrition | Verified Maven inputs | Maven verify; no unit-test suite | [PR #15](https://github.com/TF-Minecraft/Nutrition/pull/15) |
| PermCleaner | Mockito test agent | Maven verify; 20 tests, 0 failures/errors | [PR #18](https://github.com/TF-Minecraft/PermCleaner/pull/18) |
| pointshop | Verified Maven inputs; API/type warnings and documented compatibility uses | Maven verify; no unit-test suite | [PR #15](https://github.com/TF-Minecraft/PointShop/pull/15) |
| ProvinceSystem | FastAPI lifespan; explicit Next.js root; build cache; canvas test stub | Backend/frontend suites and production build | [PR #10](https://github.com/TF-Minecraft/ProvinceSystem/pull/10) |
| Recycler | Verified Maven inputs; API/type warnings and documented compatibility uses | Maven verify; no unit-test suite | [PR #18](https://github.com/TF-Minecraft/Recycler/pull/18) |
| rpcharacters | Verified Maven inputs; Model-data component API; Mockito test agent; API/type warnings and documented compatibility uses | Maven verify; 73 tests, 0 failures/errors | [PR #21](https://github.com/TF-Minecraft/RPCharacters/pull/21) |
| server-assets | No changes; original latest build had no warnings | Original Build workflow succeeded | — |
| simplefactions | Verified Maven inputs; Model-data component API; Mockito test agent; API/type warnings and documented compatibility uses | Maven verify; 1979 tests, 0 failures/errors | [PR #23](https://github.com/TF-Minecraft/SimpleFactions/pull/23) |
| surgery | API/type warnings and documented compatibility uses | Maven verify; no unit-test suite | [PR #18](https://github.com/TF-Minecraft/Surgery/pull/18) |
| tfmccore | Verified Maven inputs; SLF4J test provider; API/type warnings and documented compatibility uses | Maven verify; 41 tests, 0 failures/errors | [PR #18](https://github.com/TF-Minecraft/TFMCCore/pull/18) |
| tfmcweb | Verified Maven inputs; Mockito test agent | Maven verify; 5 tests, 0 failures/errors | [PR #19](https://github.com/TF-Minecraft/TFMCWeb/pull/19) |
| thievery | Verified Maven inputs; Model-data component API; API/type warnings and documented compatibility uses | Maven verify; no unit-test suite | [PR #18](https://github.com/TF-Minecraft/Thievery/pull/18) |
| tlibs | Verified Maven inputs; Model-data component API; Shade metadata; API/type warnings and documented compatibility uses | Maven verify; 10 tests, 0 failures/errors | [PR #22](https://github.com/TF-Minecraft/TLibs/pull/22) |
| vehicleframework | Verified Maven inputs; Model-data component API; Shade metadata; SLF4J test provider; API/type warnings and documented compatibility uses | Maven verify; 398 tests, 0 failures/errors | [PR #20](https://github.com/TF-Minecraft/VehicleFramework/pull/20) |
| vfbuilders | Verified Maven inputs | Maven verify; no unit-test suite | [PR #18](https://github.com/TF-Minecraft/VFBuilders/pull/18) |
| woodworking | Verified Maven inputs | Maven verify; no unit-test suite | [PR #18](https://github.com/TF-Minecraft/Woodworking/pull/18) |
| worldborder | No changes; original latest build had no warnings | Original Build workflow succeeded | — |

## Review and verification

Source and build-configuration diffs were reviewed before merge. Review checked dependency coordinates, hashes and generated POMs, API delegate behavior, model-data edge cases, serialized JSON shapes, manifests, and saved-data compatibility. New regression coverage exercises model-data snapshots and MMOCore readiness callbacks. Cooking’s documentation impact checks are included.

Merges require passing checks on the exact PR head. The owner explicitly authorized administrator merges after those checks because the repository rules require an independent approving GitHub account. Archived repositories are kept unarchived until their post-merge builds finish, then their original archived state is restored. No release was published and nothing was deployed to a Minecraft server.
