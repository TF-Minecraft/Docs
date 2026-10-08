# Testing

[Project index](../README.md)

With Java 21 and Maven installed, run `mvn clean verify`. Tests exercise domain
rules, YAML persistence, and plugin workflows using JUnit 4, Mockito, and MockBukkit.
Surefire test results are in `target/surefire-reports/`.
JaCoCo measures all production classes and writes its HTML report to
`target/site/jacoco/index.html` and machine-readable results to
`target/site/jacoco/jacoco.xml`. No minimum coverage gate is enforced. The Build
workflow uploads the test and coverage reports.

Tests should assert gameplay behavior, data preservation, or failure handling.
Do not add tests solely to execute a line or manufacture unreachable states to
increase coverage. MockBukkit tests do not replace testing on a real Paper server
with the optional ItemsAdder and MMOItems integrations installed.

Adapter contract tests can also run against locally supplied plugin jars:

```sh
mvn -Ppack-api-tests clean verify \
  -Ditemsadder.jar=/path/to/ItemsAdder.jar \
  -Dfastnbt.jar=/path/to/FastNbt-jar.jar \
  -Dmmoitems.jar=/path/to/MMOItems.jar \
  -Dmythiclib.jar=/path/to/MythicLib.jar
```

These tests bind the actual API classes and mock their external operations; they
do not start those plugins. The jars remain outside this repository and are used
only on the test runtime classpath. Use the FastNbt version declared by your
ItemsAdder jar. The ordinary test suite needs none of these files.
