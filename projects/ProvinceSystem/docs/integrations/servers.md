# Servers

[Project index](../../README.md) · [Source module](https://github.com/TF-Minecraft/ProvinceSystem/tree/main/backend/src/servers)

The staff panel's Servers tab compares every TFMC plugin's latest GitHub
release with the jar Main and Dev have installed and the version each server
is running. `GET /admin/servers` serves it to admins and the owner
(`view_servers`). It only reads; it does not install jars or restart servers.

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
