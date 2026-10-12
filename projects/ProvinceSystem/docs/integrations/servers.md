# Servers

[Project index](../../README.md) · [Source module](https://github.com/TF-Minecraft/ProvinceSystem/tree/main/backend/src/servers)

The staff panel's Servers tab compares every TFMC plugin's latest GitHub
release with the jar Main and Dev have installed and the version each server
is running. `GET /admin/servers` serves it to admins and the owner
(`view_servers`). The comparison reads server files; the separate control
connection below installs released jars and restarts servers.

## What the tab shows

Each server has a card with its counts and Paper version. Below them,
**Needs a look** lists the plugins with a problem, worst first; **All TFMC
plugins** lists every plugin, and **Other plugins** compares third-party jars
between Main and Dev by version.

A plugin is any active repository in the organisation whose published
releases carry a jar. Drafts and pre-releases are ignored. Each server copy
gets these labels:

| Label | Meaning |
| --- | --- |
| No label | The jar is the latest release's file and the server is running it. |
| Not a release (Main) | The jar's SHA-256 matches no published release, whatever its name. |
| Test build (Dev) | The same on Dev, where test builds are allowed. |
| Older release | The jar is an earlier release's file. |
| Needs restart | The server enabled a different version at its last startup, or a jar waits in `plugins/update/`. The cell shows the running version, then the version on disk. |
| Didn't start | The last startup finished without enabling the plugin. |
| Two jars | Two jars of the plugin sit in `plugins/`. |
| Not installed | No jar. Not counted as a problem. |

Jars are matched to plugins by SHA-256 first, using the digests GitHub reports
for release assets, then by the release file's name before its version (for
example `tfmccore-`). The running version comes from the
`Enabling <name> v<version>` lines of the most recent startup in `logs/`;
Paper also starts a new log at midnight, so up to twelve rotated logs are read
until one holds a startup. A jar replaced with another of the same version
since the last startup is not detected.

## Settings

| Variable | Meaning |
| --- | --- |
| `SERVER_MAIN_DIR`, `SERVER_DEV_DIR` | A folder inside the backend container holding the server's `plugins` and `logs` folders. Unset: the server's card says the site is not set up to read it. |
| `SERVERS_GITHUB_TOKEN` | A read-only GitHub token. Falls back to `PATCHNOTES_GITHUB_TOKEN`. Each check makes about 40 requests: with a token, releases are fetched every 10 minutes; without one, GitHub allows 60 requests an hour, so they are fetched hourly. |
| `SERVERS_GITHUB_ORG` | The organisation to read. Defaults to `TF-Minecraft`. |

Mount the folders read-only in the host's `docker-compose.override.yml`:

```yaml
services:
  backend:
    volumes:
      - /home/amp/.ampdata/instances/TFMCMain01/Minecraft/plugins:/servers/main/plugins:ro
      - /home/amp/.ampdata/instances/TFMCMain01/Minecraft/logs:/servers/main/logs:ro
      - /home/amp/.ampdata/instances/TFMCDev01/Minecraft/plugins:/servers/dev/plugins:ro
      - /home/amp/.ampdata/instances/TFMCDev01/Minecraft/logs:/servers/dev/logs:ro
    environment:
      - SERVER_MAIN_DIR=/servers/main
      - SERVER_DEV_DIR=/servers/dev
```

Jar hashes are cached until a file's size or modification time changes, so a
check after the first reads only the logs.

## Restart and release controls

Admins and the owner (`manage_servers`) can review and start a restart,
cancel Main's five-minute countdown before installation starts, and recheck a
failed restart before reopening. Dev starts immediately after confirmation.
Main's unchecked **OVERRIDE: restart immediately** option skips the countdown
for emergencies, recording the flag, actor and reason. It still requires the
backup reference, saves, release/file verification and startup checks. Instant
restarts begin installation immediately and cannot be cancelled.
The www website can control Main and Dev; the Dev
website can control Dev only. Every action requires the site's own origin,
a current signed-in session and a reason, and is recorded in the staff audit.
View-as sessions cannot issue these actions.

**Restart** activates the jars already on disk. **Use latest releases and
restart** upgrades installed TFMC plugins whose hashes identify known older
published releases. Test builds, unknown files, non-increasing versions and
plugins not installed on the target are skipped; the review shows those skips.
The release inventory is cached for ten minutes with a GitHub token, or one
hour without one. A failed refresh prevents a release plan.

Main upgrades also require the target release's exact bytes to be on Dev,
with its version enabled at Dev's last completed startup. A jar changed after
that startup is not proof and is skipped. This check proves that the release
was loaded; staff must still verify its changed features and dependencies.
Related migrations must be deployed as a reviewed set with a recovery plan.
Use the manual deployment procedure when the proposed set needs offline work.
The bulk button does not publish releases or replace unreleased fixes.

Before a Main countdown, staff must record the name or location of the
consistent data and migration backups they prepared. The review shows the
latest AMP ZIP backup time when available. That timestamp and the staff's
reference are not automatic proof that all affected data is backed up. The
helper backs up displaced jars, not worlds or databases.

After Main's countdown, or immediately for Dev and Main's emergency override,
the helper enables maintenance and confirms it, sends `save-all
flush` and waits for its save confirmation. It rechecks the files against the
reviewed plan, backs up changed jars outside plugin loading paths, installs
verified files with new inodes, then sends console `stop`. AMP relaunches
Paper. The helper never uses AMP instance `stop` or `restart`, kills Java,
or runs reload commands.

A new completed startup must load every recorded plugin at its expected
version, with the planned hashes on disk and no additional startup errors.
Existing errors are recorded in the plan and compared with severity/message
counts; they do not prevent an unchanged restart. Plans expire after ten
minutes. A changed file invalidates the plan even when its size and
modification time are unchanged.

For Main release upgrades, successful startup leaves maintenance on with
**Startup passed**. Check the changed features, then use **Recheck and
reopen** with a reason. Dev upgrades and ordinary restarts reopen after the
automatic checks pass. Cancellation, reopening and failure resolution also
require reasons.

## Host connection setup

The website's existing read-only jar/log mounts remain in place. Control uses
a separate Unix socket served by a helper running as `ryan` on the Minecraft
host. One helper owns both sockets and persists countdowns independently of
website containers, with one active operation at a time. It accepts only
`status`, `plan`, `start`, `cancel`, `reopen` and `resolve`; clients cannot
supply console commands, host paths or download URLs.

Install from the reviewed ProvinceSystem revision on the host as `ryan`:

```sh
bash scripts/install-server-control.sh
```

The installer copies only the four server-control Python modules to
`/home/ryan/.local/share/tfmc-server-control/code/backend/src/servers/`, installs
`scripts/tfmc-server-control.service` as the user unit
`tfmc-server-control.service`, and enables/starts it. Python 3.10 or later
and the existing `sudo -n -u amp /usr/local/sbin/amp-ctl` permission are required.
It refuses to replace a running helper. During an update, first check for
active jobs; stop only this helper when idle, then run the installer again.

The administrator must enable the user service after logout and reboot:

```sh
sudo loginctl enable-linger ryan
```

The administrator then adds the following mount and environment entry to the
**production backend's existing override lists**, preserving the existing
`!override` mounts, plugin/log folders and environment settings:

```yaml
services:
  backend:
    volumes:
      - /home/ryan/.local/share/tfmc-server-control/www:/server-control:ro
    environment:
      - SERVER_CONTROL_SOCKET=/server-control/control.sock
```

If enabling the Dev website, its override uses the **Dev-only** socket:

```yaml
services:
  backend:
    volumes:
      - /home/ryan/.local/share/tfmc-server-control/dev:/server-control:ro
    environment:
      - SERVER_CONTROL_SOCKET=/server-control/control.sock
```

Mount the directory, not the socket file, so helper restarts expose the new
socket inode. The sockets have mode `0600`, owned by `ryan`; the current
backend runs as container root and can connect. If backend user mapping
changes, explicitly grant that mapped user access rather than opening the
socket to everyone. A read-only mount prevents replacing the socket; it does
not prevent connecting to it. Do not mount either socket into branch previews
or other containers, and do not expose it through a public proxy.

Recreate the affected website backend through the administrator's Compose
workflow. Website code deploys still use GitHub Actions as described in
[Previews and deploys](../../DEPLOY.md). Verify `GET /admin/servers/control`
reports `available` while signed in as an admin or owner. It lists
`allowed_servers` and the latest jobs. This check does not restart Minecraft.

## Scheduled restarts and recovery

The host and the currently configured AMP schedules use UTC. The helper
rejects a start when its restart/check window overlaps these windows. Normal
Main restarts reserve twenty minutes including the countdown; Dev and Main's
emergency override reserve fifteen minutes:

- Main: 05:25–06:20 daily, covering the warnings, 06:00 application Stop,
  06:02 backup and 06:10 Start.
- Dev: fifteen minutes before/after 00:00, 06:00, 12:00 and 18:00.

These guards must be updated in `scheduled_restart` if AMP schedules change.
Recheck other backup jobs and offline work before confirming a restart.

Control state is under `/home/ryan/.local/share/tfmc-server-control/state/`.
Each plan has its immutable inventory, staged jars, `job.json` events and a
`backup/` folder holding displaced jars. `jobs.json` records the latest job
per server. Accepted plan IDs are never reused for another countdown, even
when a later job has completed. Expired unaccepted plans are removed when a
new plan is prepared; accepted job evidence/backups remain until an operator
archives them.

If a swap fails, the helper restores all displaced jars from its backups
using fresh inodes and leaves maintenance enabled. If the helper crashes or
the host reboots, active jobs are marked failed and never replayed. A
countdown interrupted by a helper restart announces cancellation when the
console is reachable. A crash during installation may require manual recovery.

Keep maintenance enabled while diagnosing. For a partial installation or a
data migration rollback, use Minecraft application Stop in AMP, confirm saves
and Java exit, restore the recorded old jars and consistent data backups as
needed, and use application Start. Do not stop/restart the AMP instance.
**Recheck and reopen** accepts either the complete planned set or the complete
recorded original set, provided the current server loaded it and startup
checks pass. A mixture never passes.

**Mark failure handled** records a staff reason and releases the job lock. It
issues no console commands, restores no files and does not disable maintenance.
Use it only after manually handling the failure. A failed Dev job does not
block work on Main, but active operations remain serialized. The helper's
journal is available with:

```sh
systemctl --user status tfmc-server-control.service
journalctl --user -u tfmc-server-control.service
```
