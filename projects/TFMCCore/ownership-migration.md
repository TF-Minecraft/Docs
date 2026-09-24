# Shared feature ownership and upgrades

TFMCCore retains server rules, drops, MMOItems station interactions, statistics,
whistles and item name/lore stones. Shared scanning, character focus and letters
have these owners:

| Feature | Runtime owner | Consumers / compatibility |
| --- | --- | --- |
| Inventory scanning | TLibs | Cooking and Magic subscribe through `net.tfminecraft.tlibs.itemscan`. Core's deprecated scanner API forwards to the same scanner. |
| Character focus | RPCharacters | Magic and Research use `RPCharacters.getFocusService()`. Core retains read/spend compatibility and `/tcore focus restore`. |
| Letter editing, sealing and opening | BirdMessenger | BirdMessenger also handles delivery. `/tcore reload letters` delegates to BirdMessenger. |

No gameplay consumer needs TFMCCore for these three features after upgrading.
Core still needs TLibs and optionally integrates with RPCharacters and
BirdMessenger. Removing Core also removes its remaining gameplay features and
admin command aliases.

## Build and release dependencies

The new scanner consumers pin `me.plugins:tlibs:2.1.0`; the new focus consumers
pin `net.tfminecraft:rpcharacters:2.1.0`. Those are the first intended provider
release versions for these APIs. BirdMessenger's letter transfer targets 1.1.0.
A POM version is a requirement, not evidence that a release has been published.

Build and release TLibs before its updated consumers. Build and release
RPCharacters before the updated Core, Magic and Research. Build BirdMessenger
before deploying Core's letter handoff. The release installer deliberately fails
if a pinned provider release is unavailable; do not substitute old jars under
new version coordinates. Dependent PRs remain drafts until provider releases
exist and their normal CI passes.

For local coordinated validation, build the provider source and install its
candidate jar under the required new coordinate in a development Maven cache.
Record the source commit with the test results. A local candidate is not a
published release or suitable evidence of release provenance.

## Runtime upgrade

Use a stopped server for the ownership handoff; do not hot-reload these plugins.
Back up the plugin jars and the full TFMCCore, RPCharacters and BirdMessenger
configuration/data directories first.

1. Install the scanner provider and updated Cooking/Magic consumers. Core's
   compatibility API forwards older consumers to TLibs after Core is upgraded.
   Before that, old consumers use the old scanner and new consumers use TLibs;
   a consumer must subscribe through only one API.
2. Install the updated RPCharacters and Core together with the focus consumers.
   RPCharacters copies missing legacy `TFMCCore/focus.yml` and
   `TFMCCore/data/focus/*.json` into its own folder before creating defaults.
   Existing destination files take precedence. Character IDs, points and
   regeneration timestamps are preserved, and source files remain untouched.
3. Install the updated BirdMessenger with Core's letter handoff.
   BirdMessenger copies a missing `letters-config.yml` from Core before creating
   defaults. It continues recognizing the `tfmccore:sealed_letter` persistent
   marker on existing items, including items stored in pending mail.

Updated RPCharacters and BirdMessenger inspect the installed Core's bundled
`plugin.yml` ownership declarations before enabling the transferred features.
If a legacy Core is installed, they leave that feature with Core and log why.
They can provide these features without Core installed. This avoids two focus
writers or duplicate letter listeners when providers are upgraded first; it
does not make every new-consumer/old-provider combination supported.

Core's `focus: RPCharacters` and `letters: BirdMessenger` ownership declarations
are part of the handoff protocol. Preserve them in custom builds. Configure focus
and letters in their new owners after migration; editing Core's old files will
no longer change those features. `/tcore reload focus` and
`/tcore reload letters` target the new owners.

BirdMessenger preserves an explicit `letters` list or a custom legacy `letter`
setting. Its default acceptance also includes the transferred feature's configured
letter variants. Review explicit lists when migrating from the Core MMOItems
`m.books.*` defaults to a BirdMessenger installation using ItemsAdder letters.

## Verification

On Paper 1.21.10 with the matching plugin set, verify:

- Cooking freshness and legacy fish conversion, Magic artifact updates, inventory
  opens and pickups; no duplicate subscriptions or scanner tasks.
- Focus balance, spending, restoration, character switching, quitting/rejoining,
  offline regeneration and restart persistence. Compare migrated JSON with the
  source before gameplay changes it.
- Existing sealed letters open once with pages/title/author rules preserved;
  newly edited, sealed and opened letters can be mailed according to the configured
  acceptance list. Pending mail remains readable.
- A provider-only upgrade with legacy Core leaves ownership with Core and logs
  the handoff requirement. Malformed migration input is reported rather than
  silently replaced with fresh state.

Unit tests and local compilation do not replace these server integration checks.

## Rollback

Stop the server before rolling back. Restore a mutually compatible set of plugin
jars; do not leave new consumers requiring APIs absent from old providers.

Legacy files retained during migration are snapshots, not continuously updated
backups. If gameplay has continued under RPCharacters, preserve its current focus
files and copy the current `data/focus` records and `focus.yml` back to Core before
restoring the old focus owner. Back up both copies and reconcile conflicts rather
than overwriting newer balances blindly. Keep the new-owner directory for a
subsequent retry; reconcile it with Core again before another forward migration,
because existing destination records take precedence.

Carry current BirdMessenger letter configuration back to Core if it changed.
Letters keep the original sealed marker, so no item rewrite is required. Keep
BirdMessenger mail data when restoring its previous jar. Do not delete the new
owner's files until rollback and a subsequent forward migration have been verified.
