# CompanionPets saved data and recovery

[CompanionPets](../README.md) · [All projects](../../../README.md)

## Files

The plugin stores pets and Pet House ownership in `plugins/CompanionPets/pets.yml`.
It saves immediately after important changes, every five minutes, and when the
plugin stops. Each save writes a temporary file and replaces the main file;
`pets.yml.bak` holds the previous valid save. All files below are in
`plugins/CompanionPets/`.

| File | Purpose |
| --- | --- |
| `pets.yml` | Current pets and Pet House ownership. |
| `pets.yml.bak` | The previous valid save. Never activated automatically. |
| `pet-deletions.log` | Durable journal of terminal deletions. |
| `pets-recovery-required` | Marker present while the plugin runs; removed after a successful final save. |
| `staff-audit.yml.log` | Private log of [staff interventions](staff.md#audit). |

Back up all these files together before manually editing saved data.

## Damaged or missing saves

If the main file is damaged or missing while a backup exists, the plugin
disables itself and leaves both files untouched. To recover, stop the server,
preserve both files, and copy the backup to `pets.yml`. Reconcile ownership
changes and deleted pets before starting: the older snapshot may revert a
transfer or restore a pet that was released or died after that save.

## Deletion journal

Terminal deletions are first appended and flushed to `pet-deletions.log`, before
release or neglect removes the body. The log filters deleted IDs even if the main
save remains stale; keep it when restoring a backup. If the deletion log cannot
be written, releases are refused and body recovery and saving stop. An actual
entity death is irreversible, so it remains pending operator reconciliation.
A damaged deletion log requires manual repair before startup.

## Recovery marker

While the plugin runs, `pets-recovery-required` protects against interruption or
complete disk write failure. It is removed only after a successful final save.
If it remains after a crash or failed shutdown, the plugin refuses to start.
Stop the server, preserve all persistence files, reconcile ownership and actual
deaths in `pets.yml` (respecting `pet-deletions.log`), then remove the marker.

## Pets left outside

Pets left outside retain their last position and identity across restarts. When
their chunk's entities have loaded, the plugin reconnects to the tagged body or
recreates it at the saved position if it is missing. Missing or unloaded bodies
do not delete pet records; care pauses until the body is available. Actual
deaths still remove the pet normally. Calling an outside pet from its Pet House
also loads its saved chunk and attempts to recover its body.

Restarting or reconnecting does not teleport distant pets with a saved Follow
order to their owner. They wait at their position until the owner approaches,
asks them to follow, or calls them from the Pet House. Pets already following
during the current session keep their usual catch-up teleport when the owner
moves too far away.
