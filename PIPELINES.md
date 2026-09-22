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

### Release presentation

Use the exact tag as the release title, such as `v2.0.1` or `v0.2.1`.
Every release uses the same two top-level sections:

- **Changes**: concise user-facing changes. The first release starts with
  `Initial release.`; later drafts include generated changes for review.
- **Downloads**: links to the attached runtime JAR or archives, followed by
  `SHA256SUMS` and `build.json`.

Keep project versions independent. Active plugins run in production and use stable
numeric release versions. Nutrition retains its historical BETA release while archived.
Do not add project names, build timestamps, or feature subtitles to release
titles. Put compatibility requirements and relevant limitations in the Changes
section. Source-only releases must say explicitly that they contain no plugin
binary. Apply this format to manually published releases as well as automated
drafts.

`build.json` records the source commit, repository, tag, workflow run, JAR name,
checksum, and dependency inputs. Locally built releases record their build
method and use `run: null`. Verify draft assets before publication. Release
publication does not deploy a Minecraft server.

All plugins target **Java 21 / Minecraft 1.21.10**; see the
[shared platform baseline](PLATFORM.md).

## Build dependencies

Plugins with file dependencies use `.github/scripts/prepare-release.sh` to download their private build inputs from a pinned commit in [ServerAssets](https://github.com/TF-Minecraft/ServerAssets). The committed `.github/dependencies.sha256` verifies the downloaded bytes. JARs go in `libs/`, outside Maven's cleaned `target/` directory, and are ignored by Git.

After download, `prepare-release.sh` calls
`.github/scripts/install-local-dependencies.sh`. This script verifies every pinned
checksum before installing the JARs into the local Maven repository using
`maven-install-plugin:3.1.4`. POMs declare these inputs with `provided` scope;
versions end in `-tfmc-<first 12 SHA-256 characters>` so different private JARs
cannot overwrite one another under the same Maven coordinates. Generated POMs
have no transitive dependencies. The input bytes and runtime plugin requirements
are unchanged.

For already downloaded `libs/`, run
`bash .github/scripts/install-local-dependencies.sh`. Pass Maven
options such as `-Dmaven.repo.local=/path/to/cache` to either preparation script
and to the subsequent build. Keep the checksum file, install commands, and POM
versions together when updating an input. Rollback consists of reverting those
files together; no runtime data migration is involved.

`DEPS_TOKEN` is an organisation Actions secret with Contents read access to ServerAssets. Grant the consuming repositories access to this one secret. A separate token for each repository is unnecessary. The workflow passes it only to dependency preparation steps. Fork pull requests do not receive Actions secrets and cannot run builds that require these private inputs.

Shared TFMC plugins use their Maven coordinates with `provided` scope.
Development and release workflows run the
[shared plugin installer](https://github.com/TF-Minecraft/TLibs/blob/main/DEPENDENCIES.md)
with `mode: pinned`. It resolves each direct dependency at the version committed
in the POM, verifies the JAR checksum, and installs a minimal Maven POM. The action
is pinned to a reviewed commit SHA. Provider build dependencies are not installed
recursively or shaded into consumers.

Shared APIs use public source-built releases. Active providers, including Cooking
and InteractibleFurniture, use stable releases.
Drafts and development artifacts are excluded. Missing releases, artifacts,
credentials, or matching checksums fail the build. Public release lookup uses
`github.token`; licensed third-party inputs use `DEPS_TOKEN`.

Builds record coordinates, checksums, and sources in
`.build/plugin-dependencies.json`. Development artifacts preserve this file;
release metadata includes the same inputs in `build.json`. Local builds use:

```sh
python3 ../tlibs/tools/install-plugins.py --pom pom.xml --mode pinned
```

To upgrade dependencies, run the installer locally with `--mode latest`, review
the POM changes, and commit the chosen versions. Build consumers against matching
provider packages before releasing the dependent set.

ServerAssets' `manifest.json` is authoritative for filenames, hashes, embedded plugin versions, and sources. Keep licensed dependency JARs in that private repository and out of public release assets.

## Workflow configuration

Plugin repositories contain `build.yml`, `release.yml`, and the reusable `maven-release.yml` under `.github/workflows/`. The release caller selects the JDK and passes `DEPS_TOKEN` explicitly where needed.

Both development and release jobs obtain the runtime JAR path from Maven's
`project.build.finalName`: `target/<finalName>.jar`. The usual Maven name is
`<artifactId>-<version>`. Runtime filenames must use a lowercase alphanumeric
plugin name followed by the version: `<name>-<version>.jar`. Do not add underscores,
word separators or a `-plugin` suffix. Examples are `tlibs-2.0.0.jar`,
`archaeo-1.0.1.jar` and `geigercounters-2.0.0.jar`. A POM `finalName` override
normalizes legacy Maven artifact IDs without changing dependency coordinates.
Keep that filename decision in the POM. Bukkit identifiers and data-folder names
remain stable; the filename convention does not rename them. Shaded plugins replace the main
runtime JAR; `original-*`, sources and test JARs are not release artifacts.

The identical `.github/scripts/plugin-artifact.py` helper in each plugin
repository checks the lowercase alphanumeric filename, resolved JAR path, archive integrity, and embedded
`plugin.yml` or `paper-plugin.yml` version before either build type uploads it.
Releases use the same helper to stage the runtime JAR, `SHA256SUMS` and
`build.json`, including resolved plugin dependency metadata where applicable.
Both build types run Maven verification with tests enabled and the
`deploy-live` profile disabled.

Plugin `.gitignore` files share rules for build output, downloaded JARs, Maven
backup files, dependency-resolution metadata, IDE files and local caches.
Maven wrapper JARs and launchers, source/tests, dependency checksums and README
files remain trackable. Repository-specific runtime data exclusions follow the
common rules. BreedingBuddies shares the ignore rules but remains a source-only
archived project without a supported plugin release workflow.

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
