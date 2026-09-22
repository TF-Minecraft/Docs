# Maintaining the documentation

Put technical manuals in `projects/<repository>/`, using the canonical PascalCase repository name (for example, `ActivityTF`, `VehicleFramework`, or `ServerAssets`). Keep source repository READMEs short and link to the matching project index here.

When changing behavior, update the relevant guide in a docs PR and link it from the implementation PR. Use relative links for other guides and GitHub source links for code. Commands and filesystem paths refer to the source checkout unless a guide says otherwise.

Keep setup instructions and configuration references current. Label plans and test reports with their status and scope so readers can distinguish proposed behavior from verified behavior.

Each project index must link to its canonical source repository and back to the root project list. Each source README must link to `https://github.com/TF-Minecraft/Docs/blob/main/projects/<repository>/README.md`; the project directory name is case-sensitive. When renaming a repository, update both ends of this link and the project list. Local-only files and separate unpublished checkouts should be described as filesystem paths, not given GitHub links to nonexistent files.

Run `python -m pip install -r requirements.txt`, `python -m unittest discover -s scripts -p 'test_*.py'`, and `python scripts/check-indexes.py` before merging. The check covers local links and section anchors in every Markdown page, including reference-style links and linked images, and verifies project navigation. Remote URLs require a separate check against the source repository and ref; private source links require repository access.

This repository is public. Keep licensed jars, model/resource-pack archives, credentials and production/player data in their authorized private stores. Preserve upstream attribution and license terms. Licenses, contribution policies, inline code comments, runtime configs and player-facing application content stay with their source repositories.

CoreProtect's MkDocs configuration is in `projects/CoreProtect`; run its documentation build from that directory.
