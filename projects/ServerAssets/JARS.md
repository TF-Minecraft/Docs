# Plugin and API jars

The private [ServerAssets manifest](https://github.com/TF-Minecraft/ServerAssets/blob/main/manifest.json)
is the authoritative inventory of stored jars, filenames, versions, roles and
SHA-256 checksums. Repository access is required.

Use each plugin's committed POM, `.github/scripts/prepare-release.sh` and
`.github/dependencies.sha256` for its build inputs. Shared TFMC plugin dependencies
come from the releases selected by the POM through the
[shared installer](../../PIPELINES.md#build-dependencies).

All binaries live under `jars/<first 12 SHA-256 characters>/<name>-<version>.jar`.
The manifest's `runtime` and `build_dependencies` mappings identify uses of those
same files; they do not refer to separate copies or directories.
A stored binary or dependency alias does not identify the current source version.
Build the TFMC plugins from `main` and record the exact jars used for runtime tests.

See [asset verification](overview.md#verify-assets).

## Selecting versions

Select the newest accessible full distribution compatible with Paper 1.21.10 and
Java 21. Preserve licensed editions: a newer free or API-only artifact is not a
replacement for a supplied Premium runtime. If a compatible update requires
account access, keep the supplied binary until that update is available.

Pin snapshot builds by exact checksum and source URL. ProtocolLib uses the
[Spigot development build](https://github.com/dmulloy2/ProtocolLib/releases/tag/dev-build)
for 1.21.10 fixes; the mutable upstream tag is not the dependency pin. Consult the
manifest for the stored bytes and the consumer's script for its immutable commit.

Update download paths, filenames, checksums, installer coordinates and POM versions
together. Verify consumer builds before merging their new pins. Previous inputs
remain accessible at their original Git commits; rollback restores the previous
consumer pin and associated checksums and Maven coordinates together.
