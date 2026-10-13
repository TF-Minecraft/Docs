# Automated tests and coverage

Run from the [Thievery source checkout](https://github.com/TF-Minecraft/Thievery)
with Java 21 and the pinned dependencies prepared according to the
[shared build guide](../../../PIPELINES.md#build-dependencies):

```sh
tfmc-mvn -o -B --no-transfer-progress clean verify
python3 .github/scripts/check-test-reports.py
```

JUnit, MockBukkit and Mockito exercise configuration, persistence, inventory
transfers, ownership rules, commands, plugin lifecycle and theft sessions.
Fixtures use temporary directories; legacy relative persistence paths are
isolated under `target/test-runtime`. External plugin APIs use mocks or fixtures.
Optional RPCharacters API compatibility uses a separately loaded fixture to
model servers with and without that API.

Trait tests register the shared character service and cover absent providers,
pending sessions, unknown character information, character switching, and current
trait changes, and mixed-case configured traits. Container and display tests
exercise the shared checker before clue checks or lockpick start. Plugin lifecycle
tests start Thievery without the character API and check that its protection
listeners register while trait checks deny. Robbery tests cover requests made as
one character and accepted after switching away and back, and pending requests
expiring when either session ends.

Pouch payment tests use real temporary SQLite files for balanced transfers,
ledger reopen, a committed payment with a lost reply, insufficient funds and
stale sessions. Handler tests repeat the same click, retry unavailable payments,
and verify that unsavable intents consume no budget. Identity tests check
member-to-account cooldown mapping and faction waiting.

Lock owner tests use temporary directories for real lock files. They cover the
migration (classification, exact-byte journal hashes, the archive, a second boot,
quarantine retry, stragglers, an exception mid-pass, every replay case and
`data-version`), the guard freeze in each data manager and handler, fail-closed
parsing, access for characters, alts, dead owners and server locks, double chests,
block hoppers and hopper minecarts, target keys and the staff lock commands.
Estate tests (`EstateLockPassTest`, `TLibsLockEstatesTest`) cover every record and
lock state mapping, waiting and frozen parts, double chests, files the migration
claims in the same pass, a planner failure that still reaches normal operation, the
report from the state after the pass, the runtime answer for later revisions, a
crashed estate pass replayed while the estate still applies and after it no longer
does, and the old-jar journal case. `LockStartupTest` runs one estate end to end
through the real TLibs facade with mocked services.
`FactionFixture` gives each mocked player a character whose ID is their account
UUID; `plays(player, id)` switches it, and its `guilds` field stands in for
SimpleFactions' `lockGuild`. A JUnit extension starts every test with locks in
normal mode, no guild source and an empty quarantine list.

The offline rollback tool has Python tests in `tools/test_thievery_rollback.py`, run
with `python3 -m unittest discover -s tools -p 'test_*.py'` and in CI after the Maven
build. They build a fixture laid out as the migration writes it, with two journals,
and cover the dry run, newest-first restores across both passes, changed, missing and
mismatched files, marker removal, and journals or archives that cannot be trusted.
Estate fixtures add `--estate-only` (estate entries only, markers kept), entries
skipped at replay, and estate entries an older jar rewrote without their kind.

Hands-up inspection tests exercise consent, independent item copies and live
refresh, full-view click and drag cancellation, creative inventory events,
robbery/pickpocket event ordering, range and visibility checks, cancelled opens,
multiple viewers, and cleanup when a participant leaves or changes character.
ItemsAdder tests check actual-animation confirmation, missing/refused starts,
API failures, stopping only the owned pose, and end-event cleanup without
recursively stopping ItemsAdder. Plugin lifecycle tests cover ItemsAdder present
and absent. Asset export verification runs in ServerAssets.
Client inventory prediction and interactions with the full live plugin set
still need the hands-up checks in the manual matrix.

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
