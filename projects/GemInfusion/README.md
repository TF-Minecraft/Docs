# GemInfusion

[Source repository](https://github.com/TF-Minecraft/GemInfusion) · [All projects](../../README.md)

Gem infusion, socket rarity preservation and the integrated goldsmithing project system.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Run `mvn clean verify` with JDK 21 from the source checkout. The POM
uses **release 21**, resolves **Paper API 1.21.10-R0.1-SNAPSHOT** from Maven,
and declares `api-version: 1.21.10` in the plugin manifest.

Install the TLibs version declared in `pom.xml` using the
[shared installer](../TLibs/README.md) in pinned mode; CI uses the shared setup action.
Prepare the authorized private jars in `libs/` with
`.github/scripts/prepare-release.sh` and verify `.github/dependencies.sha256`.
These supply Gson, MMOCore, MMOItems and MythicLib; TLibs and the server API
are Maven dependencies. Output is `target/geminfusion-<version>.jar`.

Gameplay validation remains separate from compilation; follow the
[shared baseline](../../PLATFORM.md) for build and validation requirements.

## Runtime and configuration

Required plugins declared by the manifest: TLibs, MMOItems, MythicLib. MMOCore
is declared optional.

`InfusionMain` loads `config.yml`, `goldsmithing.yml` and the `goldsmithing/`
definitions for hits, materials, tiers, qualities and projects. It loads
persisted stations, flushes them periodically and on shutdown, and registers
socket/unsocket listeners.

Infusion tables save their gem IDs and hit progress after each deposit or hit in
`plugins/GemInfusion/data/infusion-stations/<world-uuid>_<x>_<y>_<z>.yml`.
Completed batches also save the rolled items awaiting delivery. Startup restores
unfinished batches and resumes remaining drops without requiring the player to
be online. Tables stay occupied until delivery finishes. Autosave and shutdown
also save active tables.

A failed deposit or hit save leaves the gem or infusion token with the player and
keeps the previous progress. Unreadable snapshots, missing worlds and unknown
gem IDs are logged and retained; the affected table refuses new deposits until
staff repair the snapshot or restore the missing configuration. Stop the server
before repairing saved files; restart after restoring configuration to retry
retained snapshots. Snapshots are flushed to disk before atomic
replacement, then the directory is flushed. A directory flush failure after
replacement is logged without rolling back the committed deposit. Finished
tables retry failed snapshot deletion before accepting a new batch.

`/geminfusion reload` reloads definitions and stations.
`/geminfusion select <projectId>` selects a project on an empty table the player
is looking at within six blocks. Both commands require `geminfusion.admin`. Goldsmithing gameplay uses
the permission configured in `goldsmithing.yml`, defaulting to
`professions.goldsmith` (false by default); administrators bypass that gameplay
check.

Command completion requires `geminfusion.admin`. Console is offered `reload`;
players can also complete `select` and matching jewelry project IDs.

## Guides

- [Goldsmithing and finishing rules](goldsmithing.md)

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
