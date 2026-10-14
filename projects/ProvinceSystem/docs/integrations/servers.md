# Servers

[Project index](../../README.md) · [Source module](https://github.com/TF-Minecraft/ProvinceSystem/tree/main/backend/src/servers)

The staff panel's Servers tab compares every TFMC plugin's latest GitHub
release with the jar Main and Dev have installed and the version each server
is running. `GET /admin/servers` serves it to admins and the owner
(`view_servers`). The comparison reads server files; the separate control
connection below installs released jars and restarts servers.

## What the tab shows

Each server has a card showing whether it is running, its Paper version and
how many plugins have each kind of problem. Below them,
**Needs a look** lists the plugins with a problem, worst first; **TFMC
plugins** lists every plugin, and **Other plugins** compares third-party jars
between Main and Dev by version. Each row shows the plugin's latest release
beside the version each server runs, dimmed when it matches that release.
Hovering a version shows the jar's file name.

Under each latest release, a mark compares it with the repository's default
branch (`main`, or `master` for CoreProtect) and links to GitHub's comparison:

| Mark | Meaning |
| --- | --- |
| `= main` | The release is the branch's latest commit. |
| `main +3` | The branch has 3 commits since the release: merged work that is not released yet. Commits that only change docs or CI count too. |
| `Off main` | The release has commits that aren't on the branch, such as a tag on a feature branch. |
| No mark | There is no GitHub token, or GitHub couldn't compare them. |

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
plugins that then report an enable failure or disable before startup finishes
are excluded from the running versions.
Paper also starts a new log at midnight, so up to twelve rotated logs are read
until one holds a startup. A jar replaced with another of the same version
since the last startup is not detected.

## Settings

| Variable | Meaning |
| --- | --- |
| `SERVER_MAIN_DIR`, `SERVER_DEV_DIR` | A folder inside the backend container holding the server's `plugins` and `logs` folders. Unset: the server's card says the site is not set up to read it. |
| `SERVERS_GITHUB_TOKEN` | A read-only GitHub token. Falls back to `PATCHNOTES_GITHUB_TOKEN`. With a token, releases are read every 10 minutes through about 11 GraphQL queries, in groups of eight repositories, each followed by a comparison of those repositories' latest releases with their default branches. Without one, GraphQL isn't available and GitHub allows 60 REST requests an hour, so releases (about 40 requests) are read hourly and not compared with the branch. |
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
check after the first reads only the logs. Only the first check after the
backend starts waits for GitHub. After that, expired releases are shown while
they are read again in the background.

## Restart and release controls

Admins and the owner (`manage_servers`) can review and start a restart,
cancel Main's five-minute countdown before installation starts, and recheck a
failed restart before reopening. Each server's card holds its buttons and shows
the restart's progress; the review opens as a dialog. Dev starts immediately
after confirmation.
Main's unchecked **Emergency: skip the countdown** option skips the countdown
for emergencies, recording the flag, actor and reason. It still requires the
backup reference, saves, release/file verification and startup checks. Instant
restarts begin installation immediately and cannot be cancelled.
The www website can control Main and Dev; the Dev
website can control Dev only. Every action requires the site's own origin,
a current signed-in session and a reason, and is recorded in the staff audit.
View-as sessions cannot issue these actions.

**Restart** activates the jars already on disk. **Update and restart**
upgrades installed TFMC plugins whose hashes identify known older published
releases. Non-increasing versions and plugins not installed on the target are
skipped; the review shows those skips.

A jar whose hash matches no published release is a test build. The review
lists each one with a checkbox to replace it with the latest release, and
warns when the test build reports a higher version than the release. They are
ticked by default on Main and unticked on Dev, where a test build is often
someone's work in progress. The start request names the chosen plugins in
`replace_test_builds`; the helper rejects names that are not test builds in
the plan, and the audit records the list. Unchosen test builds are left on
disk, are not checked as changes, and are recorded in the plan as
`test_build_kept`. Main still requires the release to have run on Dev.

The helper must be able to read every jar. A jar moved into `plugins` keeps
its own permissions, so make it `0644` first; otherwise every plan for that
server, and every Main update plan, stops with "A plugin jar can’t be read".
The release inventory is cached for ten minutes with a GitHub token, or one
hour without one. A release plan waits for an expired inventory to be read
again, and a failed read prevents the plan.

Main upgrades also require the target release's exact bytes to be on Dev,
with its version enabled without a subsequent enable failure or disable at
Dev's last completed startup. A jar changed after
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

A new completed startup must load every changed plugin and every previously
working plugin at its expected version, with the planned hashes on disk and
no new startup error messages. An unchanged plugin with an explicitly recorded
enable failure may retain that same failure at the same version. It is not
shown as a staged activation and never counts as a verified Dev release.
Existing errors are recorded in the plan and compared as distinct messages,
preserving severity and normalizing worker thread numbers in log headers.
Repeated copies of the same known error do not prevent reopening; a new
message still fails the check. Older saved plans use the same comparison.
Plans expire after ten
minutes. A changed file invalidates the plan even when its size and
modification time are unchanged.

For Main release upgrades and restarts that activate staged plugin versions,
successful startup leaves maintenance on with
**Startup passed**. Check the changed features, then use **Recheck and
reopen** with a reason. This also applies to Main's emergency override. Dev
upgrades and restarts with no Main plugin activation reopen after the
automatic checks pass. Cancellation, reopening and failure resolution also
require reasons.

## Host connection setup

The website's read-only jar/log mounts remain separate from control. Control
uses a system service running as the locked `tfmc-server-control` account.
The account has `/usr/sbin/nologin`, a locked password and no supplementary
AMP, Docker or sudo groups. The service starts at boot independently of user
login sessions; it does not need `loginctl enable-linger ryan`.

The administrator installs from the reviewed ProvinceSystem revision:

```sh
sudo bash scripts/install-server-control.sh
```

Python 3.10+, systemd, ACL tools (`getfacl`/`setfacl`), `visudo`, the existing
AMP helper and the canonical Main/Dev instance directories are required. Run
with no active restart or pending Main feature review. If either backend
already mounts the legacy `/home/ryan/.local/share/tfmc-server-control/`
socket directory, first remove that mount and recreate that backend. The
installer refuses a live legacy mount or busy job.

The installer performs the cutover and cleanup:

1. Creates or validates the locked service account and snapshots the existing
   service files, code, job state and affected ACLs under a private
   `/var/backups/tfmc-server-control/cutover-*/` directory.
2. Stops only the idle control helpers and disables the old `ryan` user unit.
   It copies plans, job journals and jar backups into
   `/var/lib/tfmc-server-control/state/` with checksum verification, refusing
   symlinks or a conflicting destination rather than overwriting evidence.
3. Installs root-owned Python modules under
   `/usr/local/lib/tfmc-server-control/backend/src/servers/`, a root-owned
   `/usr/local/sbin/tfmc-server-command` and a validated sudoers entry allowing
   only that wrapper as `amp`. The wrapper accepts the fixed Main/Dev
   console commands used by this feature; it does not accept arbitrary
   console input or AMP instance stop/restart commands.
4. Grants traversal of the two instance paths, access to plugin jars and
   top-level plugin replacement, read access to Maintenance's configuration
   and logs, and backup directory metadata. It grants no backup archive
   contents. Already readable jars do not receive a new ACL, preserving
   their timestamp evidence where possible.
5. Installs `/etc/systemd/system/tfmc-server-control.service`, starts it, checks
   both socket scopes and prepares read-only restart plans to exercise file
   and console access. It does not start a countdown, replace a jar or
   restart Minecraft. Original accepted job evidence is checked again before
   cleanup; expired plans that were never accepted may be pruned normally.
6. Removes the old helper directory and user-unit file from `ryan`, moving
   the known old `stage-<sha>` directories and source tar files into the
   private cutover backup. It preserves the `ryan` account and its separate
   SSH/deployment permissions.

On failure before cleanup, the installer attempts to restore saved service
files, code and ACLs and restart the previous helper. Inspect the printed
backup directory and journal if any rollback step needs attention. It retains
all state copies and the locked account for inspection. Do not delete the
cutover backup until the migrated controls have been checked.

The service runs with root-owned code, private state and a filesystem
namespace exposing the two plugin folders, read-only logs and read-only backup
folders. Other home-directory files, including AMP configuration outside
those mounts, are hidden from the service. `RuntimeDirectoryPreserve=yes`
keeps socket directories intact across service restarts, so existing container
bind mounts follow the replacement socket inode. See the
[systemd execution settings](https://github.com/systemd/systemd/blob/v249/man/systemd.exec.xml).

The administrator appends the following entries to the **production backend's
existing override lists**, preserving its `!override` volumes, existing
server mounts and environment values:

```yaml
services:
  backend:
    volumes:
      - /run/tfmc-server-control/www:/server-control:ro
    environment:
      - SERVER_CONTROL_SOCKET=/server-control/control.sock
```

For the Dev website, use the separate **Dev-only** directory instead:

```yaml
services:
  backend:
    volumes:
      - /run/tfmc-server-control/dev:/server-control:ro
    environment:
      - SERVER_CONTROL_SOCKET=/server-control/control.sock
```

Mount the directory, not the individual socket. Both sockets have mode
`0600`, owned by `tfmc-server-control`; the current backend runs as container
root and can connect. If backend user mapping changes, grant that mapped user
explicit access rather than opening the sockets to everyone. A read-only
mount prevents replacing the socket; it still allows connections. Never mount
these sockets into branch previews or expose them through a public proxy.

Recreate the affected website backend through the administrator's Compose
workflow. Website code deploys still use GitHub Actions as described in
[Previews and deploys](../../DEPLOY.md). While signed in as an admin or owner,
verify `GET /admin/servers/control` reports `available` and the expected
`allowed_servers`. This check does not restart Minecraft.

`SERVER_CONTROL_LOG_TIMEZONE` in the system unit must match the Dev JVM's log
clock; the current host uses `Etc/UTC`. The Dev verification check handles a
startup before midnight whose log continues into the next day. A changed jar
ACL updates its change time; if that invalidates Dev evidence, the release
becomes eligible after a subsequent verified Dev startup.

## Updating the helper

Once the administrator has installed `scripts/server-control-update.py` as
`/usr/local/sbin/tfmc-server-control-update` and allowed the deployment
account to run it with sudo, helper code changes no longer need root:

```sh
sudo /usr/local/sbin/tfmc-server-control-update <full commit on main>
```

It updates only the four modules under
`/usr/local/lib/tfmc-server-control/backend/src/servers/`, which run as the
service account. The commit must be on the ProvinceSystem `main` branch with a
successful push Build run. The updater compiles the modules as root but never
imports or runs them as root. It refuses a commit that changes the service
unit, the console wrapper or the updater itself, or whose installer differs
from the installed commit's; those need the administrator installer. It also
refuses while a restart is running; a Main feature review waiting for staff
does not block it.

The updater backs up the old modules under
`/var/backups/tfmc-server-control/update-*` (the last ten are kept), restarts
the service and checks that both sockets answer with their scopes. If they
don't, or the update is interrupted, it puts the old modules back.
`/usr/local/lib/tfmc-server-control/SOURCE.json` records the installed commit,
and `/var/log/tfmc-server-control-update.log` records each attempt. Running it
with the commit that is already installed only records that commit.

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

Control state is under `/var/lib/tfmc-server-control/state/`.
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
checks pass. A mixture never passes. A recheck after midnight reads that
startup from Paper's rotated log. If a countdown fails before maintenance
starts, players are told the restart is cancelled.

If new startup errors persist, **Recheck and reopen** continues to refuse.
The website does not offer an override for those errors. A deployment owner
with console access must investigate and verify the running plugins, changed
features and data before deciding whether to send `maintenance off` manually.
Then use **Mark failure handled** with the findings and reason. Resolving the
job alone leaves maintenance enabled and prevents a new plan until the server
is ready. Reopen requests allow up to two minutes for file checks and console
confirmation; a disconnected client should refresh job status before retrying.

**Mark failure handled** records a staff reason and releases the job lock. It
issues no console commands, restores no files and does not disable maintenance.
Use it only after manually handling the failure. A failed Dev job does not
block work on Main, but active operations remain serialized. The helper's
journal is available with:

```sh
sudo systemctl status tfmc-server-control.service
sudo journalctl -u tfmc-server-control.service
```
