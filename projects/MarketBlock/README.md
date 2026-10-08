# MarketBlock

[Source repository](https://github.com/TF-Minecraft/MarketBlock) · [All projects](../../README.md)

Technical documentation is maintained here. Run commands from the source checkout unless a guide says otherwise.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

See the [shared API versions](../../PLATFORM.md#shared-api-versions) for the matching provider dependency set.

## Build and dependencies

From the MarketBlock source checkout, install the shared plugin versions pinned
in `pom.xml`, then verify with Java 21:

```sh
python3 path/to/TLibs/tools/install-plugins.py --pom pom.xml --mode pinned &&
  mvn clean verify
```

Point the installer at a separate TLibs checkout. See
[build dependencies](../../PIPELINES.md#build-dependencies) for access and checksum verification.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
