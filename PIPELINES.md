# Builds and releases

Plugin pull requests into `main` run Maven verification with Java unit tests enabled. CoreProtect also builds pull requests into its default branch, `master`. A failed test fails the build. Test reports are uploaded when present, including after test failures; repositories without test sources report no tests.

Development builds use `DEV-YYYYMMDD-HHmm`, with the date and time in UTC. The runtime JAR filename and embedded plugin version match, for example `armourshop-DEV-20260922-1500.jar` and `DEV-20260922-1500`. The numeric version in the committed POM remains the release version. GitHub artifact names include the run ID and attempt to distinguish builds within the same minute.

## Plugin releases

1. Set the numeric release version in `pom.xml`. Keep the plugin descriptor's version as `${project.version}` so Maven supplies it.
2. Push a matching tag, such as `v1.2`, `v1.2.3`, or `v1.2.3-rc.1`.
3. The release workflow checks the tag against the POM, prepares dependencies, and runs `mvn clean verify` with tests enabled and the `deploy-live` profile disabled.
4. It validates and uploads the exact runtime JAR, `SHA256SUMS`, and `build.json` to a draft GitHub release.
5. Download and inspect the artifacts, review the generated notes, and publish the draft.

Tags with prerelease suffixes create prereleases. Snapshot versions are rejected. An existing release causes the run to fail; use a new version for corrections. The workflow does not deploy to a Minecraft server.

`build.json` records the source commit, repository, tag, workflow run, JAR name, and checksum. Only the publishing job has repository write permission; the build job has read access.

## Build dependencies

Each plugin's `.github/scripts/prepare-release.sh` downloads its private build inputs from a pinned commit in [ServerAssets](https://github.com/TF-Minecraft/ServerAssets). The committed `.github/dependencies.sha256` verifies the downloaded bytes. JARs go in `libs/`, outside Maven's cleaned `target/` directory, and are ignored by Git.

`DEPS_TOKEN` is an organisation Actions secret with Contents read access to ServerAssets. Grant the consuming repositories access to this one secret. A separate token for each repository is unnecessary. The workflow passes it as `GH_TOKEN` only to the dependency preparation step. Fork pull requests do not receive Actions secrets and cannot run builds that require these private inputs.

ServerAssets' `manifest.json` is authoritative for filenames, hashes, embedded plugin versions, and sources. Keep licensed dependency JARs in that private repository and out of public release assets.

## Workflow configuration

Plugin repositories contain `build.yml`, `release.yml`, and the reusable `maven-release.yml` under `.github/workflows/`. The release caller selects the JDK and exact runtime artifact path; `{version}` expands to the numeric tag without `v`. It passes `DEPS_TOKEN` explicitly where needed. Select the shaded runtime JAR for plugins that use shading.

Workflows use Ubuntu 24.04 and actions with Node.js 24 runtimes. The Java version is chosen for the repository and its compiled dependencies. This does not change the runtime compatibility promised by the plugin's source configuration.

## Documentation and assets

Docs checks relative links in the project indexes and builds CoreProtect's MkDocs site in strict mode. Development artifacts contain the documentation source archive, generated CoreProtect site, and checksums, named with the same UTC timestamp format.

ServerAssets verifies every entry in its file manifest before uploading a timestamped source archive and checksums. Its artifacts retain the private repository's access controls.

Both repositories accept numeric `v*` tags for archive releases. The same verification runs before packaging the tagged source, checksums, and `build.json` into a draft release. Archive versions come from the tag; these repositories do not have Maven versions to match.

## Verification scope

A successful pull request build verifies compilation, available unit tests, and packaging. Check the downloaded JAR's embedded version as well as its filename. A tagged release run additionally verifies draft publication and release assets. Minecraft runtime and integration tests are separate checks.
