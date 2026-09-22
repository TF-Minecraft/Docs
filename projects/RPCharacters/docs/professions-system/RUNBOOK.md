# Professions verification

Build from `main` with the committed dependencies. Review `professions.yml` and per-profession YAML files before deployment. Keep a matching jar, configuration and data backup for recovery.

## Post-deploy verification

- [ ] `/profession` opens main menu on a character with active RP character
- [ ] MMOCore profession level-up grants lifetime points (account-wide)
- [ ] Purchasing upgrade on Character A spends from A's loadout; Character B still has full free pool
- [ ] Character switch strips Character A `professions.*` LuckPerms; Character B perks apply
- [ ] Crafting station permission checks still work (`professions.*` recipe conditions)
- [ ] Breeding lock/unlock behaves as before
- [ ] `/profession top <prof>` lists online players
- [ ] `/profession restoreall` / `fixperms` if LP nodes look wrong after first login

## External configs

- AdvancedCrafting and other plugins using `permission-prefix: professions.` — **no change needed**
- MMOCore profession IDs must match `professions/*.yml` filenames
