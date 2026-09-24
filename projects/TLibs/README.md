# TLibs

[Source repository](https://github.com/TF-Minecraft/TLibs) · [All projects](../../README.md)

TLibs provides shared item and block APIs, MMOItems rebuild and socket handling, armour events, inventory scanning, and SQLite helpers used by TFMC plugins. Run build commands from the `tlibs` source checkout.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

See the [shared API versions](../../PLATFORM.md#shared-api-versions) for the matching provider dependency set.

## Runtime and integration

The entrypoint is `net.tfminecraft.tlibs.TLibs`. `TLibs.getItemAPI()` and `TLibs.getBlockAPI()` expose the shared APIs; `getApiInstance(APIType)` is deprecated. Item path handlers let integrations register and remove their own item prefixes.

Startup loads `config.yml`, initializes APIs, registers armour and furniture listeners, and attempts to register the MMOItems rebuild bridge. `/tlibs` is restricted by `tlibs.admin` (operator by default). The plugin descriptor declares optional integrations for MMOItems, MythicLib, ItemsAdder, MythicMobs and MMOCore, and requests loading before RPCharacters. Optional runtime hooks still have compile-time dependency requirements in the POM.

## Build and validation

The POM targets **Java 21** (`maven.compiler.release=21`) and the Minecraft **1.21.10** API. Build with JDK 21 and the matching rebuilt TFMC dependency releases.

Use the private dependency preparation script and checksum file in the source
repository to populate `libs/`. GunsAndGadgets and Cooking resolve as provided
Maven dependencies; build/install the matching versions or use the pinned release
setup actions from CI. They also depend on TLibs, so follow the shared baseline's
bootstrap guidance when rebuilding the full stack.

Run `mvn clean verify` from `main` with JDK 21. Maven writes the JAR under
`target/` using the version declared in `pom.xml`. Validate item resolution,
rebuild/socket persistence and dependent-plugin startup on Paper 1.21.10
with the matching consumers before deployment.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, dependency selection and rollback.

Consumers use `me.plugins:tlibs` with Maven `provided` scope. The
[shared installer](https://github.com/TF-Minecraft/TLibs/blob/main/DEPENDENCIES.md)
verifies plugin release hashes and installs exact coordinates without recursively
building dependency providers. Check out TLibs `main` alongside the consumer:

```sh
python3 ../tlibs/tools/install-plugins.py --pom pom.xml --mode pinned
mvn clean verify
```

Pinned mode installs the versions declared in the consumer POM. Use
`--mode latest` when intentionally upgrading those dependencies, then review
and commit the POM changes. Release provenance records the exact source and
build inputs. TLibs remains a separate server plugin.

## Shared feature ownership

See [feature ownership and migration](../TFMCCore/ownership-migration.md) for scanner, focus and letter APIs, coordinated upgrades, and rollback.
