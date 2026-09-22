# TLibs

[Source repository](https://github.com/TF-Minecraft/TLibs) · [All projects](../../README.md)

TLibs consumers use `me.plugins:tlibs` with Maven `provided` scope. A shared
installer verifies the pinned binary and installs it in Maven's local cache;
consumer builds resolve the pinned version through Maven.

From a consumer checkout with TLibs cloned alongside as `../tlibs`:

```sh
python3 ../tlibs/tools/install-dependency.py --pom pom.xml
mvn clean verify
```

See the [installer and pinned-version guide](https://github.com/TF-Minecraft/TLibs/blob/61bd61b17fba45e5178612578805d7108596e8a0/DEPENDENCIES.md)
for source access, offline installation, Java requirements, CI and rollback.
The legacy public, legacy private and current TFMC builds have distinct checksum-based
versions; they are not interchangeable. No hosted Maven registry is configured yet.
TLibs remains a separate runtime plugin on the server.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
