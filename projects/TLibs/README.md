# TLibs

[Source repository](https://github.com/TF-Minecraft/TLibs) · [All projects](../../README.md)

TLibs consumers use `me.plugins:tlibs` with Maven `provided` scope. A shared
installer verifies the pinned binary and installs it in Maven's local cache;
consumer repositories no longer bundle TLibs or use a `tfmc.tlibs` filesystem path.

From a consumer checkout with TLibs cloned alongside as `../tlibs`:

```sh
python3 ../tlibs/tools/install-dependency.py --pom pom.xml
mvn clean verify
```

See the [installer and pinned-version guide](https://github.com/TF-Minecraft/TLibs/blob/v1.1.0/DEPENDENCIES.md)
for source access, offline installation, Java requirements, CI and rollback.
All 26 TF-Minecraft consumers now pin **TLibs 1.1.0**, built from the latest source.
Both builds and server runtime require **Java 25**. Download the versioned
[TLibs-1.1.0.jar](https://github.com/TF-Minecraft/TLibs/releases/download/v1.1.0/TLibs-1.1.0.jar).
The installer uses the public release without a private dependency token. Older
checksum-based versions remain available for rollback. No hosted Maven registry is configured yet.
TLibs remains a separate runtime plugin on the server.
