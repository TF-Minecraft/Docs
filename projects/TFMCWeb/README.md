# TFMCWeb

[Source repository](https://github.com/TF-Minecraft/TFMCWeb) · [All projects](../../README.md)

TFMCWeb connects the Minecraft server to ProvinceSystem for Discord identity, scoped website codes, player metadata and moderation notices. Run build commands from the `tfmcweb` source checkout.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Runtime and ownership

The entrypoint is `net.tfminecraft.tfmcweb.TFMCWeb`. TLibs is a required plugin; Essentials and LuckPerms are optional integrations, declared in `src/main/resources/plugin.yml`. RPCharacters depends on TFMCWeb; TFMCWeb resolves its Discord gate API at runtime. Without RPCharacters, the Discord Survival gate is disabled while linking and HTTP remain active.

`ProvinceSystemGateway` provides the shared web transport. The plugin loads `config.yml`, maintains a link cache, starts the notice poller, and registers `/linkdiscord`, `/unlinkdiscord`, `/web`, `/token`, `/warning` and `/patreon`. `/patreon` shows supporter status, starts Patreon authorization when unlinked, and supports `/patreon unlink`. Configure the API URL, plugin key and realm using the identity guide below; permission defaults and exact command syntax live in `plugin.yml`.

The `patreon:` config block enables supporter status and maps tier keys to LuckPerms groups:

```yaml
patreon:
  enabled: false
  apply-ranks: false
  poll-seconds: 60
  reconcile-minutes: 30
  groups:
    noble: noble
    gilded: gilded
    ascended: ascended
```

LuckPerms storage is shared, so set `apply-ranks: true` on exactly one server; leave it false elsewhere. See the [Patreon integration guide](../ProvinceSystem/docs/integrations/patreon.md) for the writer setup and operations.

## Build and dependencies

Run Maven with **JDK 21** from the source checkout. The POM sets `maven.compiler.release=21` and resolves `io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope from the PaperMC Maven repository. The plugin descriptor declares `api-version: 1.21.10`.

Install these matching Java 21 TFMC artifacts into local Maven before building: `me.plugins:tlibs:2.0.0`. Use the [shared installer](../TLibs/README.md) for published dependencies, or `mvn clean install` from matching source versions. CI uses the shared dependency setup actions.

Populate `libs/` with the exact files and hashes listed in `.github/dependencies.sha256`. `.github/scripts/prepare-release.sh` downloads those pinned private assets when supplied with the approved dependency token.

Run `mvn clean verify` to build and run the available tests; use `mvn clean install` when another plugin needs the result as a Maven dependency. The plugin JAR is written under `target/`. Gameplay and web integration checks on the Minecraft 1.21.10 server remain separate from build verification.

## Related integration guides

- [LuckPerms staff-panel bridge](luckperms-bridge.md)
- [Identity and web transport](../ProvinceSystem/docs/identity/tfmcweb.md)
- [Patreon integration and one-writer setup](../ProvinceSystem/docs/integrations/patreon.md)
- [Authentication and security](../ProvinceSystem/docs/identity/auth-security.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
