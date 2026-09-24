# Setup, builds and releases

[Project index](README.md)

## Runtime setup

Use Java 21 and Minecraft 1.21.10 under the [shared platform baseline](../../PLATFORM.md).
The plugin descriptor requires TLibs, MMOCore, MMOItems and MythicLib. The
build resolves Paper API 1.21.10 from Maven and declares `api-version: 1.21.10`. Configured ItemsAdder furniture requires ItemsAdder and the matching
server assets. These third-party plugins are installed separately.

For a new server, while stopped, create `plugins/AdvancedCrafting/` and copy the
`recipes/`, `colour-schemes/`, `model-schemes/` and `naming-schemes/` directories
from the source's `src/main/resources/` into it. Adapt the examples to the server's
MMOItems templates and item paths. The current bootstrap loads these directories
but does not extract their contents automatically; it also does not create the
model-schemes directory. Top-level default YAML files are copied only when missing.
Do not overwrite existing production configuration or data during this step.

Place one AdvancedCrafting release JAR in `plugins/`, start the server, and check
startup logs and configured station interactions. Back up the entire plugin data
folder before upgrading. Publication and CI never deploy to a running server.

## Build from source

Requires Java 21, Maven, Python 3 and authorised Contents read access to private
ServerAssets. Build from `main`. Clone TLibs `main` next to
the source checkout as `../tlibs`:

```sh
python3 ../tlibs/tools/install-plugins.py --pom pom.xml --mode pinned
GH_TOKEN="$(gh auth token)" bash .github/scripts/prepare-release.sh
mvn clean verify
```

Pinned mode installs the versions declared in the POM. The
[shared baseline](../../PLATFORM.md) lists the shared API versions.

Maven writes the JAR under `target/` using the version declared in `pom.xml`.
TLibs uses Maven `provided` scope; third-party API inputs are checksum-pinned
in the private preparation script. Licensed JARs are not bundled with the release.

## Releases

PR and main builds verify the source and upload a `DEV-YYYYMMDD-HHmm` JAR plus
exact shared dependency metadata. Numeric tags must match the
committed Maven version. The tag workflow creates a draft release with the JAR,
`SHA256SUMS`, and `build.json` containing source and resolved dependency provenance.
Inspect the draft before publication. Use a new version for corrections; never
replace an existing published version's bytes.
