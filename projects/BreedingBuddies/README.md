# BreedingBuddies

[Source repository](https://github.com/TF-Minecraft/BreedingBuddies) · [All projects](../../README.md)

Owned farm animals with daily care, friendship, inherited genetics, stable chunks and mount breeding.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Run Maven with **JDK 21** from the source checkout. The POM sets
`maven.compiler.release=21` and resolves
`io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope from
the PaperMC Maven repository. The plugin descriptor declares
`api-version: '1.21.10'`.

BreedingBuddies has no shared TFMC plugin dependencies, so the TLibs installer
is not needed. Its private build inputs are MMOItems `6.10.1-SNAPSHOT`,
MythicLib `1.7.1-SNAPSHOT` and json-simple `1.1.1`, pinned in
`.github/dependencies.sha256`. `.github/scripts/prepare-release.sh` downloads
them from ServerAssets and installs them into local Maven under hash-qualified
versions. In Bash:

```bash
(read -rsp 'ServerAssets token: ' GH_TOKEN && echo && export GH_TOKEN &&
  bash .github/scripts/prepare-release.sh) &&
  mvn clean verify
```

The token needs Contents read access to TF-Minecraft/ServerAssets; CI supplies
it from `DEPS_TOKEN`. See [build dependencies](../../PIPELINES.md#build-dependencies).
`mvn clean verify` also runs the unit tests in `src/test/java`. The JAR is
written to `target/breedingbuddies-<version>.jar`; nothing is shaded into it.

At runtime, `plugin.yml` requires MMOItems and MythicLib. Gameplay checks on a
Paper 1.21.10 server remain separate from build verification.

## Guides

- [Behaviour, configuration and operations](overview.md) — ownership, care,
  genetics, stable chunks, the daily change, bundles, mounts, commands and saved data

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts,
release tags and dependency access. Pull requests build
`breedingbuddies-DEV-<UTC date>-<UTC time>.jar`; `main` uses `main-SNAPSHOT`.
Version tags create a verified draft release with the runtime JAR, checksums
and build metadata.
