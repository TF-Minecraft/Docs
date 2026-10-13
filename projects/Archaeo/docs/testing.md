# Testing

[Project index](../README.md)

With Java 21 and Maven installed, run `tfmc-mvn -o -B clean verify`. Tests exercise domain
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

Ownership fixtures use distinct characters on one account, stale/wrong-account
providers, captured menu/session ends, timed sampling/mining/sketch boundaries,
raw migration/save/restart preservation, publication failure cuts, and estate
revision/revival/re-death guards. They verify full replay semantics, cumulative
receipts, restored-source refusal and placement intent before kit/world effects.
These are bounded synthetic proofs; they do not replace RPCharacters body-switch
and custom-pack tests on Paper, or establish arbitrary-crash inventory atomicity.

Run the conservative offline-recovery fixtures from the source checkout with
Python 3 and PyYAML:

```sh
python3 -m unittest discover -s tools -p 'test_site_ownership.py'
```

The 14 recovery fixtures cover exact CRLF originals, unknown binary/null fields, verified full backups,
semantic corruption, invalid later journals, gameplay drift and retained
estate/placement evidence. See [ownership and recovery](character-ownership.md)
for the operator procedure.
