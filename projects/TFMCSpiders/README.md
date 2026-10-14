# TFMCSpiders

[Source repository](https://github.com/TF-Minecraft/TFMCSpiders) · [All projects](../../README.md)

Technical documentation is maintained here. Run commands from the source checkout unless a guide says otherwise.

TFMC runs Minecraft **1.21.10**. See the [shared platform and build baseline](../../PLATFORM.md) for runtime, build and validation conventions.

TFMCSpiders is a fork of [TheCymaera/minecraft-spider](https://github.com/TheCymaera/minecraft-spider). Until it is transferred to TF-Minecraft, the source is at [JustinasLa/TFMCSpiders](https://github.com/JustinasLa/TFMCSpiders).

- [Behaviour, commands and tools](docs/SYSTEM.md)

## Build and dependencies

Run Maven with **JDK 21** from the source checkout. TFMCSpiders is written in Kotlin: sources are in `src/main/kotlin/net/tfminecraft/tfmcspiders/` and tests in `src/test/kotlin/`. The POM sets `maven.compiler.release=21` and `kotlin.compiler.jvmTarget=21`, compiles with `kotlin-maven-plugin`, and resolves `io.papermc.paper:paper-api:1.21.10-R0.1-SNAPSHOT` with `provided` scope from the PaperMC Maven repository. The Kotlin standard library is shaded into the plugin JAR without relocation. The plugin descriptor declares `api-version: 1.21.10`.

No private `libs/` JARs or shared TFMC plugins are required by this POM.

Run `mvn clean verify` to build and run the tests. The runtime JAR is `target/tfmcspiders-<version>.jar`; `original-*.jar` is the unshaded build and is not deployable. Gameplay checks on the Minecraft 1.21.10 server remain separate from build verification.

## Tests

Kotlin tests on JUnit 5 and Mockito cover staff access, the staff tools, the Cinderweaver model, climbing, pouncing, hits, mounting, the shroud and mimics by running the spider simulation against mocked worlds. They do not start a Paper server or check rendering on a client.

## Builds and releases

See the [shared pipeline guide](../../PIPELINES.md) for development artifacts, release tags, and dependency access.
