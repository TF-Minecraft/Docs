# Automated tests and coverage

Run from the [Thievery source checkout](https://github.com/TF-Minecraft/Thievery)
with Java 21 and the pinned dependencies prepared according to the
[shared build guide](../../../PIPELINES.md#build-dependencies):

```sh
mvn -B --no-transfer-progress clean verify
python3 .github/scripts/check-test-reports.py
```

JUnit, MockBukkit and Mockito exercise configuration, persistence, inventory
transfers, ownership rules, commands, plugin lifecycle and theft sessions.
Fixtures use temporary directories; legacy relative persistence paths are
isolated under `target/test-runtime`. External plugin APIs use mocks or fixtures.
Optional RPCharacters API compatibility uses a separately loaded fixture to
model servers with and without that API.

Surefire writes test results to `target/surefire-reports/`. JaCoCo includes every
production class and writes `target/site/jacoco/index.html` and
`target/site/jacoco/jacoco.xml`. The `verify` phase requires 100% instruction,
line, branch, method and class coverage with no production exclusions. The
report checker requires test reports and rejects skipped tests; Maven fails
on test failures and errors. CI runs both commands; the Build workflow uploads
both report folders.

Use a clean full run for combined coverage. Focused tests are useful during
development but do not establish the full suite's coverage. Tests should assert
observable contracts or regressions, including real configuration, metadata
and integration failures. Do not add impossible inventory states or invoke
private constructors solely to raise coverage. MockBukkit's unimplemented
operations can appear as skipped tests, so a passing coverage run must also
have zero skipped tests.

Live Paper gameplay and integration checks remain separate. Use the
[manual test matrix](TEST_MATRIX.md) and record the actual server, dependency
set and results with the release.
