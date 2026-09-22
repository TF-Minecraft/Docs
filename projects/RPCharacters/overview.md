# RPCharacters

Roleplay characters, identity, progression and character state. Build and run with **Java 21** and **Minecraft 1.21.10**, following the [shared platform baseline](../../PLATFORM.md). The POM uses compiler release 21 and Paper API `1.21.10-R0.1-SNAPSHOT`; the plugin loader declaration is `api-version: 1.21.10`.

## Dependencies

TLibs and SimpleFactions resolve as Maven plugin artifacts at the versions declared in `pom.xml`. The shared `setup-plugins` action installs those versions. For a local build, check out TLibs `main` alongside the source and run `python3 ../tlibs/tools/install-plugins.py --pom pom.xml --mode pinned`. The installer verifies release checksums; see [TLibs dependency setup](../TLibs/README.md). Runtime optional integrations can still be mandatory compile dependencies.

The remaining private reference jars are ItemsAdder 4.0.18, MMOCore 1.13.1, MMOItems, MythicLib, ProtocolLib and MythicMobs. Populate the exact paths listed in `pom.xml` under the ignored `libs/` directory. `.github/scripts/prepare-release.sh` downloads pinned files from private `TF-Minecraft/ServerAssets` and verifies `.github/dependencies.sha256`. It requires `GH_TOKEN` with read access; CI supplies the `DEPS_TOKEN` secret. Keep licensed jars private.

## Local build

Run from the source checkout with JDK 21:

```sh
mvn -B --no-transfer-progress clean verify
```

Output: a JAR under `target/` using the version declared in `pom.xml`. Use `mvn clean install` when another local plugin needs this build. Maven packaging does not deploy to a live server.

## CI and releases

The current build workflow runs for pushes and pull requests to `main`. It installs shared plugin dependencies, prepares the pinned private jars, assigns a dated `DEV-...` version, and runs tests and packaging. Artifacts contain the jar and `.build/plugin-dependencies.json`; unit-test reports are uploaded separately when present. Jar filenames therefore follow the selected Maven version.

The separate release workflow delegates to the shared Maven release workflow. Keep the dependency properties, private download script and `.github/dependencies.sha256` aligned when changing dependencies.
