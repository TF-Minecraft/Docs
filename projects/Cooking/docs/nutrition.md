# Nutrition and character sessions

[Cooking](../README.md) · [All projects](../../../README.md)

Cooking uses TLibs 2.3.0's shared character sessions with RPCharacters 2.16.0. A session identifies the account, character UUID and activation generation. Switching away and back to the same character creates a new session; reconnecting also replaces the player connection. See the [shared identity API](../../TLibs/character-identity.md).

## Readiness and storage

Nutrition requires a ready shared session and the matching RPCharacters character object, including its owner. A registered provider with no ready session means selection or loading is still in progress. Cooking skips nutrition reads, saves, HUD updates and attribute changes until the character is ready.

`CharacterSessionStartEvent` initializes nutrition after activation. Cooking also initializes players already ready when its startup task runs. Join delays and the legacy character activation event do not initialize nutrition.

RPCharacters still stores `food-value`, `raw-diet-score`, `diet-score` and `last-diet-tier` in its character data. Meal variety keeps the existing player persistent-data key `cooking:variety_history` and format; this integration does not move it into character JSON. Food, diet, variety, drain intervals and attribute calculations keep their existing configuration.

Ordinary Minecraft death applies the configured respawn food, except during a started battle, when food is preserved. Ending a character session does not itself reset nutrition. Respawn updates the HUD only for a ready character.

Nutrition work retains its original session through save, HUD and MMOCore callbacks. If a callback changes the character, remaining writes stop. HUD synchronization suppression belongs to the current session, so an outgoing update cannot suppress a replacement character's events.

## Player actions and furniture

Vanilla food and milk-cup nutrition runs on the following tick, after consumption, and only if the original session is still current and the consumption event remained uncancelled. Milk buckets use custom consumption: the bucket is spent before nutrition callbacks.

Queued player actions retain both their original session and player connection. Milk conversion, empty-cup replacement, saturation updates, CustomCrops inventory conversion and bundle stacking stop when either changes. A provider appearing or disappearing also invalidates queued work. When no identity provider is registered, these item actions can operate without a character; nutrition still requires RPCharacters and a ready session. When a provider is registered but the player is pending selection, Cooking skips these inventory updates and refuses new Cooking food consumption, hoe harvests and sausage cranks.

Hoe harvesting checks the session around crop events and conversion. It builds the drops before removing the crop. After harvesting has committed, remaining output goes to the original crop location if the player is no longer current. A delayed replant that loses its session returns the reserved seed there instead of planting for a replacement character.

Sausage completion retains the session that started the crank. A stale completion leaves the unconsumed meats and casing in place. Once completion consumes the inputs, any output that cannot go to the original player drops at the captured station location. Furniture processing and world-owned timers continue independently of character sessions.

## Verification

Run `mvn clean verify` with the pinned dependencies. The tests exercise absent and pending providers, shared activation, owner/UUID mismatches, repeated activation of the same character, reconnects and session changes inside nutrition or item callbacks. Coverage reports are in `target/site/jacoco/`.

On a test server, verify food and HUD state after selection, switching, reconnecting and ordinary death. Start a harvest or sausage crank, switch before its delayed work completes, and verify that the replacement character receives no old player action. Check the original crop or station for committed output and reserved seeds. Verify furniture processing continues while its initiating player is offline. Automated tests do not replace these integration checks with Paper, RPCharacters, MMOCore and the configured item/furniture providers.
