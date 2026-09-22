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

See the [installer and pinned-version guide](https://github.com/TF-Minecraft/TLibs/blob/5da8e77d0e0696bbff7d7064a2644072da9c6428/DEPENDENCIES.md)
for source access, offline installation, Java requirements, CI and rollback.
The 24 active TF-Minecraft consumer pipelines select the **latest published stable TLibs release**
once per build and verify its checksum. Each job uses the resolved exact version
throughout compilation and packaging; drafts, prereleases and DEV artifacts are excluded.
Local POM defaults remain **TLibs 1.1.0**.
Both builds and server runtime require **Java 25**. Download the versioned
[TLibs-1.1.0.jar](https://github.com/TF-Minecraft/TLibs/releases/download/v1.1.0/TLibs-1.1.0.jar).
The installer uses the public release without a private dependency token. Older
checksum-based versions remain available for rollback. No hosted Maven registry is configured yet.
TLibs remains a separate runtime plugin on the server.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.

See [pipeline release selection](../../PIPELINES.md#build-dependencies) for promotion and rollback.

Nutrition and PointShop are archived and keep their previous pipeline definitions;
they are excluded from the active rollout.
