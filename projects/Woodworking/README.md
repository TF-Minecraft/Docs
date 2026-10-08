# Woodworking

[Source repository](https://github.com/TF-Minecraft/Woodworking) · [All projects](../../README.md)

Technical documentation is maintained here. Run commands from the source checkout unless a guide says otherwise.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

## Build and dependencies

Run Maven with **JDK 21** from the source checkout. The POM sets `maven.compiler.release=21` and resolves `io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope from the PaperMC Maven repository. The plugin descriptor declares `api-version: 1.21.10`.

Install these matching Java 21 TFMC artifacts into local Maven before building: `me.plugins:tlibs:2.0.0`. Use the [shared installer](../TLibs/README.md) for published dependencies, or `mvn clean install` from matching source versions. CI uses the shared dependency setup actions.

Populate `libs/` with the exact files and hashes listed in `.github/dependencies.sha256`. `.github/scripts/prepare-release.sh` downloads those pinned private assets when supplied with the approved dependency token.

Run `mvn clean verify` to build and run the available tests; use `mvn clean install` when another plugin needs the result as a Maven dependency. The plugin JAR is written under `target/`. Gameplay and external-plugin integration checks on the Minecraft 1.21.10 server remain separate from build verification.

## Workbench rules

Each workbench holds a project while its materials and required actions are
completed. The bench accepts any woodworking material and any tool action, so
players need to know the design. Tool work starts once every material group has
at least the amount listed by the project. Finishing waits until every required
hit group has reached its listed count too; an attempt before then leaves the
project unchanged.

Once those minimums are met, finishing produces furniture only when the material
ids, amounts and tool actions match the recipe exactly. Any other finish ruins
the project and loses its deposited materials. Players can inspect progress
with the branding tool or cancel unfinished work for a full material refund.
Station progress persists across server restarts.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
