# BirdMessenger

[Source repository](https://github.com/TF-Minecraft/BirdMessenger) · [All projects](../../README.md)

Character-addressed letters sent through mailbox furniture, with persisted delivery and optional Discord notifications.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Run Maven with **JDK 21** from the source checkout. The POM sets `maven.compiler.release=21` and resolves `org.spigotmc:spigot-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope from Spigot snapshots. The plugin descriptor declares `api-version: 1.21.10`.

Install these matching Java 21 TFMC artifacts into local Maven before building: `me.plugins:tlibs:1.1.0`, `net.tfminecraft:rpcharacters:1.1.7`. Their source repositories use `mvn clean install`; CI uses the pinned dependency setup actions.

Populate `libs/` with the exact files and hashes listed in `.github/dependencies.sha256`. `.github/scripts/prepare-release.sh` downloads those pinned private assets when supplied with the approved dependency token.

Run `mvn clean verify` to build and run the available tests; use `mvn clean install` when another plugin needs the result as a Maven dependency. The plugin JAR is written under `target/`. Gameplay and web integration checks on the Minecraft 1.21.10 server remain separate from build verification.

## Runtime and configuration

The manifest requires TLibs and marks RPCharacters, TFMCWeb and ItemsAdder optional. The character picker needs RPCharacters; furniture mailboxes need ItemsAdder; offline Discord notifications need TFMCWeb and `discord.enabled`. `/birdmessenger reload` requires `birdmessenger.reload` (op by default). See the mailbox guide below for interaction checks.

## Guides

- [Behavior and operations](overview.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
