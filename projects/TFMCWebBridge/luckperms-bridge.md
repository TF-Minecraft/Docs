# LuckPerms staff-panel bridge

[Project index](README.md)

The bridge is off by default and needs LuckPerms on the server:

```yaml
luckperms-bridge:
  publish: false        # send LuckPerms snapshots to this server's site
  apply: false          # also apply staff-queued changes (implies publish)
  poll-seconds: 3       # how often to fetch queued changes when applying
  snapshot-seconds: 30  # how often to publish a snapshot
```

LuckPerms storage is shared between servers, so set `apply: true` on exactly one
of them. A server that only publishes makes its site's panel read-only. Changes
are checked against live LuckPerms data, saved together or not at all, logged in
`/lp log`, and followed by a fresh snapshot. A change made by a website admin
(rather than root) is refused if the player already holds a staff group, or if
the group it adds, or any group that group inherits, is outside the admin groups. `/web status` shows the bridge state
and the age of the last snapshot.


While the bridge runs it also publishes the server's command list for the staff
panel's Commands tab: every registered command with its plugin, aliases and
permission, and whether each LuckPerms group's permissions allow it on this server
(Bukkit's defaults count where LuckPerms has no node). It reads the list a minute
after starting, checks each minute, and uploads when it changes or every ten
minutes.

Set `LUCKPERMS_READ_ONLY=1` on a website that must never queue writes. The backend also refuses new changes without a recent applying bridge poll.

See the [website protocol and permission policy](../TFMCWeb/docs/integrations/luckperms.md), [plugin configuration](https://github.com/TF-Minecraft/TFMCWebBridge/blob/main/src/main/resources/config.yml), and [bridge implementation](https://github.com/TF-Minecraft/TFMCWebBridge/tree/main/src/main/java/net/tfminecraft/tfmcweb/luckperms).
