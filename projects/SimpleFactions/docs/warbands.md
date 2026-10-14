# Warband character authority

Warband roster and leader IDs route Minecraft accounts to live combat. The
persisted `memberCharacters` and `invitedCharacters` maps record the character
holding each membership or invitation. Leadership belongs to the character in
the leader account's member slot. A ready, current session must match that exact
reference to exercise the role, appear in online member/invite lists, or resolve
through player/leader lookups. Switching to another character on the same
account grants none of those roles.

UUID-only lookups remain structural account routing for battles. New enrollment
captures an explicitly named character; an online account must be playing it.
An offline named character must resolve through the identity registry with the
same owning account. Unknown records do not create membership. Dummy members
and pending leader placeholders do not acquire reviewed heir references.

Invitations survive persistence and target their recorded character. Menus and
delayed spawn callbacks recheck character authority; spawn callbacks also retain
the initiating session generation. Session-end cleanup uses the captured outgoing
reference after that session has become noncurrent. Rejoining restores only its
recorded character. Raid muster deduplication remains account-wide and is not
cleared by switching characters or leaving a warband.

## Legacy expansion

Warband files live under `plugins/SimpleFactions/Warbands/warband_<id>.json`.
Before typed loading, the raw loader validates JSON, duplicate keys, stored/file
IDs, UUID fields and the supported `character-identity-version`. It preserves
unknown fields and explicit nulls, including nested fields in character records,
through migration, ordinary saves and restarts.

With reviewed heirs ready, absent account slots resolve only through
`Characters.legacyHeir`. Existing references remain fixed. A missing heir becomes
an explicit null slot; malformed or conflicting case aliases grant no authority.
Neither later login nor a new last-played character assigns those slots.

Each file has an independent fixed journal:

```text
Warbands/character-identity-v1/warband_<id>.json/source.json
Warbands/character-identity-v1/warband_<id>.json/plan.json
```

`source.json` contains the exact original UTF-8 text and SHA-256. `plan.json`
records its hash, complete planned output and output hash. Both are durably
written before publishing version 1. File contents and directory entries are
synced. Interrupted publication reuses those recipients without consulting a
changed heir map. Changed source, corrupt backup/plan or unsupported metadata
holds the file for review; loading, pruning and saving cannot replace it.

The heir capability is probed before linking its new methods. Older TLibs without
that API leaves legacy slots unassigned and performs no migration write. This
does not provide character authority through an account fallback. Existing valid
character references can still be used when the basic identity API is available.

## Held records and recovery

Inspect server log errors and the raw warband file plus its journal. Explicit
null or invalid member/invite entries remain visible in those documents even
when they grant no runtime role. The faction `/f admin quarantine` commands do
not assign warband slots.

The production loader retries a file held after a failed read only at startup.
After repairing it while stopped, restart the Minecraft application to reload
the warband; a successful validated read clears the hold. There is no command
that clears or retries these file holds in a running server.

For a reviewed manual assignment, cleanly stop the Minecraft application and
back up the whole SimpleFactions data directory. Verify the original account and
the chosen character's owning account against RPCharacters' reviewed records.
For a completed version-1 file, edit only the relevant `memberCharacters` or
`invitedCharacters` entry, preserving unknown fields, to a full reference:

```json
{"ownerId":"<account UUID>","characterId":"<character UUID>"}
```

Resolve conflicting aliases together, retain an audit of the original and the
decision, and validate the JSON before restart. Preserve the immutable journal.
A prepared but unpublished or conflicting plan requires staff reconciliation of
source, backup and fixed recipients; deleting its journal to obtain new heirs
does not constitute recovery. Verify the assigned character has the role and
another character on the same account cannot use it after restart.

## Offline rollback

Stop the Minecraft application using the normal deployment procedure. Keep a
fresh backup of all SimpleFactions data and the relevant RPCharacters identity
data before replacing a JAR. An older SimpleFactions restores account-based role
checks and may discard new or unknown fields on its next save, so a JAR swap
alone is not a data-preservation rollback.

From the source checkout, preview one migrated warband:

```sh
python3 tools/warband-identity-rollback.py /path/to/plugins/SimpleFactions/Warbands/warband_example.json
```

The preview checks immutable source/plan hashes and reports original member and
invite counts, whether current state differs from the planned output, and whether
the original has already been restored. Apply requires a new recovery filename:

```sh
python3 tools/warband-identity-rollback.py /path/to/plugins/SimpleFactions/Warbands/warband_example.json --apply --backup /path/to/warband-example-before-rollback.json
```

Apply preserves and syncs exact current bytes before atomically restoring the
original bytes. It refuses an existing backup or any post-migration state change,
including membership, invitations, name and unknown metadata. Reconcile changed
files and newly created warbands manually from the current-state backup; a full
pre-cutover snapshot restore discards later gameplay writes. Never resurrect a
deleted warband just because its journal still exists. Keep journals and recovery
images. Old-version writes after rollback can conflict with the fixed migration
plan; review those writes before upgrading again.

## Verification

Use Java 21 and run `tfmc-mvn -o -B clean verify` in the SimpleFactions worktree.
The production line gate covers same-account character isolation, invitations,
recorded rejoin and outgoing cleanup, current-session deferred work, held-file
protection, raw/null preservation, interrupted publication and fixed-plan replay,
source/backup/output conflicts, and actual TLibs 2.3.0 classloading. CI installs
the old release through the pinned `.github/compatibility/tlibs-2.3.xml` fixture;
local builds need that JAR in their Maven repository too.

Run the offline restore checks with isolated synthetic documents:

```sh
python3 -m unittest discover -s tools -p 'test_warband_identity_rollback.py'
```

These are storage and identity-boundary tests. A full multi-plugin combat
playtest remains a separate runtime verification procedure. See
[character membership](characters.md) for guild identity and
[estates](estates.md) for death cleanup and succession.
