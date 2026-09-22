# TLibs

[Source repository](https://github.com/TF-Minecraft/TLibs) · [All projects](../../README.md)

TLibs provides shared item and block APIs, MMOItems rebuild and socket handling, armour events, and SQLite helpers used by TFMC plugins. Run build commands from the `tlibs` source checkout.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

Published Java 21 replacement: [1.1.1](https://github.com/TF-Minecraft/TLibs/releases/tag/v1.1.1), verified locally. See the [replacement release status](../../PLATFORM.md#java-21-dependency-replacements) for provenance, verification and deployment status.

## Runtime and integration

The entrypoint is `net.tfminecraft.tlibs.TLibs`. `TLibs.getItemAPI()` and `TLibs.getBlockAPI()` expose the shared APIs; `getApiInstance(APIType)` is deprecated. Item path handlers let integrations register and remove their own item prefixes.

Startup loads `config.yml`, initializes APIs, registers armour and furniture listeners, and attempts to register the MMOItems rebuild bridge. `/tlibs` is restricted by `tlibs.admin` (operator by default). The plugin descriptor declares optional integrations for MMOItems, MythicLib, ItemsAdder, MythicMobs, MMOCore and MCPets, and requests loading before RPCharacters. Optional runtime hooks still have compile-time dependency requirements in the POM.

## Build and validation

The POM targets **Java 21** (`maven.compiler.release=21`) and the Minecraft **1.21.10** API. Build with JDK 21 and the matching rebuilt TFMC dependency releases.

Use the private dependency preparation script and checksum file in the source
repository to populate `libs/`. GunsAndGadgets and Cooking resolve as provided
Maven dependencies; build/install the matching versions or use the pinned release
setup actions from CI. They also depend on TLibs, so follow the shared baseline's
bootstrap guidance when rebuilding the full stack.

For the replacement release source at `v1.1.1`, run `mvn clean verify` with
JDK 21. The output is `target/TLibs-1.1.1.jar`.
Validate item resolution, rebuild/socket persistence and dependent-plugin startup
on Paper 1.21.10 with the matching rebuilt consumers before deployment.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, dependency selection and rollback.

Consumers use `me.plugins:tlibs` with Maven `provided` scope. The
[shared installer](https://github.com/TF-Minecraft/TLibs/blob/v1.1.1/DEPENDENCIES.md)
verifies plugin release hashes and installs exact coordinates without recursively
building dependency providers. Use the installer from the published TLibs tag
`v1.1.1`. From a consumer source checkout with that TLibs checkout next to it:

```sh
python3 ../tlibs/tools/install-plugins.py --pom pom.xml --mode pinned
mvn clean verify
```

The published **1.1.1** replacement supports Java 21. Current migration POMs
pin `tlibs.version=1.1.1`; pinned mode preserves their exact selected versions.
Use `--mode latest` to select newer published releases and update the consumer
properties explicitly. Older TLibs 1.1.0 binaries require Java 25. Release
provenance records the exact source and build inputs. Preserve older release
versions for rollback. TLibs remains a separate server plugin.
