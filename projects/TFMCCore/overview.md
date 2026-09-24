# TFMCCore

Shared gameplay systems and statistics integrations. Build and run with **Java 21** and **Minecraft 1.21.10**, following the [shared platform baseline](../../PLATFORM.md). The POM uses compiler release 21 and Paper API `1.21.10-R0.1-SNAPSHOT`; the plugin loader declaration is `api-version: 1.21.10`.

## Dependencies

TLibs, VehicleFramework, RPCharacters, AdvancedCrafting and SimpleFactions resolve as Maven plugin artifacts at the versions declared in `pom.xml`. The shared `setup-plugins` action installs those versions. For a local build, check out TLibs `main` alongside the source and run `python3 ../tlibs/tools/install-plugins.py --pom pom.xml --mode pinned`. The installer verifies release checksums; see [TLibs dependency setup](../TLibs/README.md). Runtime optional integrations can still be mandatory compile dependencies.

The remaining private reference jars are MMOCore 1.13.1 and MythicLib. `.github/scripts/prepare-release.sh` downloads the pinned files listed in `.github/dependencies.sha256` from private `TF-Minecraft/ServerAssets` into the ignored `libs/` directory, then runs `install-local-dependencies.sh`, which verifies the checksums and installs each jar into the local Maven repository. It requires `GH_TOKEN` with read access; CI supplies the `DEPS_TOKEN` secret. Keep licensed jars private.

## Local build

Run from the source checkout with JDK 21:

```sh
mvn -B --no-transfer-progress clean verify
```

Output: a JAR under `target/` using the version declared in `pom.xml`. Use `mvn clean install` when another local plugin needs this build. Maven packaging does not deploy to a live server.

## CI and releases

The current build workflow runs for pushes and pull requests to `main`. It installs shared plugin dependencies, prepares the pinned private jars, sets the version to `main-SNAPSHOT` (a dated `DEV-...` version for pull requests), and runs tests and packaging. Pull request artifacts contain the jar and `.build/plugin-dependencies.json`; unit-test reports are uploaded separately when present. Jar filenames therefore follow the selected Maven version.

The separate release workflow delegates to the shared Maven release workflow. Keep the dependency properties, private download script and `.github/dependencies.sha256` aligned when changing dependencies.
