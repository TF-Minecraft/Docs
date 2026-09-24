# Shared feature ownership

| Feature | Owner | API / administration |
| --- | --- | --- |
| Inventory scanning | TLibs | `net.tfminecraft.tlibs.itemscan.ItemScanService` and `ItemScanHandler` |
| Character focus | RPCharacters | `RPCharacters.getFocusService()`; `/focus restore <player>` and `/focus reload` |
| Letter editing, sealing and opening | BirdMessenger | `letters-config.yml`; `/birdmessenger reload` |

Cooking and Magic subscribe directly to TLibs scanning. Magic and Research read
and spend focus through RPCharacters. These consumers do not depend on TFMCCore.
Core owns server rules, custom drops, MMOItems station interactions, statistics,
whistles and item name/lore stones.

## Inventory scanning

TLibs starts and stops the scanner with its own lifecycle. Consumers with a hard
TLibs dependency subscribe during enable and unsubscribe during disable. Only
TLibs calls `start` or `stop`.

The scanner processes one online player every two ticks, scans inventory opens
immediately, and calls pickup handlers with a null inventory and slot -1. Handlers
run synchronously in registration order and own item mutation. The scanner uses
Paper's global Bukkit scheduler and does not support Folia.

## Character focus

RPCharacters owns `focus.yml` and `data/focus/<character-id>.json`. Character
activation switches balances, quitting saves them, and one timer applies configured
regeneration. Point limits, attribute bonuses and offline regeneration are
configured in `focus.yml`. Corrupt or unreadable records are reported and leave
the affected character's focus unavailable; they are not replaced with fresh points.

`RPCharacters.getFocusService()` exposes balance, maximum, spending, granting and
restoration. It returns null if focus has not started successfully. Administrators
need `rpchar.focus.admin` (operator by default) for `/focus restore <player>` and
`/focus reload`. RPCharacters' general reload also reloads focus configuration.

## Letters

BirdMessenger owns `letters-config.yml` and book edit/sign/open listeners, in
addition to delivery. The `tfmccore:sealed_letter` persistent item key remains the
stable identifier for sealed items; there is no alternative-key fallback.

The default mail acceptance includes the configured blank/sealed/opened letter
variants. An explicit `letters` list or a custom `letter` setting remains
authoritative. Check that these settings accept the items used by the server.

## Build order

1. Build and publish TLibs 2.1.0 and RPCharacters 2.1.0 from their merged source.
   Verify the release JARs, embedded versions, checksums and build metadata.
2. Build Cooking, Magic and Research against those published provider versions.
   Require their pinned-dependency CI builds to pass. Build BirdMessenger and
   TFMCCore from the merged source as well.
3. Stage all seven JARs together: TLibs, RPCharacters, Cooking, Magic, Research,
   BirdMessenger and TFMCCore. Record the source commit and checksum of each JAR;
   use the same verified set for dev and main. Publishing a release does not
   update either server.

## Manual dev and main update

The installations are controlled together. There are no automatic data imports,
version-detection paths, old API wrappers or old command aliases. Update the full
plugin set while each server is stopped. Complete and verify dev before main.

Back up the plugin jars and all affected configuration/data folders. Before first
starting the updated plugins, manually copy these files under that server's
`plugins` directory:

| Copy from | Copy to |
| --- | --- |
| `TFMCCore/focus.yml` | `RPCharacters/focus.yml` |
| `TFMCCore/data/focus/*.json` | `RPCharacters/data/focus/` (same filenames) |
| `TFMCCore/letters-config.yml` | `BirdMessenger/letters-config.yml` |

Create destination directories as needed. Compare existing destination files
before copying and resolve differences explicitly; do not overwrite newer
balances or server settings. Keep the source copies in the backup until the
update is verified. Starting without the copies creates defaults/new focus state,
so perform the file transfer first. No scanner data needs moving.

Install the updated TLibs, RPCharacters, BirdMessenger, Core, Cooking, Magic and
Research jars as one coordinated set. Update staff permissions and configured
commands to use `/focus` and `/birdmessenger reload`. Core's reload targets now
cover its own configuration, drops, stations, stats, whistle and lorestones.
Remove the replaced JARs from the plugins directory so each plugin has exactly
one installed JAR. Use a full stop/start rather than a plugin reload.

Consumer builds require TLibs 2.1.0 for scanning and RPCharacters 2.1.0 for focus;
BirdMessenger's letter feature targets 1.1.0. Publish provider releases before
building dependent consumers through the pinned-release CI. Local source-built
candidates can verify the changes together, but are not published releases.

After startup, verify food freshness/fish conversion, artifact updates, focus
spending and character switching, offline regeneration, restart persistence,
letter editing/sealing/opening in both hands, and queued mail. Compare copied balances and item
content before exercising them. Repeat the same procedure on main after dev
passes. Unit tests do not replace these Paper integration checks.

Copy main's own current files during main's maintenance window; do not copy dev's
focus balances over main. Sealed items keep their existing identifier and need
no item conversion. No scanner files need transferring.

For rollback, stop the server and restore a compatible set of jars/configuration.
If players have used the updated system, manually reconcile the current
RPCharacters focus records back into Core before restoring its ownership; the
pre-update backup no longer contains the latest balances. Retain current mail
storage and reconcile any changed letter settings as well.
