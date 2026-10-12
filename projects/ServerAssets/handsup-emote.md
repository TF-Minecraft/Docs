# Hands-up emote

The `tfmc_handsup` ItemsAdder emote raises both arms over 0.8 seconds and holds
them above the shoulders. It uses the player's skin and the standard player
skeleton. Walking is allowed. Sneaking, taking/dealing damage or leaving the
ground cancels immediately. There are no sounds or particles.

[Thievery's `/handsup`](../Thievery/docs/SYSTEM.md#hands-up-inventory-inspection)
starts this pose and enables read-only inspection. Playing the emote through
ItemsAdder alone does not enable inspection.

## Files and export

All content is in the private [ServerAssets repository](https://github.com/TF-Minecraft/ServerAssets)
under `configs/ItemsAdder/contents/tfmc_emotes/`:

- `handsup.iaentitymodel`: editable Blockbench project with the ItemsAdder entity plugin.
- `custom_emote_handsup.yml`: movement, equipment and cancellation settings.
- `resourcepack/assets/tfmc_emotes/models/entity/handsup/.player_animations`:
  baked animation, including the leading dot in the filename.
- `licenses/`: the upstream player template's Apache-2.0 license and attribution.

The timeline raises the arms from 0–0.8 seconds, holds from 0.8–1.8, and returns
to neutral from 1.8–2.6. Loop markers repeat only the held section. Cancellation
uses `skip_emote_end: true` to immediately restore the normal player pose.

Run from ServerAssets:

```sh
python3 tools/build_handsup_emote.py
python3 tools/build_handsup_emote.py --check
python3 tools/verify.py
```

The baker supports this project's linear Z rotations and unscaled skeleton.
It emits 53 frames at 20 Hz using ItemsAdder's player coordinate conventions.
Update affected `manifest.json` sizes and SHA-256 hashes after changing content.
CI checks both the manifest and the committed export.

## Installation and validation

Use ItemsAdder 4.0.18 with emotes enabled and its modern player-emote method for
Paper 1.21.10. When deployment is authorized, copy the namespace directory into
`plugins/ItemsAdder/contents/`, preserving the hidden animation file, and activate
it alongside the matching Thievery release with a server restart. No permission
grant for the ItemsAdder emote command is needed by Thievery's API integration.

The export and Java integration have offline checks. Visual rendering, model
right-click targeting and the complete plugin stack still require the
[two-player manual checks](../Thievery/docs/TEST_MATRIX.md#hands-up-inventory-inspection)
on an explicitly authorized test server.

The editable skeleton comes from [ItemsAdder's player template](https://github.com/ItemsAdder/itemsadder-entity/blob/7cabde3393be1df683b53638314113e7e7ae225f/src/assets/player_emote_blank.json).
See the upstream [animation workflow](https://wiki.itemsadder.com/adding-content/player-emotes/animations/)
and [emote properties](https://wiki.itemsadder.com/adding-content/player-emotes/advanced-properties/).
