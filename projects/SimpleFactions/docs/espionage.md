[SimpleFactions](../README.md) · [All projects](../../../README.md)

# Espionage and special positions

A faction's **Spymaster** decides how much it can learn about other factions and how much
they can learn about it. Office and espionage code lives in
[`espionage/`](https://github.com/TF-Minecraft/SimpleFactions/tree/main/src/main/java/net/tfminecraft/simplefactions/espionage);
its settings live in
[`special-positions.yml`](https://github.com/TF-Minecraft/SimpleFactions/blob/main/src/main/resources/special-positions.yml).

## What players see

Foreign faction and guild menus show public identity and flavour details: faction leaders'
character names when available, government, rank, tier, titles, settlements, culture,
religion, guild types, allies and subjects. Prestige is public and its ranking uses exact
values. Other figures are hidden or shown as intelligence ranges. Members always see exact
information about their own faction and guilds. These rules cover in-game menus; website
exports and staff administration commands are not masked.

A faction without an eligible, living Spymaster reveals exact information to everyone,
including its guild menus, complete rosters, ledgers and wealth rankings. No daily estimates
are generated about an unguarded faction. This takes effect when menus are reopened,
including after removal, permanent character death or a solo leader becoming ineligible.
Appointing an eligible Spymaster restores the usual intelligence checks, even if their
aptitude is 0. Public viewing does not grant management authority or access to private
sabotage settings.

Without an eligible Spymaster, a faction also receives no daily reports about protected
foreign factions. Cached reports become unreadable immediately; private fields remain
**Unknown** and the menu shows "Report quality: Absent" with "The Spymaster's office stands
vacant; no findings reach your court." Unguarded foreign factions and normally public
information remain visible. Refilling the office restores access to any still-current
cached reports.

## Staff viewing permission

Staff with the bypass permission see the original exact faction and guild menus, complete
rosters, ledgers and rankings, plus Minecraft account names alongside character names. The
node is set in `plugins/SimpleFactions/special-positions.yml`:

```yaml
espionage:
  bypass-permission: simplefactions.espionage.bypass
```

Missing or blank values use the default node above. Changing the node does not assign
permissions; grant the configured node through LuckPerms. `simplefactions.espionage.bypass`
defaults to false and must be assigned explicitly.

Bypass viewers skip daily intelligence gathering and its notices; their views do not
generate or change faction reports. The permission grants information access only: faction
management and private Spymaster conduct keep their leader and office-holder requirements.
Bypass viewers see exact foreign offices without gaining appointment authority. Removing the
permission restores the usual membership and intelligence checks.

For the staff track (`staff_player` → `staff_inactive` → `staff`), grant the node explicitly
to `staff` and deny it for `staff_inactive`; explicit denials inherited from lower ranks
override a generic `*` grant. Dev and Main share one LuckPerms database, so use the
`server=dev` context for a Dev-only grant. After a rank change, reopen the menu on a foreign
faction with an eligible Spymaster: own and unguarded faction information stays exact at
every rank.

## Appointing a Spymaster

Open **Special Positions** in the faction menu or use `/faction positions`, then select
**Spymaster**. The menu is an office directory, ready for additional positions.

- `/faction spymaster <player>` appoints a member.
- `/faction spymaster remove` leaves the office vacant.
- `/faction espionage` opens the holder's private settings, or the office menu for other
  members.

Only the faction leader can appoint or remove the Spymaster. The appointee must be an online
member with an active RPCharacters character. The faction leader is ineligible unless the
faction has only one member across all its guilds; a solo leader uses 25% of their permanent
aptitude, rounded down. If another member joins, the leader's office becomes vacant when it
is next checked. Missing or ineligible Spymasters have aptitude 0.

Only the appointee receives the roleplay appointment letter and their aptitude in chat.
Member and candidate entries use character names and guild affiliations. Appointment
commands and invitations accept either full character names (including spaces) or Minecraft
account names; only online players match, matching is exact and ignores case, and duplicate
character names require the account name.

### Founding offices and appointment costs

A new faction automatically assigns its founder to the office, subject to the solo-leader
aptitude penalty. This automatic assignment does not count as the first deliberate
appointment. The first deliberate appointment is free and causes no unrest. Every later
appointment costs **250d** from the faction treasury and causes **−10 stability points**,
fading linearly over **7 real days**. Removing an office holder does not reset the history.
Unrest persists across restarts, progresses during downtime, and repeated replacements stack
their own decaying penalties. Saves from before appointment counting was recorded treat an
existing deliberate holder, or a stored legacy aptitude roll, as having used the first
appointment.

```yaml
espionage:
  appointments:
    repeat-cost: 250.0
    stability-penalty: 10.0
    penalty-days: 7.0
```

Zero disables the corresponding cost or penalty.

An empty or ineligible office also applies a persistent **Vacant Spymaster** stability
penalty until it is filled, including offices never deliberately assigned and holders who
leave. `positions.spymaster.vacancy-stability-penalty` defaults to 10 points; zero disables
it. This is independent of the replacement unrest.

### Character death

Permanent RPCharacters character death removes that character's Spymaster office and keeps
the paid appointment history. Ordinary Minecraft respawns and cancelled character deaths do
not remove the office. Removal is confirmed after the death event commits, and loaded
assignments for dead characters are rejected when checked.

## Aptitude

Aptitude rolls **once per character**, independent of faction membership. Leaving, rejoining,
transferring factions, removal and reappointment, deleting a faction and restarting do not
reroll it. A server-wide registry stores these values in
`plugins/SimpleFactions/Cache/character-aptitudes.json`; offices and daily reports remain in
the faction JSON.

On startup the registry imports aptitudes stored per faction by older saves without
rerolling them. If a character has several faction-specific values, an existing registry
entry wins; otherwise the first faction ID alphabetically supplies the permanent value.

The roll uses permanent MMOCore attribute bases (creation, traits and allocated points;
equipment bonuses excluded), capped to 0–16 and centred at 6. Without MMOCore, aptitude uses
RPCharacters' saved attribute values.

```
base aptitude = clamp(round(50 + sum(weight * (attribute - 6)))
                      + uniformInteger(-20, 20), 0, 100)
```

Default weights, set under `espionage.aptitude.attribute-weights`:

```yaml
espionage:
  aptitude:
    attribute-weights:
      intelligence: 3.0
      wisdom: 2.5
      charisma: 1.5
      dexterity: 1.0
      constitution: -2.0
      strength: -2.0
```

Weights can be positive, zero or negative; non-finite weights, or weights beyond ±1000, fall
back to the defaults. Low mental and social scores and high strength or constitution
penalise aptitude. Physical specialists with mental attributes at 6 and strength and
constitution at 16 roll 0–30. Strong mental and social builds with low physical attributes
can reach 100; physical builds with poor judgement can reach 0. Configuration changes affect
only the first roll of new characters; existing permanent aptitudes are kept.

## Daily intelligence

Any `/faction` or `/guild` command that opens a GUI requests the faction's reports on
protected foreign factions when its own Spymaster is eligible, including list, menu,
positions, espionage and Spymaster settings commands. The first member to open a GUI by
command that UTC day triggers the checks; all faction members share the reports. Faction and
guild clicks, sorting and periodic GUI refreshes only read cached reports and never roll or
send intelligence messages. Commands that do not open a menu never gather intelligence.
Protected uncached information stays hidden until a member opens a GUI by command. One
roleplay notice goes to the requesting player when new reports are created.

Days run from midnight to midnight **UTC**. Each faction rolls offence and defence once per
day:

```
offense = round(1.25 * effective aptitude + mean(3 uniformInteger(-75, 75))) - offensiveSabotage
defense = round(1.25 * effective aptitude + mean(3 uniformInteger(-75, 75))) - defensiveSabotage
margin  = observer.offense - target.defense
```

Averaged luck makes a full 0-versus-100 upset exceptionally rare (roughly 0.002% with
defaults), while smaller aptitude gaps can still be overcome. Each ordered observer/target
pair has one snapshot per day. Reopening menus, replacing Spymasters, sabotage changes and
restarts do not reroll the day's intelligence; other changes affect the next uncached rolls.
A recreated target faction receives a fresh report.

| Margin | Intelligence | Approximate range width | Known non-leader members |
| --- | --- | --- | --- |
| <= 0 | Rumours | Up to 300% | 20% |
| 1–29 | Rumours | 300% of magnitude | 20% |
| 30–64 | Broad estimates | 150% | 40% |
| 65–99 | Reliable estimates | 40% | 60% |
| >= 100 | Detailed estimates | 20% | 80% |

Reports always have at least Rumours quality, including negative margins. Every guild in a
faction shares that day's quality. A missing or invalid stored report uses the
zero-information category **Botched report**, with private fields Unknown.

### Rosters

Member samples are rounded down, capped at 23, and saved with the report so reopening cannot
reveal extra names. They contain character names and guild affiliations; foreign reports
show Unknown for missing character names, while own views, staff bypass and invitations fall
back to account names. The faction leader is always displayed separately alongside the
member-count range. Guild rosters use the same sample, filtered by guild; guild leaders and
office identities use their own tier gates. All rosters distinguish the leader, guild
leaders and office holders. The leader uses the faction's custom ruler title, defaulting to
Leader. Subjects belong only to their own roster. The realm guild always comes first,
followed by other guilds in descending visible wealth (estimated midpoints for foreign
views).

### Estimates

Ranges are rounded, asymmetric snapshots containing the true value when generated. They
never collapse to an exact number, including zero. Reports cover members, wealth,
prosperity, daily net income, professional army, levies, mercenaries, installations,
stability and administrative power. Professional army counts filled professional soldier
slots, excluding equipment and mercenaries. Guild wealth, member count, net income and trade
power have separate estimates.

Missing or unusably broad estimates display as grey **Unknown**. Counts, prosperity and trade
power cannot be negative; guild member estimates respect the configured guild capacity.
Stability estimates are limited to 0–100% and become Unknown if they exceed their tier's
maximum span (65 points at Broad, 50 at Reliable and Detailed). The faction tooltip shows the
stability state at the bounded range's midpoint in the usual state colours; the Government
item shows the range in that colour. Unbounded metrics become Unknown when their interval is
too broad relative to its midpoint or spans zero. Wealth and income keep meaningful negative
estimates for debt and deficits. These rules also apply when reading older cached reports,
without rerolling or changing them.

### Rankings

Prestige ranking uses public exact values. Wealth and member rankings and guild rankings
compare known range midpoints, with exact values for the viewer's own faction. Unknown
entries appear alphabetically after ranked known entries and have no numeric rank. Guild
income leaderboards use the same policy.

## Foreign menus

Foreign tooltips keep the same colours, spacing and field order as own entries, and foreign
faction and guild views keep their familiar slot layouts, inventory sizes, template icons
and back routes. Foreign menus allow diplomacy and guild browsing, plus read-only masked
ledgers, military, government, laws, installations and upgrade windows. Private menus
recheck membership before interacting or refreshing.

- **Ledgers** show daily income, expenses, net income and a reported accounts menu in the
  original ledger slots. Available cashflows appear under Income or Expenses, without a long
  list of Unknown categories; the detail windows keep the 27-slot layout, and cashflow
  estimates remain in the Ledger tooltip. Trade breakdowns and dividends use the same
  snapshot. Dividend percentages stay within 0–100% and cashflows respect their valid signs.
  Fields missing from an older report stay Unknown until the next day's report; opening a
  ledger never regenerates it.
- **Guild branches** return to their normal building slots; levels and effects are
  estimates gated by `buildings`. Guild upgrades and the upgrade queue use `upgrades`.
- **Military** opens normally; regiment counts are gated by `professional-army` and
  `levies`, and the training queue by `training`.
- **Government** legitimacy and council size use `government`; numeric tax rates use
  `taxes`; selected laws use `laws`.
- **Installations** identity, levels and construction use `installation-details`.
- **Special Positions** is a read-only report using the same daily comparison. Office names,
  vacancy and aptitude ranges are saved snapshots; holder-only sabotage choices are never
  included.

Hidden categories keep their menu entry with Unknown details. Foreign views cannot submit
proposals, train troops, upgrade buildings, cancel queues or modify another faction, and
periodic refreshes never replace a masked snapshot with an exact submenu.

Report headings use RPCharacters' lore calendar (year offset and era) and name the observing
faction's Spymaster in their roleplay closing line. Daily refresh boundaries remain UTC.

## Private sabotage

The Spymaster can select their office and click their own head to inspect private conduct.
Offensive and defensive sabotage are separate voluntary settings, both **disabled (0)** on
appointment. Click to cycle through reductions of 0, 25, 50, 75 and 100 roll points, or use:

```
/faction spymaster sabotage offense <0|25|50|75|100>
/faction spymaster sabotage defense <0|25|50|75|100>
```

Only the office holder can see or change these controls. Preferences persist through
restarts and reset on a new appointment. Selecting 0 disables that side again. Existing daily
rolls and reports remain unchanged.

## Configuration reference

All office and espionage settings live in `plugins/SimpleFactions/special-positions.yml`.
Missing settings are populated from the bundled defaults on startup or reload; existing
values always win. If the file does not exist but `config.yml` still has an `espionage`
section, those values (custom weights, costs and permission nodes) are copied across,
`config.yml` is backed up to `config.yml.before-special-positions`, and the section is
removed from `config.yml`.

| Key | Default | Purpose |
| --- | --- | --- |
| `positions.spymaster.vacancy-stability-penalty` | `10.0` | Stability lost while the office is vacant or ineligible. |
| `espionage.bypass-permission` | `simplefactions.espionage.bypass` | Exact-view permission for staff. |
| `espionage.reload-permission` | `simplefactions.espionage.reload` | Permission for `/faction reloadespionage`. |
| `espionage.appointments.*` | `250.0`, `10.0`, `7.0` | Repeat cost, unrest points and unrest days. |
| `espionage.aptitude.base` | `50.0` | Starting score before attribute weights. |
| `espionage.aptitude.attribute-center` / `attribute-cap` | `6` / `16` | Attribute centring and cap. |
| `espionage.aptitude.random-spread` | `20` | Random ± added to the aptitude roll. |
| `espionage.aptitude.solo-leader-multiplier` | `0.25` | Aptitude kept by a solo leader. |
| `espionage.aptitude.attribute-weights.*` | see above | Attribute weights. |
| `espionage.checks.aptitude-multiplier` | `1.25` | Aptitude multiplier in the daily roll. |
| `espionage.checks.luck-spread` / `luck-draws` | `75` / `3` | Luck range and number of averaged draws. |
| `espionage.intelligence.tiers.<tier>.*` | see file | Margin thresholds, uncertainty, roster fractions and useful range widths. |
| `espionage.intelligence.maximum-roster-size` | `23` | Maximum sampled roster names. |
| `espionage.intelligence.minimum-tiers.*` | see below | Minimum tier for each field. |

Out-of-range values fall back to their defaults.

### Disclosure gates

`espionage.intelligence.minimum-tiers` sets the lowest tier at which each field is shown.
Lower tiers show broader ranges when useful. By default:

- **Rumours:** members, roster, wealth and guild members.
- **Broad:** prosperity, stability, levies, installations, net income, trade power, ledger
  totals and guild buildings.
- **Reliable:** professional army, mercenaries, administrative power, individual cashflows,
  dividends, office holders, guild leaders, training, upgrades, taxes, laws, government and
  installation details.
- **Detailed:** office aptitude.

A value of `unknown` disables that field. Invalid or unconfigured fields fail closed.
`cashflows` accepts per-category overrides by enum name, such as `TRADE: broad`. The gates
apply when generating **and reading** reports, including old caches. Faction leaders remain
public.

## Staff test refresh

`/faction reloadespionage` reloads `special-positions.yml`, clears every faction's daily
offence and defence rolls and reports, then immediately rebuilds all foreign reports. It
works in game and from the console, requires the reload permission (default false), and
deliberately overrides the once-per-day rule for testing. Reopen menus afterwards to see
the refreshed reports. It preserves permanent aptitude, office holders, sabotage
preferences, appointment counts, treasury and unrest.

`/faction reloadconfigs` (admin) reloads settings, including `special-positions.yml`,
without regenerating reports.

## Saving and failure handling

Office appointments, removals and sabotage changes report success only after the faction
save succeeds. Failed saves restore the previous office state and refund any appointment
charge; faction JSON is staged before replacing the previous save. Daily refreshes batch
faction saves once per changed faction. A startup failure before faction restoration
completes cannot overwrite faction saves or the saved timer during shutdown.

A founder whose aptitude cannot be saved, or who has no active character (or RPCharacters is
disabled), stays pending. The office is retried when next checked while the founder has an
active character; a failed roll is never finalised as a permanent zero and never consumes the
free appointment. Pending founder appointments keep their character identity, and an
unrelated character death cannot cancel them. Changed pending identities are saved
immediately during office lookups, or once with the faction's report batch, so they survive
an unexpected process exit. Failed immediate saves restore the previous identity and keep
initialisation pending, so a later lookup can retry without consuming an appointment.

## Verification

Automated tests run with `mvn clean verify` (Java 21) and cover attribute weights and
extremes, daily luck, estimate bounds, caching, character aptitude persistence and
migration, leader eligibility, solo penalties, sampled rosters, rank privacy and
permissions.

On a test server, use `/faction menu`, then compare reports from two members, test prestige
and wealth sorting, browse foreign guilds and inspect private conduct. Use
`/faction reloadespionage` to regenerate the day's reports between checks.
