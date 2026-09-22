# Maintaining the documentation

Put technical manuals in `projects/<repository>/`. Keep source repository READMEs short and link to the matching project index here.

When changing behavior, update the relevant guide in a docs PR and link it from the implementation PR. Use relative links for other guides and GitHub source links for code. Commands and filesystem paths refer to the source checkout unless a guide says otherwise.

Keep setup instructions and configuration references current. Label plans and test reports with their status and scope so readers can distinguish proposed behavior from verified behavior.

This repository is public. Keep licensed jars, model/resource-pack archives, credentials and production/player data in their authorized private stores. Preserve upstream attribution and license terms. Licenses, contribution policies, inline code comments, runtime configs and player-facing application content stay with their source repositories.

CoreProtect's MkDocs configuration is in `projects/CoreProtect`; run its documentation build from that directory.
