# CompanionPets character ownership

[CompanionPets](../README.md) · [Saved data](saved-data.md)

Pets and Pet Houses belong to a character. The account UUID remains routing metadata for Minecraft's tame owner and account capacity limits. Switching characters ends hatch/rename/release prompts, training, greetings and fetch work; an inactive character's pet does not follow, teleport to or deliver a fetched toy to the new character. Native swimming, self-defense and safety goals remain available. When `native-combat` is enabled, the two native owner-assist goals require the recorded current owner character; another character on the same account cannot trigger that pet's assistance.

The configured total-pet and outside-pet limits are account-wide. Character rosters show only that character's pets. Hatching, management and new Pet House ownership require a ready character session. Missing identity services refuse property actions.

Carer recognition uses character IDs; changing character does not borrow another character's trust. Pet friendships use pet IDs. Inheritance retains physiology, bond, tricks, favourite toy, pet friendships and the original character identities of human memories.

## Dependencies and compatibility

The build pins TLibs **2.6.0**. RPCharacters supplies ready character sessions and reviewed legacy heirs. New API classes are capability-probed: an older or absent identity API leaves property actions unavailable; an absent estate API leaves ownership with the existing character. Upgrade provider and consumer JARs through a server restart. Plugin reload tools are not supported.

## Legacy ownership migration

After the reviewed legacy-heir directory is ready, each account-owned pet and Pet House receives that account's single reviewed heir. A dead reviewed heir remains the recipient; its estate decides any subsequent inheritance. No active-character or last-played fallback is used.

`ownership-migrations/plan-NNNN.original.yml` is an immutable, verified source copy. `plan-NNNN.yml` contains the original/planned hashes, exact planned bytes and completion marker. These precede the forced file replacement and synchronization of its directory ancestry. Restart retries the stored recipient; conflicting source edits are held for review. Later migration passes may resolve previously missing heirs.

Unknown owners remain inaccessible, retain their saved records and still count toward account limits. Unresolved human-carer pages remain under `legacy-carers` and are inert without freezing an otherwise assigned pet. Root, nested pet, relationship and Pet House metadata survive ordinary saves and restart, including unknown null-valued fields. Unsupported, quoted, null or fractional ownership schema versions, duplicate YAML keys and duplicate Pet House coordinates are refused without rewriting the source. No legacy files are automatically deleted.

## Estates

The `companionpets` estate participant describes pets and Pet Houses for wills. It uses the estate's property recipient. WAITING and FROZEN property stays with the testator. Moving ownership preserves pet/entity IDs and saved gameplay state; inherited overflow is retained.

`estates/<death>-<revision>.yml` records the exact decision, source/recipient account and character, pet/house IDs and completed receipts. Settlement requires the matching death, revision and decision immediately before publication. The participant reconciles at startup and hourly. It waits for this startup's reviewed migration and healthy persistence before creating estate intents; delayed heir readiness cannot seal an empty transfer. An unresolved legacy owner slot on the testator account blocks settlement until staff review resolves its heir; resolved pets retain their normal character authority. Completed IDs remain receipts; repeated settlement does not duplicate pets. A completed receipt that conflicts with remaining testator holdings is BLOCKED for a reviewed new revision, including old empty receipts after late heir resolution. Previously completed IDs that reappear under the testator are held for source/receipt reconciliation and are never transferred again automatically. A stale partial, malformed or conflicting intent is BLOCKED for staff review. Preserve its journal and current save before resolving it.

## Stopped-server rollback

Stop the server cleanly and preserve the complete CompanionPets directory, including deletion/estate journals and the latest progress. Install Python with PyYAML for the source repository tool:

```sh
python3 tools/ownership-rollback.py /path/to/plugins/CompanionPets plan-0001
python3 tools/ownership-rollback.py /path/to/plugins/CompanionPets plan-0001 --apply
```

The first command previews. Applying is accepted only while the current file exactly matches the migration's planned hash and the immutable archive verifies. `pets.pre-rollback.yml` preserves the current file. Any gameplay, estate or later migration changes produce a conflict; reconcile them manually rather than overwriting them. Never remove `pet-deletions.log` to resurrect deleted pets.

An older JAR alone is not a rollback: it cannot enforce character ownership and discards unknown fields during saves. Restore/convert the matching legacy data while stopped, then use the corresponding JAR. Restoring an old source copy can discard subsequent care, grants, item state and estates; the preview deliberately refuses that case.

## Verification boundaries

Unit tests exercise character isolation, captured callbacks, reviewed-heir mapping, unknown-field preservation, durable failure/replay and exact estate-intent guards. The loopback-only Paper ownership fixture exercises the actual native FOLLOW_OWNER selector across same-account character switches, water and training transitions; see [testing](testing.md).

Ownership/queue commits and player inventory are separate transactions. Existing egg consumption and physical toy/world effects do not establish arbitrary-crash exactly-once delivery. Preserve the recovery marker, saved carried-toy state and world evidence after interruption; ambiguous effects need staff reconciliation.
