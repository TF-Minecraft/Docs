# Codex

[Source repository](https://github.com/TF-Minecraft/Codex) · [All projects](../../README.md)

TFMC's copy of [Ajneb97/Codex](https://github.com/Ajneb97/Codex): a journal of lore discoveries that each roleplay character keeps for itself.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Run Maven with **JDK 21** from the source checkout. The POM sets `maven.compiler.release=21` and resolves `io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope. The plugin descriptor declares `api-version: 1.21.10`. PlaceholderAPI, WorldGuard, WorldEdit, MythicMobs, EliteMobs and Residence come from their public Maven repositories, so Codex has no private build inputs.

Install `me.plugins:tlibs:2.6.1` with the [shared installer](../TLibs/README.md), then build:

```bash
python3 path/to/TLibs/tools/install-plugins.py --pom pom.xml --mode pinned && mvn clean verify
```

JaCoCo requires 100% line coverage of `net.tfminecraft.codex.character`, the TFMC character code. Upstream code has no tests.

## Runtime and configuration

The manifest requires TLibs and loads after RPCharacters, which provides character sessions. WorldGuard, PlaceholderAPI, MythicMobs and Residence are optional. Categories, discoveries, rewards and menus are configured as in upstream Codex; see the [upstream wiki](https://ajneb97.gitbook.io/codex).

This copy has no MySQL storage, update checker or bStats reporting. Old `mysql_database` and `update_notify` keys in `config.yml` are ignored.

## Guides

- [Behaviour and operations](overview.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
