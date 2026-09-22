# Setup, builds and releases

[Project index](README.md)

## Runtime setup

Use Java 25 and a compatible Minecraft 1.21 server. The plugin descriptor requires
TLibs, MMOCore, MMOItems and MythicLib. The build uses the 1.21.8 Spigot API; the
older `api-version: 1.20` descriptor is not a promise of Java 17 or 1.20 runtime
compatibility. Configured ItemsAdder furniture requires ItemsAdder and the matching
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

Requires Java 25, Maven, Python 3 and authorised Contents read access to private
ServerAssets. Clone TLibs next to the source checkout as `../tlibs`:

```sh
python3 ../tlibs/tools/install-plugins.py --pom pom.xml
GH_TOKEN="$(gh auth token)" bash .github/scripts/prepare-release.sh
mvn clean verify
```

The default output is `target/advancedcrafting-1.2.2.jar`. TLibs uses Maven
`provided` scope; third-party API inputs are checksum-pinned in the private
preparation script. No licensed JARs are committed or bundled with the release.
The original developer's absolute Windows paths and package-time copies are removed.

## Releases

PR and main builds verify the source and upload a `DEV-YYYYMMDD-HHmm` JAR plus
exact shared dependency metadata. `v1.2.2` and later numeric tags must match the
committed Maven version. The tag workflow creates a draft release with the JAR,
`SHA256SUMS`, and `build.json` containing source and resolved dependency provenance.
Inspect the draft before publication. Use a new version for corrections; never
replace an existing published version's bytes.

The source archive SHA-256 and import changes are recorded in
[SOURCE.md](https://github.com/TF-Minecraft/AdvancedCrafting/blob/main/SOURCE.md).
The archive supplied no Git history or license file; no new license is inferred.
