# XML and Maven POM conventions

All TFMC plugin repositories use this layout. The platform target remains
[Java 21 / Minecraft 1.21.10](PLATFORM.md). Each repository remains independently
buildable; no shared parent POM is required.

## Formatting

- Use UTF-8, LF line endings, four spaces per indentation level, a final newline,
  and no trailing whitespace. Each plugin repository has an XML-only
  `.editorconfig` section to retain these settings when opened independently.
- Include `<?xml version="1.0" encoding="UTF-8"?>`.
- Keep the Maven namespace and use the HTTPS Maven XSD location. Put the three
  project namespace/schema attributes on separate, aligned lines.
- Put nested elements on separate lines, including goals, includes, excludes,
  and dependency exclusions. Keep scalar values on one line.
- Separate top-level sections with one blank line. Preserve explanatory comments.

## POM structure

Use this top-level order, omitting sections the project does not need:

1. Model version and parent.
2. Coordinates: group, artifact, version, packaging.
3. Project metadata: name, description, URL, ownership and related metadata.
4. Properties.
5. Dependency management and dependencies.
6. Repositories and plugin repositories.
7. Build, reporting, and profiles.

This follows [Maven's recommended POM section order](https://maven.apache.org/developers/conventions/code.html#pom-code-convention),
with TFMC's existing four-space indentation and multiline project header.

Put `maven.compiler.release` first and `project.build.sourceEncoding` second in
properties, followed by the remaining properties alphabetically. Set them to
`21` and `UTF-8`, respectively. Use `release` as the single Java target setting;
do not also declare redundant `source` and `target` values.

Keep dependency, repository, resource, plugin, and execution lists in their
existing order. Those lists can affect resolution, resource precedence, and
build execution. Preserve versions, scopes, exclusions, filtering, relocations,
and profile activation when reformatting. Existing dependency property names
are also used by build automation and must remain stable.

Declare the compiler plugin explicitly. The common TFMC version is `3.14.1`;
CoreProtect retains `3.15.0` and SimpleFactions retains `3.13.0`. Other plugin
versions remain project-specific. Version alignment requires its own build
verification and is not a formatting operation.

Do not commit generated `dependency-reduced-pom.xml` files. Maven Shade may
generate them during packaging; `pom.xml` is the maintained build definition.

## Verification

For layout changes, compare Maven's effective POM before and after from the same
checkout, JDK, Maven installation, and active profiles:

```sh
mvn org.apache.maven.plugins:maven-help-plugin:3.5.2:effective-pom -Doutput=/tmp/effective-pom.xml
```

Allow only reviewed configuration differences; ignore XML layout and property
map order. Run `mvn clean verify` when changing compiler configuration or other
build behavior, with dependencies prepared according to the repository's CI.

ProvinceSystem, ServerAssets, and Docs currently have no tracked XML or Maven
POMs to format. Their other build systems keep their own conventions.
