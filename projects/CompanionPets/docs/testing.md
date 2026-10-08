# Testing CompanionPets

Run commands from the [CompanionPets source checkout](https://github.com/TF-Minecraft/CompanionPets)
with Java 21 and Maven. See the [project index](../README.md) for dependencies.

## Automated tests

```sh
mvn clean verify
```

JUnit, MockBukkit, and Mockito exercise plugin logic, configuration, persistence,
and simulated Bukkit/provider interactions. Surefire reports are in
`target/surefire-reports/`; JaCoCo HTML, XML, and CSV reports are in
`target/site/jacoco/`. Verification requires 100% production line coverage with
no class or package exclusions, and checks that `target/jacoco.exec` and the XML
report exist. CI uploads test and coverage reports. The `coverage` profile is a
compatibility alias; ordinary verification already enforces the same gate.

These tests do not establish live Paper behaviour or correct client rendering.

## Paper integration helper

The [helper source](https://github.com/TF-Minecraft/CompanionPets/tree/main/integration-tests)
runs once, starting 240 server ticks after enabling, then disables itself when
the checks finish. It uses its own `plugins/CompanionPetsSmoke/` persistence files
and namespace, leaving live CompanionPets records alone.

Build the plugin into the local Maven repository, then compile the helper:

```sh
mvn clean install
mvn -f integration-tests/pom.xml clean package
```

If the plugin Maven version differs from `main-SNAPSHOT`, supply
`-Dcompanionpets.version=<version>` to the second command. Copy
`integration-tests/target/companionpets-smoke-1.0.0.jar` to the dev server
alongside the matching CompanionPets JAR and its configured provider plugins,
then restart dev. The server process must be able to create or write
`plugins/CompanionPetsSmoke/`; prepare this isolated directory with the server
account's ownership if the plugins directory is not writable.

The helper spawns temporary entities near the first world's spawn, loads and
temporarily force-loads chunks, and places stone test platforms in air for native
movement checks. Its disable handler removes test entities and isolated records,
restores the platforms' original blocks, and releases the chunks it force-loaded.
Cleanup failures are reported as failures.

Look for `COMPANIONPETS_INTEGRATION PASS checks=...` or
`COMPANIONPETS_INTEGRATION FAIL` in the server log. PASS is emitted only after
the checks and cleanup succeed. Checks use the active configuration:

- Bodies, egg identity, model attachment, and available mapped/custom clips.
- Native AI pause/resume, Follow navigation, frozen needs, and postures held
  across 180 native ticks.
- Adoption and body restoration without losing learning, default learned Follow,
  and modeled wolves starting shake with the native shake clock.
- Duplicate removal, owner/staff Pet House actions, confirmed release and heal,
  and removal of model registrations and modeled owners.
- Toy landing, offline return with original data, stale projectile rejection,
  and configured provider IDs and required animations.

Keep the helper's staff audit and deletion journal with the log as test evidence.
Remove the helper JAR after running; an installed helper runs again at the next
server restart. CI compiles the harness but does not execute these Paper checks.
Client rendering still needs a separate in-game check.
