# ConditionalEvents

[Project index](README.md)

## Account or character data

`one_time` and `cooldown` remember who has run an event. In this copy that memory belongs to the roleplay character being played. Set `data_scope: account` to keep it per account instead, as upstream:

```yaml
Events:
  act1_exp_catchup:
    type: repetitive
    one_time: true
    data_scope: account
```

The scope only matters for events with `one_time` or a `cooldown` that involve a player. Other events have nothing to keep and run as upstream: join messages, `server_start`, `player_pre_join`, and commands without a cooldown.

An event that keeps per-character data runs only while a character is in play, so not at join before a character is chosen, in the selection room, or after the session has ended on quit. Use `data_scope: account` for join and leave events that keep data. A run belongs to the character it started for: if that character leaves before a delayed action is due, for example during `wait_ticks`, the rest of the actions, including action groups it calls with `execute_action_group`, are dropped, and the run's one-time flag and cooldown are undone so the character can earn it again. The undo skips anything a later run or a staff reset changed since. With `retain_player_data_until_restart: false`, a player who logs out mid-run has already been saved, so the marks stay; Main keeps player data until restart. Any `data_scope` value other than `character` or `account` logs a warning and counts as `character`.

Keep anything a character learns or earns per character, such as Codex unlocks, since [Codex](../Codex/overview.md) keeps a journal per character. Use `data_scope: account` for supporter perks and other account rewards. The supporter EXP booster is `/tfmc booster` in TFMCCore and is per account.

## Stored data

Each account's file, `plugins/ConditionalEvents/players/<account>.yml`, keeps account events under `events` and per-character events under `characters.<character>.events`. As a one-off, on an account's first character session after the change, its old account-level entries for events that are now per character move to its most-played living character (else its most-played character), the same character [Codex](../Codex/overview.md) copies the old journal to. An event done once stays done, and the later cooldown start wins. The file records `seeded-to: <character>` so this happens once; if RPCharacters cannot list the account's characters yet, it waits for a later session. Every other character starts these events fresh. Account-scoped events keep their data on the account.

`/ce reset <player> <event|all>` and `/ce reset * <event|all>` clear the account and every character.

## Events on Main

Main has 90 events that keep data. The 87 Codex unlocks in `codex.yml` and `codex_research.yml` and the meditation cooldown in `r_lore.yml` are per character by default, so a second character can earn an achievement, duchy title or research entry its account already has. `act1_exp_catchup` and `act1_exp_catchup_retry` set `data_scope: account`, so the one-off catch-up from before characters had their own progress does not arm again for every character.
