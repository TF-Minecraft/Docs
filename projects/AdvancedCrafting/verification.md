# Verification and operations

[Project index](README.md)

## Automated evidence

With Java 21 and the [build dependencies](setup.md#build-from-source) prepared,
run `mvn clean verify`. JUnit 5, MockBukkit and Mockito exercise crafting, alloys,
commands, persistence and plugin boundaries. JaCoCo checks every production class
and requires 100% instruction, branch and line coverage without exclusions.
Surefire reports are in `target/surefire-reports/`; coverage HTML, XML and CSV
are in `target/site/jacoco/`. Build CI uploads test and coverage reports; release
CI uploads coverage reports. Available reports are uploaded after failures too.
These tests do not start a live Paper server or the external plugin set.

Release CI sets Maven's version from the tag, checks the packaged plugin descriptor
against that version, and verifies the release checksum against the JAR bytes.
The descriptor receives the same version as the JAR through Maven resource
filtering. Compile ActivityTF, TFMCCore, Thievery and Recycler and run their
available tests against the matching API version.

## Server smoke checklist

Run these checks on a configured Minecraft server for the source and dependency
versions being released:

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
