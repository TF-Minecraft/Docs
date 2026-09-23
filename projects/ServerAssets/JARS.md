# Plugin and API jars

The private [ServerAssets manifest](https://github.com/TF-Minecraft/ServerAssets/blob/main/manifest.json)
is the authoritative inventory of stored jars, filenames, versions, roles and
SHA-256 checksums. Repository access is required.

Use each plugin's committed POM, `.github/scripts/prepare-release.sh` and
`.github/dependencies.sha256` for its build inputs. Shared TFMC plugin dependencies
come from the releases selected by the POM through the
[shared installer](../../PIPELINES.md#build-dependencies).

The manifest's `runtime` mapping lists stored runtime plugin binaries;
`build_dependencies` records aliases for stored build inputs.
A stored binary or dependency alias does not identify the current source version.
Build the TFMC plugins from `main` and record the exact jars used for runtime tests.

See [asset verification](overview.md#verify-assets).
