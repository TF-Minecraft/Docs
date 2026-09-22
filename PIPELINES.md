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

Plugins with file dependencies use `.github/scripts/prepare-release.sh` to download their private build inputs from a pinned commit in [ServerAssets](https://github.com/TF-Minecraft/ServerAssets). The committed `.github/dependencies.sha256` verifies the downloaded bytes. JARs go in `libs/`, outside Maven's cleaned `target/` directory, and are ignored by Git.

`DEPS_TOKEN` is an organisation Actions secret with Contents read access to ServerAssets. Grant the consuming repositories access to this one secret. A separate token for each repository is unnecessary. The workflow passes it only to dependency preparation steps. Fork pull requests do not receive Actions secrets and cannot run builds that require these private inputs.

Shared TFMC plugins use their native Maven coordinates with `provided` scope. Development and release workflows run the [shared plugin installer](https://github.com/TF-Minecraft/TLibs/blob/main/DEPENDENCIES.md) with `mode: latest`. It resolves each direct declared plugin dependency, verifies the JAR's SHA-256, installs its actual Maven version with a minimal POM, and updates the checkout's version properties after all inputs succeed. The action implementation remains pinned to a full commit SHA. Providers' build dependencies are not recursively installed or shaded; this handles existing source dependency cycles without requiring recursive builds.

Stable plugins use GitHub's latest published release. Cooking and InteractibleFurniture explicitly permit their existing ALPHA/BETA release channels. Drafts and DEV artifacts are excluded. A missing release, asset, credential or checksum mismatch fails the build. Publishing a release promotes that API to future builds; it does not deploy anything to a Minecraft server.

AdvancedCrafting now uses public source-built releases from its new repository, starting at 1.2.2; its old private 1.2.1 remains available only for pinned rollback. MusicalInstruments 2.5 remains a private, checksum-pinned ServerAssets input. Its repository has version 2.4 without the `InstrumentPlayEvent` API used by ActivityTF; the accessible Drefvelin branches did not contain the missing source. Those consumers pass `DEPS_TOKEN` as the action's `private-token`; public release lookup uses the separate default GitHub token.

Every migrated build records exact coordinates, checksums and sources in `.build/plugin-dependencies.json`, uploaded alongside its development JAR. Tagged releases include that list in `build.json`. Local builds use `python3 ../tlibs/tools/install-plugins.py --pom pom.xml`; add `--mode latest` to update local version properties, or use the default `--mode pinned` and versions from a successful build's metadata for reproducible API selection. The private inputs also require `TFMC_PRIVATE_TOKEN` or `--assets /path/to/server-assets`.

Archaeo's initial API release `v1.0.1` was built from unchanged source and records its source commit and checksum. Its existing embedded plugin descriptor still says `1.0`; this is documented in the release metadata. It has no automated release workflow yet.

ServerAssets' `manifest.json` is authoritative for filenames, hashes, embedded plugin versions, and sources. Keep licensed dependency JARs in that private repository and out of public release assets.

## Workflow configuration

Plugin repositories contain `build.yml`, `release.yml`, and the reusable `maven-release.yml` under `.github/workflows/`. The release caller selects the JDK and exact runtime artifact path; `{version}` expands to the numeric tag without `v`. It passes `DEPS_TOKEN` explicitly where needed. Select the shaded runtime JAR for plugins that use shading.

Workflows use Ubuntu 24.04 and actions with Node.js 24 runtimes. The Java version is chosen for the repository and its compiled dependencies. This does not change the runtime compatibility promised by the plugin's source configuration.

## Documentation and assets

Docs checks local links and section anchors in every Markdown page, verifies navigation between the project list and project indexes, and builds CoreProtect's MkDocs site in strict mode. Development artifacts contain the documentation source archive, generated CoreProtect site, and checksums, named with the same UTC timestamp format.

ServerAssets verifies every entry in its file manifest before uploading a timestamped source archive and checksums. Its artifacts retain the private repository's access controls.

Both repositories accept numeric `v*` tags for archive releases. The same verification runs before packaging the tagged source, checksums, and `build.json` into a draft release. Archive versions come from the tag; these repositories do not have Maven versions to match.

## ProvinceSystem

PRs run frontend Vitest and backend pytest suites, upload JUnit reports, and build the Next.js frontend. CI uses Node 22 and Python 3.12; the backend tests use SQLite's connection-limit testing API. A failed suite prevents application artifact publication.

Development artifacts include timestamped source and frontend archives, checksums, and build metadata. Both archives share the same root directory; extracting the frontend archive over the source archive supplies the compiled `.next` output and generated public assets. Dependencies and configuration must be installed separately to run the application.

The frontend bundle uses `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000` at build time. Build with the intended URL for a deployment that needs a different API endpoint. The pipeline does not deploy the application.

Numeric `v*` tags must match `frontend/package.json`. The release workflow runs the same tests and build, then creates a draft archive release.

## Verification scope

A successful pull request build verifies compilation, available unit tests, and packaging. Check the downloaded JAR's embedded version as well as its filename. A tagged release run additionally verifies draft publication and release assets. Minecraft runtime and integration tests are separate checks.
