# Auth and security

ProvinceSystem authentication model, production guards, and staff access controls.

Sources: [`prod_guard.py`](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/backend/src/api/prod_guard.py), [`map_access.py`](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/backend/src/api/map_access.py), [`internal_access.py`](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/backend/src/api/internal_access.py), [STAGING.md](../../STAGING.md).

## Threat model (intentional)

Public map data is low sensitivity. Still validate uploads, hash codes, and keep plugin/staff secrets server-side. Docker isolation matters more than auth theater on map read endpoints.

Cosmetics and identity are higher sensitivity: UUID-bound codes, opaque Bearer sessions, and server-side staff keys.

## Discord website sign-in

The website supports Discord OAuth sign-in for account pages and the staff panel,
separately from the UUID-bound feature codes below. Enable it with
`DISCORD_AUTH_ENABLED=1`; configure `DISCORD_CLIENT_ID`, `DISCORD_CLIENT_SECRET`,
`DISCORD_GUILD_ID` and `SITE_PUBLIC_URL`. `DISCORD_REDIRECT_URI` defaults to the
site URL plus `/api/auth/discord/callback` and must return to that site.

[`auth_routes.py`](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/backend/src/api/auth_routes.py)
starts sign-in at `/auth/discord/start`, checks the OAuth state against a browser
cookie, and sets an HttpOnly, SameSite=Lax session cookie. HTTPS uses the Secure
`__Host-tfmc_session` cookie; plain HTTP local development uses `tfmc_session`.
Cookie-authenticated writes enforce an origin check. `/account` exposes the
signed-in account and supports Minecraft linking and Patreon authorization.

Linking a Minecraft account needs TFMC server membership checked within the
last 15 minutes. Sign-in checks it. After that, the backend asks Discord with
`DISCORD_BOT_TOKEN` (`GET /guilds/{DISCORD_GUILD_ID}/members/{user}`) when an
unlinked player loads `/account` or starts a link, so a signed-in player never
has to sign in again just to link. "Unknown Member" or "Unknown User" means not
a member. One bot request runs at a time, so a request that arrives mid-check
waits for that answer. A "not a member" answer is reused for 15 seconds. An
unclear answer keeps the old check, and that session is not asked again for a
minute. A rate limit pauses every check for Discord's `retry_after`, and a
timeout or 5xx pauses them for 30 seconds. `/account` returns
`guild.can_recheck`. When it is false, Discord could not be asked, and "I've
joined, check again" falls back to a Discord sign-in.
Source: [`guild_check.py`](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/backend/src/auth/guild_check.py).

## Microsoft link

Signed-in players can link Minecraft by signing in with Microsoft instead of
pasting a `/linkdiscord` code. This needs an Azure app for personal Microsoft
accounts that Mojang has allow-listed for Minecraft services. Enable it with
`MICROSOFT_LINK_ENABLED=1`, `MICROSOFT_CLIENT_ID` and `MICROSOFT_CLIENT_SECRET`.
`MICROSOFT_REDIRECT_URI` defaults to the site URL plus
`/api/auth/microsoft/callback`; register it as a Web redirect on the Azure app.

`POST /account/minecraft/microsoft/start` needs the same fresh Discord guild
check as code linking. It stores a single-use state and PKCE verifier tied to
the site session, then returns the Microsoft sign-in URL. The callback exchanges
the code, follows Xbox Live, XSTS and Minecraft services to the Java profile, and
links that UUID through the same rules as a code. A link never replaces another
link in either direction. Microsoft, Xbox and Minecraft tokens are discarded
after the request. The callback returns to `/account?minecraft=<outcome>`.
Source: [`microsoft.py`](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/backend/src/auth/microsoft.py).

## Account page

`/account` is the hub for a signed-in player. Once Minecraft is linked it shows
the player's skin face, rank, time on the server, Profile counts and one list of
linked accounts with sign-out, unlink and Patreon controls. Before linking it
offers Microsoft sign-in with the in-game code as a fallback. The Discord,
Microsoft and Patreon buttons use each service's own artwork from
`frontend/public/brand/`, so the page loads nothing from those services.

| Route | Purpose |
|-------|---------|
| `GET /account/overview` | First and last sight on this site's server from `COREPROTECT_DB`, and the rank from the LuckPerms mirror. Each part is null when unreadable. |
| `GET /account/minecraft/head` | The linked player's face as a 64×64 PNG, from Mojang's session server and `textures.minecraft.net`. It serves only your own player, so it is no open proxy, and caches each face in memory for six hours. |
| `POST /account/profile-session` | Opens Profile for the linked player without an in-game code (below). |
| `POST /account/patreon/unlink` | Disconnects Patreon from the signed-in Discord account. |

`discord_links.link_method` records how a link was proved: `code` or
`microsoft`. Links made before it was kept have no method, and the page shows
only their date. Source: [`account_overview.py`](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/backend/src/auth/account_overview.py).

### Profile without a code

A signed-in Discord account with a linked Minecraft account gets a `profile`
Bearer session from `POST /account/profile-session`. It is the same 8-hour
session a `/token create profile` code gives, so every Profile, character and
Patreon route works unchanged. The route needs the site origin and a current
link, and shares the link-attempt rate limit. It records a spent `profile` code
with no plaintext, because sessions belong to a code. The realm comes from
`PROFILE_REALM_ID`: `main` by default, and `dev` on the Dev site.

The browser keeps that session in local storage marked as opened through
Discord, and reuses it across tabs while more than five minutes remain.
Signing out of Discord or unlinking Minecraft on `/account` revokes it. Signing
out on Profile also signs out of Discord, so Profile does not reopen on the next
visit. A visitor without a link still redeems an in-game code.

Website roles (`mod`, `admin`, `root`) control staff capabilities independently
of feature-code scopes. See [CoreProtect data](../integrations/coreprotect.md),
[rail data](../integrations/rail.md), and [LuckPerms policy](../integrations/luckperms.md)
for the individual staff panels. Configuration validation is in
[`auth/config.py`](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/backend/src/auth/config.py).

## Opaque Bearer sessions

| Surface | Mechanism |
|---------|-----------|
| Player redeem (skins / drinks / profile) | `POST …/redeem` with code → short-lived **opaque** session token stored in SQLite; client sends `Authorization: Bearer <token>` |
| Session scope | Encoded in DB row (`skin`, `skin_staff`, `drink`, `profile`) |
| TTL | Default **8h** after redeem; profile Remember me **30d** |
| Profile / map staff | `profile` scope session from `/profile` redeem or a linked Discord account ([Profile without a code](#profile-without-a-code)); carries `player_uuid` and `realm_id` for permission checks |
| No website passwords | Codes are UUID-bound and not shareable by design |

Codes are **hashed at rest** (SHA-256). Plaintext shown once in-game at mint.

### Scope enforcement

Routes validate session **scope** before acting:

- Skin upload/submit requires a valid `skin` or `skin_staff` session tied to the issuer UUID.
- Drink submit requires `drink` scope.
- Character create requires `profile` scope.
- Staff map viewer and title editor require `profile` scope plus permission flags.

Invalid or expired tokens return **401**. Wrong scope returns **403**.

## Staff map and site staff

[`map_access.py`](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/backend/src/api/map_access.py) centralizes map and staff checks.

### Staff-only maps

- Map entries in `maps.yml` declare `public: false` and optional per-map `staff_permission`.
- `ensure_map_access()` returns **403** without a valid profile Bearer session and matching permission from `rpc_player_meta` / LuckPerms sync.

### Map title editor write

- `ensure_map_staff_write()` requires `tfmc.map.staff` permission flag (constant `EDITOR_STAFF_PERMISSION`).
- Editor regen endpoints use Bearer staff session, not the plugin regen hash.

### Site staff helper

`require_site_staff(authorization)`:

1. Parses Bearer token.
2. Accepts any valid feature session (`skin`, `drink`, `profile`, …) via `get_feature_session()`.
3. Requires `has_map_staff_access(…, "tfmc.map.staff")`.
4. Returns **401** without token; **403** without permission.

Used by **`POST /skins/codes/inspect`** so only staff can decode redeem codes from the website UI.

### UI dev bypass (non-production only)

When `CHARACTER_UI_DEV=1` and token is `ui-dev-session`, staff map/editor checks bypass for local UI work. **Must be unset in production** (see production guard below).

## Plugin and staff API keys

| Key | Header | Used by |
|-----|--------|---------|
| `PLUGIN_KEY` | `X-Plugin-Key` | TFMCWeb: link start, code mint, and the gateway for ArmourShop, DrinkBuilder, RPCharacters and SimpleFactions |
| `STAFF_KEY` | `X-Staff-Key` | tfmc_bot approve/deny, notifications, staff file download |

Never expose these as `NEXT_PUBLIC_*` env vars.

## Internal plugin routes (IP, not staff tokens)

[`internal_access.py`](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/backend/src/api/internal_access.py) defines `require_localhost(request)`:

- Allows loopback (`127.0.0.1`, `::1`) and private TCP peers (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) so Paper on the Docker host can reach a published API (peer is often `172.18.0.1`).
- Rejects the request if `X-Forwarded-For` or `X-Real-IP` is set, so public nginx `/api/` cannot use the same Docker gateway IP to regen or overwrite map JSON.
- Used for hashed queue upload, plugin regen, and all `POST /{map}/data/upload/{mode}` (including title tiers). No Bearer session is required on that upload path.
- Website title editor write/regen still uses `ensure_map_staff_write()` (staff Bearer + `tfmc.map.staff`).

**Production rule:** TFMCWeb `api.base-url` on the game host must be loopback (e.g. `http://127.0.0.1:8000`), not the public website hostname. SimpleFactions regen and uploads inherit that URL through TFMCWeb's gateway. Hitting the public `/api/` hostname adds forwarded-for headers and is rejected.

## Production startup guard

[`prod_guard.py`](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/backend/src/api/prod_guard.py) runs at server startup when `PS_PRODUCTION=1`:

| Check | Failure if |
|-------|------------|
| `SKINS_DEV=1` | Dev skins helpers enabled |
| `CHARACTER_UI_DEV=1` | UI dev session bypass enabled |
| Missing `PLUGIN_KEY` | Plugin routes unauthenticated |
| Missing `STAFF_KEY` | Staff routes unauthenticated |

Startup raises `RuntimeError` and refuses to boot if any check fails.

### Frontend production build

`frontend/scripts/assert-prod-build-env.mjs` runs on `prebuild`: if `PS_PRODUCTION=1` and `NEXT_PUBLIC_CHARACTER_UI_DEV=1`, the build fails.

Pass `PS_PRODUCTION` as a Docker build arg for production frontend images.

## Staging vs production checklist

| Topic | Staging | Production |
|-------|---------|------------|
| `PS_PRODUCTION` | **Do not set** | Set `PS_PRODUCTION=1` |
| Dev flags | `SKINS_DEV=1` OK | `SKINS_DEV` and `CHARACTER_UI_DEV` must be unset |
| API keys | Compose dev defaults OK | Real `PLUGIN_KEY` / `STAFF_KEY` required |
| Internal queue/regen/plugin upload | Loopback `api.base-url` (Docker NAT private peer OK; not public hostname) | Same |
| Code inspect | Staff Bearer + `tfmc.map.staff` | Same |
| Frontend build | `NEXT_PUBLIC_CHARACTER_UI_DEV` unset for prod images | Pass `PS_PRODUCTION=1` build arg |

Full operator detail: [STAGING.md](../../STAGING.md), [ops/dev-config.md](../ops/dev-config.md).

## Free-text validation

Display names and prose fields share charset rules in `backend/src/text_validation.py` (frontend mirror: `frontend/lib/textValidation.ts`):

- Display names: Unicode letters, digits, limited punctuation; no emoji or colour codes.
- Prose: printable text; no controls or colour codes.
- Technical ids (slugs, codes): unchanged strict alphabets.

Invalid input is **rejected** at the API (400). React renders user strings as text only.

## Site dev gate (optional)

When `NEXT_PUBLIC_SITE_DEV_GATE=1`, the entire UI is replaced by a dev landing page until the visitor redeems a **profile** code and has `tfmc.map.staff`.

**Security:** Client-side gate only; API routes remain reachable if endpoints are known. Unset on public launch.

## See also

- [identity/tfmcweb.md](tfmcweb.md) - Discord link and tokens
- [cosmetics/skins.md](../cosmetics/skins.md) - skins HTTP contracts and staff routes
- [map/overview.md](../map/overview.md) - staff map gates
