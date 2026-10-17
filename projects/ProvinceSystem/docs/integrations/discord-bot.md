# TFMC Discord bot

The bot runs as Red-DiscordBot on AMP instance `TFMCDiscordBot01`. MinecraftBan,
Precedent and PatchNotes sources are maintained under
[`ProvinceSystem/discord/`](https://github.com/TF-Minecraft/ProvinceSystem/tree/main/discord).
Other cogs, including SkinsReview and Patreon, are installed separately on AMP.
TFMCWeb is the Minecraft plugin; ProvinceSystem stores the verified account links.

## Role

[Red-DiscordBot](https://github.com/cog-creators/red-discordbot) cogs on AMP (CubeCoders):

| Cog area | Purpose |
|----------|---------|
| Skins review | Pending notify → `#bot-feed`, Approve/Deny → ProvinceSystem staff API |
| Drinks review | `drinksreview` cog - same pattern for drink submissions |
| Link | `/linkdiscord <code>` completes MC ↔ Discord bind |
| Moderation | `/minecraftwarn`, `/minecraftban` resolve selected Discord users to Minecraft accounts; `/minecraftwho` shows the link. Ban/warn DMs and **Banned** role add/clear |
| Precedent | `/case-log [user]` (staff) logs a case with the selected user's Minecraft identity; `/precedent <info>` (staff+helper) searches precedent — see [precedent.md](precedent.md) |
| Patreon | `patreon` cog - supporter link/status/unlink, role outbox, DMs, staff lookup and sync tools — see [patreon.md](patreon.md) |

The bot does **not** execute in-game bans (Essentials owns MC bans).

## ProvinceSystem API surface (staff)

Bot calls ProvinceSystem with `X-Staff-Key`. Full route list:

- Skins: [cosmetics/skins.md](../cosmetics/skins.md) (staff pending, approve/deny, notifications, file download)
- Drinks: [cosmetics/drinks.md](../cosmetics/drinks.md) (staff pending, approve/deny)
- Identity: [identity/tfmcweb.md](../identity/tfmcweb.md) (link complete, guild events)
- Precedent: [precedent.md](precedent.md) (log case, search precedent)

Player-facing mint and link **start** run in-game via TFMCWeb, not the bot.

## Linked accounts in moderation

Staff and Helpers select the Discord user in `/minecraftwarn user reason` or
`/minecraftban user reason duration`. The Minecraft name and UUID come from the
verified one-to-one account link. Discord nicknames and display names are never
used to infer a Minecraft identity. These commands send notifications; Essentials
still executes the Minecraft ban.

`/minecraftwho user` privately displays the linked Minecraft name and UUID for
Staff and Helpers. The name comes from the latest CoreProtect `co_user` row for
that UUID when available, otherwise the name stored with the link. A rename
does not change which account is selected. The lookup labels the name's source.
When no name is recorded, moderation identifies the player by UUID.

`username` is an optional fallback on warn/ban for an account confirmed to be
unlinked. Staff records label this **Unlinked (manual name)**. A supplied name
that differs from the linked name is refused. A failed account lookup stops the
command before any DM, role change or log; it does not allow a guessed name to
override a link. Link or unlink changes are read on every command, and expired
guild-leave graces count as unlinked.

For a case, run `/case-log user` and select the Discord user. The modal asks for
the incident, rule, ruling and punishment, without a player-name field. Submission
checks the member's current link and staff permission. It stores the name
in `players` and appends the Minecraft UUID and Discord ID to the ruling, leaving
the incident summary used for embeddings unchanged. The ruling input is capped
at 300 characters to leave room within the API's 500-character limit.
`/case-log` without `user` keeps manual entry for multiple or unlinked players.

Players can link through [Profile](https://tfminecraft.net/profile), or run
`/linkdiscord` in Minecraft and redeem the code with `/linkdiscord code` in Discord.
The bot's existing link/unlink commands remain in SkinsReview.

## Identity lookup API

`GET /skins/discord/identity/{discord_user_id}` requires `X-Staff-Key`; plugin keys
and public/browser requests do not grant access. The path accepts a numeric
Discord snowflake (15–20 digits).

```json
{
  "linked": true,
  "discord_user_id": "323456789012345678",
  "player_uuid": "0f6c5a52-3b7e-4c39-9d1d-2a8f0e7b9c11",
  "minecraft_name": "Steve",
  "name_source": "coreprotect"
}
```

`name_source` is `coreprotect`, `link`, or `null` if no name is known. An unknown
or expired link returns `linked: false` and null Minecraft fields. CoreProtect
unavailability falls back to the stored link without changing it. The bot's
lookup requests time out after eight seconds and return a private retry message.

## Configuration (summary)

| Env / config | Purpose |
|--------------|---------|
| `API_BASE_URL` | ProvinceSystem API (use local/staging URL for dev) |
| `STAFF_KEY` | Matches backend `STAFF_KEY` |
| `BOT_FEED_CHANNEL_ID` | `#bot-feed` for review embeds |

## Local development

Run bot against a local API with a test `STAFF_KEY`. Create pending submissions
via Profile's Skins or Drinks tab or curl. See [ops/local-dev.md](../ops/local-dev.md).

The cog tests use the installed bot's Red 3.5.24 and discord.py 2.7.1 on Python 3.11.
From a ProvinceSystem checkout:

```sh
python3.11 -m venv .venv-bot
.venv-bot/bin/python -m pip install -r discord/requirements-test.txt
.venv-bot/bin/python -m pytest -q discord/test_identity_commands.py
```

They exercise real command definitions and modals against a local HTTP server;
delivery calls are mocked, so no Discord token or guild is needed. Backend
lookup tests run with the normal Postgres test setup in
[local development](../ops/local-dev.md):

```sh
cd backend
python -m pytest -q src/skins/test_bot_identity.py
```

## Updating the maintained cogs

Deploy the merged ProvinceSystem API before updating MinecraftBan or Precedent.
Then copy the corresponding `discord/minecraftban/` and `discord/precedent/`
source files into `cogs/CogManager/cogs/<cog>/` through `amp-api` on
`TFMCDiscordBot01`. Preserve each live `config.yml`; it holds the API URL,
staff key and role/channel settings. Example configs contain no production key.

Reload the affected cog with `[p]reload minecraftban` or `[p]reload precedent`,
then run `[p]slash sync` so Discord receives the optional `username`, optional
case `user`, and new `/minecraftwho` command. Enable the cog's slash commands
with `[p]slash enable <cog>` first if they were not already enabled. A website
deployment does not update the separately running bot.

The Minecraft plugin needs no update for this workflow. To roll back, restore
the previous cog files, reload them and sync slash commands. The lookup API is
additive and can remain deployed with the older cogs.
