# Healing tick

Healing duration elapses in real time, including while a player is offline or a
character is inactive. The saved expiry controls the remaining time; the task
removes expired injuries and refreshes effects on active characters.

## Runtime behavior

[`InjuryHealingService`](https://github.com/TF-Minecraft/RPCharacters/blob/main/src/main/java/net/tfminecraft/rpcharacters/injuries/InjuryHealingService.java)
runs at `healing-tick-interval` in `injuries.yml` (default `1m`). It visits online
players with an active character, skipping dead players and pending permadeath
respawns. Traits missing duration state receive their full configured duration.
Expired traits are removed through `TraitChangeService`, with the lost-trait
message; remaining traits have their scaled effects refreshed.

The task does not subtract a fixed interval from saved time.
[`TraitInstanceState`](https://github.com/TF-Minecraft/RPCharacters/blob/main/src/main/java/net/tfminecraft/rpcharacters/objects/TraitInstanceState.java)
computes remaining duration from `expires-at-ms`. Inactive characters lose expired
traits when loaded from storage. See [trait persistence](trait-state-persistence.md).

## Verification

- Check that remaining time decreases for active, inactive and offline characters.
- Reload an inactive character after expiry and confirm the expired trait is absent.
- Confirm active-character completion removes the injury, updates effects and sends the lost message.
- Confirm penalties fade with the remaining fraction of the configured duration.
