# Website realm wipe

**Repos:** `rpcharacters` (owner), `ProvinceSystem` (website DB + plugin-key routes)

Player-facing strings: no em dash. Use `-` or `:`.

`/rpcharacter wipe website` deletes the website's character data for the realm this server belongs to. Use it to reset a realm, for example after pre-season testing. It does not touch the plugin's own character files.

Each realm has its own website: Dev (realm `dev`) uses the dev site, and Main (realm `main`) uses the main site. So characters made on Dev never reach the main site, and every server syncs characters with its own site.

---

## Behavior

| Piece | Choice |
|-------|--------|
| Realm | Read from the TFMCWeb gateway (`realm.id`), same as pending ingest and catalog sync. Deletes site tables for **this** `realm_id` only. Aborts if TFMCWeb cannot supply a realm id. |
| Confirm | `/rpcharacter wipe website` then `/rpcharacter wipe website confirm`. 30s TTL, same sender. No bare `/rpcharacter confirm`. |
| Auth | Command: `rpcharacters.admin`, console allowed. HTTP: `X-Plugin-Key` via `ProvinceSystemClient`. |
| Player meta | Does **not** clear `rpc_player_meta` / `character_player_meta` (ranks, 18+, slots). |
| Local data | Does **not** delete `plugins/RPCharacters/data/**`. In-game characters reappear on the site at their owner's next roster push. |

Only one server should ingest a realm; two ingesting servers would race on pending ack.

---

## Commands (player-facing)

| Input | Effect |
|-------|--------|
| `/rpcharacter wipe website` | Admin. Prints realm + that a confirm is required. |
| `/rpcharacter wipe website confirm` | Admin + pending. Calls plugin-key realm wipe. |

Usage / errors: `Usage: /rpcharacter wipe website [confirm]`. `Nothing to confirm.` `Confirm expired. Run the wipe command again.`

---

## Website wipe tables (`realm_id` = this server)

Delete:

- `character_roster`
- `character_creates`
- `character_wardrobe_slots`
- `character_create_wardrobe`
- `lore_item_customisations`

Do not delete player rank/age meta.
