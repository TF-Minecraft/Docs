# ConditionalEvents

[Project index](README.md)

## Account or character data

`one_time` and `cooldown` remember who has run an event. By default that memory belongs to the account, as upstream. Set `data_scope: character` to give each roleplay character its own:

```yaml
Events:
  research_bronze:
    type: item_interact
    one_time: true
    data_scope: character
```

A per-character event runs only while a character is in play. It does not run at join before a character is chosen, in the selection room, or after the session has ended on quit, so use the account scope for join and leave events. Per-account events behave as before. Any other `data_scope` value logs a warning and counts as `account`.

Use the character scope for anything a character learns or earns, such as Codex unlocks, since [Codex](../Codex/overview.md) keeps a journal per character. Keep supporter perks and other account rewards per account. The supporter EXP booster is `/tfmc booster` in TFMCCore and is per account.

## Stored data

Each account's file, `plugins/ConditionalEvents/players/<account>.yml`, keeps account events under `events` and per-character events under `characters.<character>.events`. When a character session starts, any account-level data for events now set to the character scope moves to the account's RPCharacters heir (or, if that heir has since been deleted, its most-played living character), the same character that received the account's money, body and Codex discoveries. An event done once stays done, and the later cooldown start wins. The server log records each move as `Moved <n> per-character event records of account <account> to character <character>`.

`/ce reset <player> <event|all>` and `/ce reset * <event|all>` clear the account and every character.

## Codex events on Main

`codex.yml` and `codex_research.yml` unlock Codex entries with `one_time` events, so they need `data_scope: character`. Otherwise a second character could not earn an achievement, duchy title or research entry its account already has.
