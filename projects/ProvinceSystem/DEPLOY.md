# Previews and deploys

ProvinceSystem changes reach the website in three steps, all driven by GitHub Actions on the TF server
(`188.40.119.246`, hostname `Ubuntu-2204-jammy-amd64-base`):

| Step | Site | Trigger |
| --- | --- | --- |
| Test | `https://<branch>.tfminecraft.net` | Push to any branch except `main` ([Preview](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/.github/workflows/preview.yml)) |
| Staging | `https://dev.tfminecraft.net` | Merge to `main`, once **Build** passes ([Deploy](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/.github/workflows/deploy.yml)) |
| Live | `https://www.tfminecraft.net` | **Actions → Deploy → Run workflow**, site `www` |

Paths below are on the TF server.

## Branch previews

Pushing a branch builds its backend and frontend images on GitHub, in parallel, and pushes them to
`ghcr.io/tf-minecraft/provincesystem-preview-{backend,frontend}:<slug>` (public packages). Pushes to `main` build
the same images without deploying them and keep a registry build cache (`:buildcache`) that every branch starts
from, so a new branch reaches its preview in about three minutes. The workflow then runs
`up <slug> <sha>` over SSH as `psdeploy`, whose key is pinned to `ps-preview-ssh`.
`/usr/local/sbin/ps-preview` (runs as `tfmc`) starts compose project `pv-<slug>` on the `ps-previews` network, with
both containers running as `tfmc` under `init`;
the `ps-preview-router` Caddy container (`127.0.0.1:8090`, behind the `*.tfminecraft.net` tunnel rule) routes
`<slug>.tfminecraft.net` to it, with `/api/` going to the preview's backend.

- **Name:** [`preview_slug.py`](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/.github/scripts/preview_slug.py)
  lowercases the branch and turns anything other than letters and digits into `-` (`codex/new-map` becomes
  `codex-new-map`). Names longer than 40 characters are cut and given a 6-character hash. Hostnames already in use
  (`www`, `dev`, `api`, `mail`, `map`, `admin`, `staff`, `play`, `mc`, `status`, `preview`, `t3`, `portainer`) fail the run.
  `dependabot/**` branches are skipped.
- **Data:** the first `up` copies the dev backend's data, input, defines and output folders, with sign-in sessions,
  OAuth states and link codes deleted. A redeploy of the same branch keeps its data.
- **Environment:** only `SKINS_DEV=1`, `SITE_PUBLIC_URL` and random `STAFF_KEY`/`PLUGIN_KEY`, plus
  `SIGN_IN_SITE=https://dev.tfminecraft.net` built into the backend image. Patreon, CoreProtect and patch notes are off.
- **Sign-in:** Discord sign-in goes through dev, which needs `PREVIEW_SIGN_IN_DOMAIN=tfminecraft.net`, and keeps the
  dev account's role ([Branch previews](docs/identity/auth-security.md#branch-previews)). A player signed in on dev
  usually skips Discord.
- **Access:** public, with `X-Robots-Tag: noindex, nofollow`.
- **Limits:** at most four previews at once (`up` exits 3); backend 2 GB / 1.5 CPU, frontend 1 GB / 1 CPU.
- **Lifetime:** each `up` sets the expiry to 90 minutes later; `ps-preview-reap.timer` runs `reap` every minute.
  Push again or re-run **Preview** on the branch to restart it. Deleting the branch (merged branches are deleted
  automatically) runs `down` at once. Closing a PR without merging leaves the preview until it expires.

Inspect or stop previews by hand:

```bash
sudo -n -u tfmc /usr/local/sbin/ps-preview list
sudo -n -u tfmc /usr/local/sbin/ps-preview logs <slug> [backend|frontend]
sudo -n -u tfmc /usr/local/sbin/ps-preview down <slug>
```

## Site deploys

The **Deploy** workflow resolves the commit, checks it is on `main`, and runs `deploy <www|dev> <sha>` over SSH as
`psdeploy` with `DEPLOY_SSH_KEY`. That key is pinned in psdeploy's `authorized_keys` to
`restrict,command="/usr/local/sbin/site-deploy-ssh"`
([`scripts/site-deploy-ssh.sh`](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/scripts/site-deploy-ssh.sh)),
which runs `/usr/local/sbin/site-deploy`, a root-owned copy of
[`scripts/site-deploy.sh`](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/scripts/site-deploy.sh), as `tfmc`,
the owner of both checkouts. Deploys to the same site run one at a time.

| | `www` | `dev` |
| --- | --- | --- |
| Checkout | `/home/tfmc/ProvinceSystem` (branch `main`) | `/home/tfmc/tfmc-staging` (detached) |
| Compose target | `ps-compose main` | `ps-compose dev` |
| Health checks | `127.0.0.1:3000/` and `127.0.0.1:8000/maps/accessible` | `127.0.0.1:13001/` and `127.0.0.1:18001/maps/accessible` |
| Backups | `/home/tfmc/provincesystem-data/deploy-backups/` | `/home/tfmc/provincesystem-dev-data/deploy-backups/` |
| Older commit than deployed | deployed (this is a rollback) | skipped as `already deployed` |

`site-deploy`:

1. Refuses commits not on `origin/main` (exit 4) and, on www, a checkout with uncommitted changes to tracked files
   (exit 1). On dev, `git checkout --detach` keeps the expected local edits and refuses if they would be overwritten.
2. Backs up `province.db` with SQLite's backup API inside the backend container as `province.db.before-deploy-<sha>-<UTC time>`, keeping the newest 10.
3. Rebuilds only what changed: `frontend/`, `shared/` or `docker-compose*` rebuild the frontend; `backend/`,
   `shared/`, `frontend/lib/skins/` or `docker-compose*` rebuild the backend (`up -d --build --no-deps`).
   Other changes only move the checkout.
4. Waits up to 3 minutes for both health checks. If they fail, it puts the previous commit back, rebuilds and checks
   again, then exits 5. It never restores the database; restore a backup by hand if a migration needs undoing.
5. After a healthy www deploy that changes `backend/src/patchnotes/`, runs `sudo tfmc-patchnotes-update <sha>` so the
   [patch note jobs](docs/ops/patch-notes-jobs.md) use the same code. A failure there is logged and does not fail the
   deploy.

Each run appends a line to `/home/tfmc/site-deploy.log`.

### Rolling back www

Run **Deploy** with site `www` and an older commit on `main`. Data written since that commit stays; restore a
`deploy-backups` copy only if the newer code changed the data.

### Deploying by hand

Use the same script rather than `ps-compose up` directly, so backups, health checks and the log stay consistent:

```bash
sudo -u tfmc site-deploy deploy www <full sha>
sudo -u tfmc site-deploy deploy dev <full sha>
```

## Host Compose overrides

Each site's `docker-compose.override.yml` (`/home/tfmc/ProvinceSystem` and `/home/tfmc/tfmc-staging`, mode 640, owned
by `tfmc`) holds the host's ports, mounts and environment. The backend runs as `tfmc`, not root, so the files it
writes stay `tfmc`'s:

```yaml
services:
  backend:
    user: "1001:1001"      # tfmc
    group_add:
      - "1000"             # amp: some plugin jars are amp's and mode 640
      - "996"              # tfmc-control: the server control socket
```

`backend/.env` reaches the container only through Compose: www's base file loads it with `env_file`, and Dev's
override does the same because its `environment: !override` replaces the base list. `.dockerignore` keeps `.env`
files out of images, so a local `docker-compose.staging.yml` run gets only the settings it lists. Files the plugins
sync to the site go to `backend/src/data/plugin-assets/`, inside the data mount. Both compose files run the backend and
frontend with `init: true`, which reaps the renderer's Chromium processes.

## Keys and secrets

| Secret | Where | Used by |
| --- | --- | --- |
| `PREVIEW_SSH_KEY` | repository secret | Preview (`psdeploy`, pinned to `ps-preview-ssh`) |
| `PREVIEW_SSH_HOST`, `PREVIEW_SSH_KNOWN_HOSTS` | repository secrets | Preview and Deploy |
| `DEPLOY_SSH_KEY` | `production` and `dev` environment secrets | Deploy (`psdeploy`, pinned to `site-deploy-ssh`) |

The `production` and `dev` environments only accept deployments from `main`, so workflows on other branches cannot
read `DEPLOY_SSH_KEY`. Each psdeploy key runs only its own forced command, so the preview key cannot deploy a site.

To rotate the deploy key, generate an ed25519 key, replace its line in `/home/psdeploy/.ssh/authorized_keys` (root-owned)
with `restrict,command="/usr/local/sbin/site-deploy-ssh" ssh-ed25519 … github-site-deploy`, and store the private half as
`DEPLOY_SSH_KEY` in both the `production` and `dev` environments.

The host scripts are root-owned copies of files in
[`scripts/`](https://github.com/TF-Minecraft/ProvinceSystem/tree/main/scripts). sudoers lets `psdeploy` run `ps-preview`
and `site-deploy` as `tfmc`, and `tfmc` run `tfmc-patchnotes-update` as root.

| Host path | Source |
| --- | --- |
| `/usr/local/sbin/site-deploy`, `site-deploy-ssh` | `site-deploy.sh`, `site-deploy-ssh.sh` |
| `/usr/local/sbin/ps-preview`, `ps-preview-ssh` | `ps-preview.sh`, `ps-preview-ssh.sh` |
| `/usr/local/sbin/ps-compose` | `ps-compose.sh` |
| `/usr/local/sbin/ps-image-prune` | `ps-image-prune.sh` |
| `/etc/systemd/system/ps-preview-reap.{service,timer}`, `ps-image-prune.{service,timer}` | same names |
| `/home/tfmc/ps-preview-router/Caddyfile` (router container `ps-preview-router`, `caddy:2`) | `ps-preview-router.Caddyfile` |

After changing one, install it once merged, for example:

```bash
sudo install -m 755 scripts/ps-preview.sh /usr/local/sbin/ps-preview
sudo install -m 644 scripts/ps-preview-reap.timer /etc/systemd/system/ && sudo systemctl daemon-reload
sudo install -m 640 -o tfmc -g tfmc scripts/ps-preview-router.Caddyfile /home/tfmc/ps-preview-router/Caddyfile && sudo docker restart ps-preview-router
```
