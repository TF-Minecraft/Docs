# Verification and operations

[Project index](README.md)

## Automated evidence

The supplied archive contains no unit tests. `mvn clean verify` checks source
compilation and packaging; a successful build must not be described as gameplay
coverage. CI uses Java 25 and publishes test reports if tests are added later.
The first public import preserves the supplied Java sources byte-for-byte.

Release checks verify that the tag matches Maven, the JAR has a plugin descriptor,
and the release checksum matches its bytes. The descriptor receives the same
version as the JAR through Maven resource filtering. ActivityTF, TFMCCore,
Thievery and Recycler compile and run their available tests against the API as
part of the cross-repository migration.

## Server smoke checklist

These checks require a configured Minecraft server and have not been performed
as part of the repository import:

1. Start with all declared dependencies and the configured recipes/schemes; inspect startup logs.
2. Open each configured crafting, alloy and ingredient-conversion station.
3. Craft an item and apply smithing hits; confirm quality, lore, stats and ingredient use.
4. Forge the same alloy twice; check the crafted event both times and discovery only on the first recorded forge.
5. Exercise ActivityTF/TFMCCore listeners and the Recycler/Thievery integrations.
6. Restart after a clean stop; confirm station progress, alloys, revision state and per-player discovery survive.
7. Test admin inspection and refresh with permissions, then with an ordinary player.

For startup null-list failures, verify that all four scheme/recipe directories
from [setup](setup.md#runtime-setup) exist. For missing item models or templates,
check TLibs item paths and the server's MMOItems/ItemsAdder assets. For refresh
issues, enable `debug-stat-refresh` temporarily and inspect `[AC][StatRefresh]` logs.

Rollback means stopping the server, restoring the previous plugin JAR and the
matching data backup when needed, then restarting. Keep one AdvancedCrafting JAR
in the plugin directory. Build/release workflows perform no runtime deployment.
