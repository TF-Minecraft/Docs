# Maintaining the unified documentation

Put technical manuals in `projects/<repository>/`. Keep source repository READMEs short and link to the matching project index here. Licenses, contribution policies, inline code comments, runtime configs and player-facing application content stay with their source repositories.

When changing behavior, update the relevant guide in a docs PR and link it from the implementation PR. Use relative links for documentation in this repository and GitHub source links for code. Commands and unlinked filesystem paths in migrated manuals retain their original source-checkout context. Imported planning notes and test reports are historical evidence, not claims that every planned feature is shipped or that old test results cover new commits.

This repository is public. Keep licensed jars, model/resource-pack archives, credentials and production/player data in their authorized private stores. A link to a private repository does not grant access. Preserve upstream attribution and license terms when editing imported manuals.

## Migration record

`migration/manifest.json` records every imported document and supporting asset, the source commit/blob/hash and the initial centralized file hash. Markdown was normalized to UTF-8, given source/context notes, and links rewritten to centralized documents or pinned source files. VehicleFramework Java/API and train-tool defaults were corrected against its POM and shipped configuration. ProvinceSystem's index now points to this shared documentation. The server-assets guides identify the subsequent removal of the ItemsAdder archive; that unrelated asset change is preserved.

`migration/historical-links.json` lists references already absent from the source snapshot. Their source context is preserved; they are not newly created local links. Documentation hashes describe the migration snapshot and should not block later documentation edits.

All 37 current source repositories are indexed, including repositories with no existing technical manual. The stale demo-repository listing disappeared from the organisation during inventory and is not part of the current repository set.

## Verification and rollback

Before removing originals, verify imported files against the manifest and publish this repository's migration PR. Source migration PRs then remove technical manuals and add a short canonical pointer. Keep documentation assets with their manuals. CoreProtect's MkDocs configuration moves with its documentation; run MkDocs from `projects/CoreProtect` if using that upstream renderer.

Rollback is per repository: revert its migration merge commit to restore the original manuals. The immutable source commits recorded in the manifest also retain every original byte. Do not delete the central repository during a partial rollout or rollback, because other repositories may already link to it. Do not rewrite source history.

## Completed rollout

All 37 source migration PRs were merged and their merge trees verified against the planned changes. See [the rollout record](migration/rollout.json) for PR links and merge commits. The verification checked that imported originals were removed, unrelated file contents and modes were unchanged, all current repositories were indexed, and source privacy was preserved.

Run `python3 tools/check_docs.py` after documentation edits to check repository-local link destinations. Use `--migration-snapshot` only when verifying the initial imported file hashes; those hashes intentionally describe the migration snapshot.
