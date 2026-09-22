> Canonical documentation: [TF-Minecraft/docs](https://github.com/TF-Minecraft/docs). [Source snapshot](https://github.com/TF-Minecraft/ProvinceSystem/blob/9b34fd3fd336af9025ca187ca9610690695c0efa/backend/assets/kit_skins/README.md). Commands and plain-text code/config paths refer to the source repository unless stated otherwise.

# Kit default skins

Default editable-kit PNGs live here as `{skin_png}.png` (for example `knife_skin.png`).

**Production:** RPCharacters uploads these on creation-catalog sync via
`PUT /characters/plugin/kit-skins/{name}` from `plugins/RPCharacters/assets/`.
Do not hand-copy assets onto the website host.

**Local fallbacks:** the API also checks `KIT_SKINS_DIR` and the monorepo path
`Workspace/rpcharacters/src/main/resources/assets/{skin_png}.png` when present.
