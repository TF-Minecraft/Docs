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

## API requirements

Inventory-scanning consumers require TLibs 2.1.0 or newer. Character-focus
consumers require RPCharacters 2.1.0 or newer. Use the dependency versions
pinned in each consumer's POM and the [shared pipeline guide](../../PIPELINES.md)
for build and release verification.

## Verification

On Paper, check food freshness and fish conversion, artifact updates, focus
spending and character switching, offline regeneration, and restart persistence.
For letters, check editing, sealing and opening in both hands, plus queued mail.
Verify that balances and item contents remain correct across these operations.
Unit tests do not replace these integration checks.
