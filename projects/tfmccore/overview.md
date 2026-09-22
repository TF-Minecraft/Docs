# TFMC Core

Build with Java 21 and Maven. Private dependency JARs live in `libs/` and are
ignored by Git. Commit `libs/SHA256SUMS` to verify the exact builds in CI.

## CI setup

The workflow follows `JustinasLa/activity-tf`: pushes to any branch and
same-repository pull requests targeting `main`, plus manual runs, build and test the plugin and save
the JAR as a workflow artifact for 90 days. Successful pushes to `main` also
upload it to this repository's `latest` release. Manual runs only produce an
artifact. Fork and Dependabot PRs are skipped because secrets are unavailable.

Each push builds its newest commit; pushing several commits together produces
one build. Local commits trigger CI once pushed to GitHub. New pushes do not
cancel earlier builds. Dependabot pushes are also skipped because they cannot
access the dependency secret.

Upload these five files from `libs/` as **release assets on tag `v1`** in
[tfmc-deps](https://github.com/JustinasLa/tfmc-deps/releases/tag/v1), not into a
repository folder named `releases`:

```powershell
gh release upload v1 --repo JustinasLa/tfmc-deps libs/TLibs-1.0.jar libs/vehicleframework-1.1.11.jar libs/rpcharacters-1.1.6.jar libs/advancedcrafting-1.1.7.jar libs/simplefactions-2.8.7.jar
```

The other two required assets, `MMOCore-1.13.1.jar` and
`MythicLib-dist-1.7.1.jar`, were already present with matching SHA-256 digests
when checked on September 12, 2026. Paper API and Gson come from Maven;
they do not need release assets.

Create a fine-grained personal access token with the tfmc-deps owner as resource
owner, select tfmc-deps, and grant **Contents: Read-only**. The account creating
the token must have access to that repository. A TFMC Core repository
administrator must save it as the Actions repository secret `DEPS_TOKEN`
(Settings > Secrets and variables > Actions), or use the interactive command:

```powershell
gh secret set DEPS_TOKEN --repo Drefvelin/tfmccore
```

The default `GITHUB_TOKEN` cannot read another private repository. Publishing
uses TFMC Core's own `GITHUB_TOKEN` with `contents: write`; no additional token
is needed for that job.

Review and commit from PowerShell:

```powershell
git diff
git add .github/workflows/build.yml .gitignore pom.xml libs/SHA256SUMS README.md
git add src/main/java/net/tfminecraft/tfmccore/golem/GolemListener.java src/main/java/net/tfminecraft/tfmccore/stats/categories/skills/SkillsStatMain.java
git diff --cached
git commit -m "Set up TFMC Core CI builds with private dependencies"
git push origin HEAD
```

The source files above contain existing API compatibility fixes for the selected
dependencies. The separate existing `StoneListener.java` edit is excluded.
Push to `main`, or merge your branch into it, for automatic release uploads.

## Local build

With all seven JARs in `libs/`, run:

```powershell
mvn -B --no-transfer-progress '-P!deploy-live' clean package
```

Output: `target/TFMCCore.jar`. This command disables the local
`deploy-live` profile, which otherwise copies the JAR into a server folder
when that folder exists.

When changing a dependency, update the POM and workflow filenames if needed,
upload the intended server-compatible JAR, and regenerate the manifest:

```powershell
Get-ChildItem libs/*.jar | Sort-Object Name | ForEach-Object {
    '{0} *libs/{1}' -f (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant(), $_.Name
} | Set-Content libs/SHA256SUMS -Encoding ascii
```

Review and commit the manifest. Prefer distinct filenames for different builds:
replacing shared release assets can break other repositories' checksum checks.
After a TFMC Core version change, remove obsolete JARs from its `latest` release
manually; the workflow only replaces assets with matching filenames.
