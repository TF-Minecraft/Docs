> Canonical documentation: [TF-Minecraft/docs](https://github.com/TF-Minecraft/docs). [Source snapshot](https://github.com/TF-Minecraft/drinkbuilder/blob/e3d0394feba5f0067194eab2ccaca74d73cfbf16/src/main/resources/assets/README.txt). Commands and plain-text code/config paths refer to the source repository unless stated otherwise.

Place vanilla-style potion textures here (copied to plugin data/assets on first enable):

  potion_overlay.png  — liquid layer (tinted by drink color / CustomPotionColor)
  glass_bottle.png    — glass bottle layer (not tinted)

On enable / reload / catalog sync, DrinkBuilder uploads both PNGs to ProvinceSystem
(PUT /drinks/plugin/assets/…). The website and Discord review sheets load them from
the API — do not copy into ProvinceSystem or the frontend repo.
