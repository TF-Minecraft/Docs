# CoreProtect

[Source repository](https://github.com/TF-Minecraft/CoreProtect) · [All projects](../../README.md)

Technical documentation is maintained here. Run commands from the source checkout unless a guide says otherwise.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## TFMC build

Use JDK 21 and `mvn clean verify` from the source checkout. The POM compiles against Paper API `1.21.10-R0.1-SNAPSHOT` with compiler release 21; the loader API is `1.21.10`. Output is `target/CoreProtect-24.0.jar` for the current source version. Dependencies resolve from the POM repositories.

The later-version adapters resolve sound variants, sulfur material and the Speleothem block type without compile-time dependencies on Minecraft 26.x APIs. The existing 1.21.10 adapter selection remains in place. Build verification does not replace server checks for logging, lookup and rollback.

## Guides

- [Project overview](overview.md)
- [docs/api/index.md](docs/api/index.md)
- [docs/api/networking.md](docs/api/networking.md)
- [docs/api/version/v10.md](docs/api/version/v10.md)
- [docs/api/version/v11.md](docs/api/version/v11.md)
- [docs/api/version/v12.md](docs/api/version/v12.md)
- [docs/api/version/v13.md](docs/api/version/v13.md)
- [docs/api/version/v7.md](docs/api/version/v7.md)
- [docs/api/version/v8.md](docs/api/version/v8.md)
- [docs/api/version/v9.md](docs/api/version/v9.md)
- [docs/auto-purge.md](docs/auto-purge.md)
- [docs/commands.md](docs/commands.md)
- [docs/config.md](docs/config.md)
- [docs/database-migration.md](docs/database-migration.md)
- [docs/index.md](docs/index.md)
- [docs/languages.md](docs/languages.md)
- [docs/permissions.md](docs/permissions.md)
- [docs/tools-integrations.md](docs/tools-integrations.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
