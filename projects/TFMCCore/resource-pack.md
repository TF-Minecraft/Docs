# Three-part resource-pack delivery

[TFMCCore](README.md) · [All projects](../../README.md)

TFMC's pack spends substantial client reload time scanning ZIP entries. The opt-in
multipart path partitions the completed ItemsAdder archive by whole namespaces:
`core`, `models` (ModelEngine), and `sounds` (namespaces containing only
`sounds.json`). Resource identifiers, bytes, overlay order and protected ZIP
records remain unchanged. Overlay compaction (`resource-pack.compact-overlays`)
still runs during `/iazip`.

The implementation is in
[`net.tfminecraft.tfmccore.resourcepack`](https://github.com/TF-Minecraft/TFMCCore/tree/main/src/main/java/net/tfminecraft/tfmccore/resourcepack),
and the defaults are in
[`config.yml`](https://github.com/TF-Minecraft/TFMCCore/blob/main/src/main/resources/config.yml).

## Build and delivery

The background publisher checks the completed `generated.zip` against ItemsAdder's
cached SHA-1. It copies a snapshot, verifies the hash, writes all three parts into
a temporary directory and atomically publishes the directory. Requests use three
URLs and hashes from that single generation. An unfinished or unsupported build
uses ItemsAdder's single-pack delivery. Packs containing `filter` metadata, ZIP64,
or missing the expected namespace groups are not split.

`/tcore pack` requests the pack for yourself. Console or `tfmccore.admin` may use
`/tcore pack <player>`. `/tfmc pack` uses the same route. The request replaces
previous server-provided packs, as the single-pack route does, while leaving the
player's own packs alone. Completion requires successful callbacks for every part.
Download and reload failures fall back once to ItemsAdder; decline/discard does not
trigger another prompt. An unresponsive request falls back after 180 seconds. Quit
invalidates old callbacks, and a second request is rejected while one is still
loading. A 15-second request cooldown limits repetition. With multipart delivery
disabled, these commands send ItemsAdder's single pack.

The publisher also checks on startup, so an existing completed pack can be split
without `/iazip`. It detects later rebuilds automatically. It does not itself
rebuild ItemsAdder's content on restart. Configuration changes below require a
restart; `/tcore reload config` does not restart the HTTP listener.

After `/iazip`, ItemsAdder's automatic send is replaced with the matching three
parts once publication completes. No `/tfmc pack` or reconnect is needed.
ItemsAdder still selects the recipients, so `--apply-to self` and `--apply-to none`
retain their meaning. `/iatexture` uses the same bridge. Only the configured
ItemsAdder pack UUID in the play phase is intercepted; other packs and login
configuration-phase delivery remain untouched. The required flag and prompt are
preserved. A newer send replaces an older waiting request for the same player,
and sends wait for an existing multipart reload to finish.

If the matching generation cannot be published within 60 seconds, the retained
original request is sent instead. Download/apply failures also use that original
request without reentering the bridge. Leaving removes queued sends. This bridge
uses the server's existing ProtocolLib plugin and is enabled only with multipart
delivery; no additional server configuration is needed.

## Activation

Activate and verify on Dev before Main.

1. Install a released TFMCCore build. Preserve the current jar and configs.
2. Set ItemsAdder `resource-pack.allow_other_plugins_resourcepacks: true` and
   `resource-pack.protect-player.lock-player: false`. Keep ItemsAdder's current
   self-host enabled; it serves the fallback archive. TFMCCore rejects multipart
   activation if either setting is incompatible.

   ItemsAdder 4.0.18 applies its equipment-hiding loading effect once for each
   accepted pack, but removes it only once per player. With three packs, leftover
   entries repeatedly hide the selected hotbar/held item after loading finishes.
   Disconnecting removes only one entry, so reconnecting may not clear it.
   Disabling `lock-player` avoids that visual/movement-lock effect; the separate
   command, teleport, and movement cancellation settings remain unchanged.
   Restart the server after changing this setting to clear existing duplicate
   entries.
3. Configure TFMCCore:

   ```yaml
   resource-pack:
     compact-overlays: true
     multipart:
       enabled: true
       port: 9981
       public-url: "http://<public-host>:9981/"
   ```

   The port must be free and publicly reachable; each server instance on a host
   needs its own port. The listener serves only the published ZIP parts. No
   directory listing or arbitrary plugin file is exposed.
4. In ConditionalEvents' `events/a_commands.yml`, the automatic join event sends
   the pack to players with `tfmcresourcepack.enable`. Use
   `console_command: tcore pack %player%` for that action rather than
   `iatexture %player%`, and show “Loading Resource Pack…” rather than an
   immediate “Applied Resource Pack!” message; TFMCCore reports completion after
   all parts load. Keep the existing auto/manual preference, permissions,
   reminders and timing intact. `/tfmc pack` is a native TFMCCore command (see
   [/tfmc player commands](src/main/java/net/tfminecraft/tfmccore/tfmc/TFMC.md))
   and needs no ConditionalEvents change.
5. Restart the server and verify the published-generation log, HTTP hashes, real
   joining, reconnecting, and `/iazip` regeneration.

Parts are kept under `plugins/TFMCCore/resource-pack/parts-v1/<source-sha1>/`.
Published generations are immutable and retained so in-flight clients can finish
an older download. They occupy approximately one full pack per rebuild; remove
old generations during maintenance when no clients are downloading them. The
original ItemsAdder archive is never overwritten.

## Rollback

Restore the ConditionalEvents join action to `iatexture %player%` with its original
message, set multipart `enabled: false`, restore ItemsAdder's previous
`allow_other_plugins_resourcepacks` and `protect-player.lock-player` settings,
and restart the affected server. Clients should disconnect fully and reconnect:
`iatexture` alone adds the original ZIP alongside any multipart packs still active.
The original archive and its ItemsAdder host are still present. Restore the prior
released plugin jar if rolling back the whole feature. Do not overwrite files that
another deployment has changed since the captured baseline.

## Compatibility and validation limits

The server targets Paper 1.21.10. Multiple server packs are a native Minecraft
feature since 1.20.3; TFMC's generated archive declares format 32 or newer.
Multipart delivery does not add protocol support for additional client versions.
Resource map equivalence across format boundaries does not substitute for checking
real clients, particularly newer clients' shader and atlas handling.

The offline prototype applied in 11–12 seconds versus 21–23 seconds for the
compacted single ZIP on the tested CachyOS 1.21.10 client. This is application time,
not a promise about download or total join time. Production Java output also
passed exact resource-map comparison at 24 format boundaries.
