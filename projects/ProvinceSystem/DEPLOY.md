# Previews and deploys

ProvinceSystem changes reach the website in three steps, all driven by GitHub Actions on the TF server
(`188.40.119.246`, hostname `Ubuntu-2204-jammy-amd64-base`):

| Step | Site | Trigger |
| --- | --- | --- |
| Test | `https://<branch>.tfminecraft.net` | Push to any branch except `main` ([Preview](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/.github/workflows/preview.yml)) |
| Staging | `https://dev.tfminecraft.net` | Merge to `main`, once **Build** passes ([Deploy](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/.github/workflows/deploy.yml)) |
| Live | `https://www.tfminecraft.net` | **Actions → Deploy → Run workflow**, site `www` |

Paths below are on the TF server as `ryan` unless stated.

## Branch previews

Pushing a branch builds its backend and frontend images on GitHub, in parallel, and pushes them to
`ghcr.io/tf-minecraft/provincesystem-preview-{backend,frontend}:<slug>` (public packages). Pushes to `main` build
the same images without deploying them and keep a registry build cache (`:buildcache`) that every branch starts
from, so a new branch reaches its preview in about three minutes. The workflow then runs
`up <slug> <sha>` over SSH as `psdeploy`, whose key is pinned to the host administrator's `ps-preview-ssh`.
`/usr/local/sbin/ps-preview` (runs as `tfmc`) starts compose project `pv-<slug>` on the `ps-previews` network;
the `ps-preview-router` Caddy container (`127.0.0.1:8090`, behind the `*.tfminecraft.net` tunnel rule) routes
`<slug>.tfminecraft.net` to it, with `/api/` going to the preview's backend.

- **Name:** [`preview_slug.py`](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/.github/scripts/preview_slug.py)
  lowercases the branch and turns anything other than letters and digits into `-` (`codex/new-map` becomes
  `codex-new-map`). Names longer than 40 characters are cut and given a 6-character hash. Hostnames already in use
  (`www`, `dev`, `api`, `mail`, `map`, `admin`, `staff`, `play`, `mc`, `status`, `preview`, `t3`) fail the run.
  `dependabot/**` branches are skipped.
- **Data:** the first `up` copies the dev backend's data, input, defines and output folders, with sign-in sessions,
  OAuth states and link codes deleted. A redeploy of the same branch keeps its data.
- **Environment:** only `SKINS_DEV=1`, `SITE_PUBLIC_URL` and random `STAFF_KEY`/`PLUGIN_KEY`, plus
  `SIGN_IN_SITE=https://dev.tfminecraft.net` built into the backend image. Patreon, CoreProtect and patch notes are off.
- **Sign-in:** Discord sign-in goes through dev, which needs `PREVIEW_SIGN_IN_DOMAIN=tfminecraft.net`, and keeps the
  dev account's role ([Branch previews](docs/identity/auth-security.md#branch-previews)). A player signed in on dev
  is signed in on a preview without seeing Discord.
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
`ryan` with `DEPLOY_SSH_KEY`. That key is pinned in `~/.ssh/authorized_keys` to
`restrict,command="/home/ryan/bin/site-deploy"`, a copy of
[`scripts/site-deploy.sh`](https://github.com/TF-Minecraft/ProvinceSystem/blob/main/scripts/site-deploy.sh).
Deploys to the same site run one at a time.

| | `www` | `dev` |
| --- | --- | --- |
| Checkout | `~/work/provincesystem` (branch `main`) | `~/work/provincesystem-dev` (detached) |
| Compose target | `ps-compose main` | `ps-compose dev` |
| Health checks | `127.0.0.1:3000/` and `127.0.0.1:8000/maps/accessible` | `127.0.0.1:13001/` and `127.0.0.1:18001/maps/accessible` |
| Backups | `~/work/provincesystem-data/deploy-backups/` | `~/work/provincesystem-dev-data/deploy-backups/` |
| Older commit than deployed | deployed (this is a rollback) | skipped as `already deployed` |

`site-deploy`:

1. Refuses commits not on `origin/main` (exit 4) and, on www, a checkout with uncommitted changes to tracked files
   (exit 1). On dev, `git checkout --detach` keeps the expected local edits and refuses if they would be overwritten.
2. Backs up `province.db` with SQLite's backup API inside the backend container (the `~/work` mounts do not pass
   file locks through) as `province.db.before-deploy-<sha>-<UTC time>`, keeping the newest 10.
3. Rebuilds only what changed: `frontend/`, `shared/` or `docker-compose*` rebuild the frontend; `backend/`,
   `shared/`, `frontend/lib/skins/` or `docker-compose*` rebuild the backend (`up -d --build --no-deps`).
   Other changes only move the checkout.
4. Makes changed files and their folders world-readable (git writes new files there as 660, which the containers
   cannot read).
5. Waits up to 3 minutes for both health checks. If they fail, it puts the previous commit back, rebuilds and checks
   again, then exits 5. It never restores the database; restore a backup by hand if a migration needs undoing.

Each run appends a line to `~/site-deploy.log`.

### Rolling back www

Run **Deploy** with site `www` and an older commit on `main`. Data written since that commit stays; restore a
`deploy-backups` copy only if the newer code changed the data.

### Deploying by hand

Use the same script rather than `ps-compose up` directly, so backups, health checks and the log stay consistent:

```bash
~/bin/site-deploy deploy www <full sha>
~/bin/site-deploy deploy dev <full sha>
```

## Keys and secrets

| Secret | Where | Used by |
| --- | --- | --- |
| `PREVIEW_SSH_KEY` | repository secret | Preview (`psdeploy`, pinned to `ps-preview-ssh`) |
| `PREVIEW_SSH_HOST`, `PREVIEW_SSH_KNOWN_HOSTS` | repository secrets | Preview and Deploy |
| `DEPLOY_SSH_KEY` | `production` and `dev` environment secrets | Deploy (`ryan`, pinned to `site-deploy`) |

The `production` and `dev` environments only accept deployments from `main`, so workflows on other branches cannot
read `DEPLOY_SSH_KEY`. The `psdeploy` user, `ps-preview`, the router and the reap timer belong to the host
administrator.

If the host administrator rotates ryan's login key (`ryan-regenerate-key`), `authorized_keys` is rewritten and the
deploy key line is lost. Generate a new ed25519 key, add its public half as
`restrict,command="/home/ryan/bin/site-deploy" ssh-ed25519 … github-site-deploy`, and store the private half as
`DEPLOY_SSH_KEY` in both environments.

After changing `scripts/site-deploy.sh`, copy it to `~/bin/site-deploy` once merged. The forced command never runs
the copy in a checkout it updates.
