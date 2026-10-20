# TFMCCore

Shared gameplay systems and statistics integrations. Build and run with **Java 21** and **Minecraft 1.21.10**, following the [shared platform baseline](../../PLATFORM.md). The POM uses compiler release 21 and Paper API `1.21.10-R0.1-SNAPSHOT`; the plugin loader declaration is `api-version: 1.21.10`.

## Dependencies

TLibs, VehicleFramework, RPCharacters, AdvancedCrafting and SimpleFactions resolve as Maven plugin artifacts at the versions declared in `pom.xml`. The shared `setup-plugins` action installs those versions. For a local build, check out TLibs `main` alongside the source and run `python3 ../tlibs/tools/install-plugins.py --pom pom.xml --mode pinned`. The installer verifies release checksums; see [TLibs dependency setup](../TLibs/README.md). Runtime optional integrations can still be mandatory compile dependencies.

The private inputs include MMOCore, MythicLib, ItemsAdder and ProtocolLib, plus ModelEngine for tests. `.github/scripts/prepare-release.sh` downloads the pinned files listed in `.github/dependencies.sha256` from private `TF-Minecraft/ServerAssets` into the ignored `libs/` directory, then runs `install-local-dependencies.sh`, which verifies the checksums and installs each jar into the local Maven repository. It requires `GH_TOKEN` with read access; CI supplies the `DEPS_TOKEN` secret. Keep licensed jars private.

## Local build

Run from the source checkout with JDK 21:

```sh
mvn -B --no-transfer-progress clean verify
```

Output: a JAR under `target/` using the version declared in `pom.xml`. Use `mvn clean install` when another local plugin needs this build. Maven packaging does not deploy to a live server.

## CI and releases

The current build workflow runs for pushes and pull requests to `main`. It installs shared plugin dependencies, prepares the pinned private jars, sets the version to `main-SNAPSHOT` (a dated `DEV-...` version for pull requests), and runs tests and packaging. Pull request artifacts contain the jar and `.build/plugin-dependencies.json`; unit-test reports are uploaded separately when present. Jar filenames therefore follow the selected Maven version.

The separate release workflow delegates to the shared Maven release workflow. Keep the dependency properties, private download script and `.github/dependencies.sha256` aligned when changing dependencies.

## Signed-book appearance

`hide-book-glint` in `config.yml` defaults to `true`. TFMCCore hides the default
enchantment glint on signed books, including letters and book skins, by storing a
glint override on the books themselves. Books in player inventories are updated
within a second; books in containers (blocks, entities, ender chests) when the
container is opened. Lecterns and plugin menus are left alone, as are books with
their own glint override. Updated books carry the `tfmccore:hidden_glint` tag, so
setting the option to `false` brings the glint back on exactly those books, in the
same way.

Inventory packets are never rewritten: clients hash every stack they
click, and in 3.8.1 and earlier a book that looked different to the client than
on the server could leave a ghost copy on the cursor. With ProtocolLib enabled, books on
entities (dropped items, item frames, displays, held books) that have not been
updated yet are still shown without glint through entity packets only.

Change the setting and run `/tcore reload config` to apply it. Validate books in
inventories, containers, item frames and dropped items with the intended resource pack.

## Book copies

`allow-book-copies` in `config.yml` defaults to `true`. Players copy a written
book by crafting it with a Book and Quill (the vanilla recipe). On the TFMC
servers every Book and Quill is the MMOItems `BOOKS.WRITABLE_BOOK`, which has
`disable-crafting`, and books signed from it keep that tag. MMOItems therefore
cancels the craft: the copy shows in the result slot but cannot be taken.

TFMCCore wraps MMOItems' `DisableInteractions` registrations in the
`InventoryClickEvent` handler list (which `CraftItemEvent` shares). It does this
when TFMCCore enables if MMOItems is already enabled, and otherwise when MMOItems
enables. Wrappers are never wrapped again, and disabling TFMCCore puts MMOItems'
own registrations back. For a book copy craft, the wrapper undoes a cancel only when that
MMOItems handler call made it. Cancels from every other plugin, at any priority,
still apply, such as character freezes. The wrapped handler keeps its plugin,
`NORMAL` priority and place among the `NORMAL` handlers. The console
logs `Book copies: wrapped <n> MMOItems click handlers`, or a warning when
MMOItems is enabled and no handler is found.

Vanilla rules are unchanged: copies are Copy of Original or Copy of a Copy, and
Copy of a Copy and Tattered books cannot be copied. A copy keeps every component
of the original, including book skins.

Change the setting and run `/tcore reload config` to apply it.
