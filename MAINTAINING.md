# Maintaining the documentation

Put technical manuals in `projects/<repository>/`, using the canonical PascalCase repository name (for example, `ActivityTF`, `VehicleFramework`, or `ServerAssets`). Keep source repository READMEs short and link to the matching project index here.

When changing behavior, update the relevant guide in a docs PR and link it from the implementation PR. Use relative links for other guides and GitHub source links for code. Commands and filesystem paths refer to the source checkout unless a guide says otherwise.

Use [PLATFORM.md](PLATFORM.md) as the shared **Java 21 / Minecraft 1.21.10** baseline. Every project index links to it. Keep runtime versions separate from Maven API dependencies, Java compiler targets and plugin loader metadata; document source mismatches rather than changing their labels to suggest a completed migration. When source build settings change, update the matrix and record the migration/release status.

Keep setup instructions and configuration references current. Keep one-off review notes, playtest reports, raw command output and captures in PR descriptions, an ignored source-checkout `.scratch/` directory, or the external test lab. Do not commit these session artifacts to source repositories or copy them here. Promote lasting findings into the relevant architecture, troubleshooting or testing guide, with their scope and limitations. Label maintained plans and verification guides with their status so readers can distinguish proposed behavior from verified behavior.

Each project index must link to its canonical source repository and back to the root project list. Each source README must link to `https://github.com/TF-Minecraft/Docs/blob/main/projects/<repository>/README.md`; the project directory name is case-sensitive. When renaming a repository, update both ends of this link and the project list. Local-only files and separate unpublished checkouts should be described as filesystem paths, not given GitHub links to nonexistent files.

Run `python -m pip install -r requirements.txt`, `python -m unittest discover -s scripts -p 'test_*.py'`, and `python scripts/check-indexes.py` before merging. The check covers local links and section anchors in every Markdown page, including reference-style links and linked images, and verifies project navigation. Remote URLs require a separate check against the source repository and ref; private source links require repository access.

This repository is public. Keep licensed jars, model/resource-pack archives, credentials and production/player data in their authorized private stores. Preserve upstream attribution and license terms. Licenses, contribution policies, inline code comments, runtime configs and player-facing application content stay with their source repositories.

CoreProtect's MkDocs configuration is in `projects/CoreProtect`; run its documentation build from that directory.
