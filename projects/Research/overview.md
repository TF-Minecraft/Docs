# Behaviour, configuration, and operations

[Research documentation](README.md) · [All projects](../../README.md)

## System model

Research treats every block of the configured `station.block` (default
`LECTERN`) as a research station. A station holds at most one active project,
owned by the player who started it. The project records its input, the output
rolled from that input, the result item resolved at the start, the points and
state of each aspect, the items already tested, and which aspect sits in each of
the six menu rows.

## Player flow

**Starting.** A player with a ready character session right-clicks a free station
while holding an enabled input's `start_item`. Research rolls one of the input's outputs by weight,
resolves its result, and then consumes `start_item.amount` from the hand used.
If the rolled output is disabled or its result cannot be resolved, nothing is
consumed. The project belongs to the character who started it. Other players,
and other characters on the same account, get an "in use" message and cannot
add their focus to it; the starting character reopens the menu. A station saved
before characters were recorded belongs to the next ready character to open it.
Without a ready shared session, Research leaves start items and station ownership
untouched. The optional `station.character_required` message explains this;
existing message files without that key use a built-in message.

Lecterns without an active project retain vanilla book handling: players can
place a written book or book and quill, or open a book already on the lectern.
A book in the other hand also works when the interacting hand is empty. Remove
an existing book before starting research; an active project takes precedence
over book interactions.

**Experimenting.** Clicking an item in the player's inventory moves one of it
into the experiment slot, and clicking the slot returns it. Only items listed in
an aspect's `primary_items` or `secondary_items` are accepted, and each item path
can be tested once per project. Preview slots show the item's aspects, their
status, and the points they would add. Confirming spends
`mental_points.experiment_cost`, returns the item, and adds
`experiment.primary_points` and `experiment.secondary_points` to the item's
primary and secondary aspects. When `external_modifiers.experiment.aspect_point_bonus_percent`
is set, each grant is increased by that fraction, rounded down. Points on
required aspects are capped at `required_points`. Aspects the output does not
need collect up to `experiment.reject_points` and are then rejected; an item
whose aspects are all rejected cannot be confirmed.

**Discovery.** Each required aspect row has five panes; pane *k* fills at
`ceil(k × required_points / 5)`. With *A* as the player's total in the MMOCore
attribute `attributes.discovery.mmocore_id`:

| Stage | Reached when points are at least | Row shows |
| --- | --- | --- |
| Hidden | — | Divider and inactive panes, like a decoy row. |
| Undiscovered | `required_points` × max(`min_reveal_percent`, `base_reveal_percent` − *A* × `reveal_percent_reduction_per_point`) | `aspect_tested_unknown` icon and unknown panes. |
| Confirmed | `required_points` × max(`min_confirm_percent`, `base_confirm_percent` − *A* × `confirm_percent_reduction_per_point`) | The aspect's display item and revealed panes. |

The reveal values are under `aspect_discovery` and the confirm values under
`aspect_confirm`. The mystery display switches to the product display once the
number of confirmed required aspects reaches
`product_reveal.base_after_confirmed_aspects` minus the attribute bonus
(*A* × `product_reveal_bonus_per_point`, capped at `caps.product_reveal_bonus`),
rounded to the nearest whole number. Because halves round up, a bonus of 0.5
or less, including the default cap, leaves the base unchanged. An output without
`product_reveal` reveals its product at the first confirmed aspect.

**Completing.** The project completes when every required aspect is confirmed
and at full `required_points`. The result item pops above the station as a
dropped item that anyone can pick up, `ResearchCompleteEvent` fires, and the
station is cleared. If the result cannot be built or spawned, a warning is
logged and the project stays open. The scrap button asks for confirmation and
then discards the project without refunding the start item. Breaking the
station block scraps its project in the same way.

## Station menu

The menu is a six-row chest. The left panel holds the scrap button (slot 0),
the mystery or product display (10), the experiment slot (27), the primary and
secondary previews (28 and 37), the mental points display (45), and the confirm
button (47). Column 3 and columns 4–8 hold six aspect rows. Required aspects are
shuffled into random rows when the project starts, and the remaining rows are
decoys, so an output can require at most six aspects. After each experiment, a
pulse in the scoring aspect's `pulse_color` crosses the left panel.

Each menu belongs to the session that opened it. When that session ends, the
menu closes and returns its experiment item once, before the outgoing character
is saved. At server stop, Research disables before RPCharacters and returns the
item itself. A menu from an earlier session cannot spend focus or scrap a
project, even after switching back to the same character. Delayed refreshes and
completion sounds stop with the session; station and dropped-item particles
still play.

## Configuration files

The plugin copies `config.yml`, `gui.yml`, and `messages.yml` into
`plugins/Research/` on first start and creates empty content folders; no
example content is shipped.

| File | Purpose |
| --- | --- |
| `config.yml` | Station block and optional use permission, start and completion effects, result pop motion, experiment cost, experiment points and `reject_points`, discovery attribute and product-reveal bonus, reveal and confirm thresholds, and optional `external_modifiers`. |
| `gui.yml` | Menu item paths (`items`), titles and button labels (`labels`), and hex colour tokens (`colors`). Slot positions are fixed in code. |
| `messages.yml` | Chat and menu text, with a `prefix` added to chat messages. |
| `aspects/*.yml` | Aspects keyed by identifier: `name`, `lore`, `display.item`, `pulse_color` (or a `grid_color` name), `sounds` (`input`, `confirm`, `volume`, `pitch`), `primary_items`, and `secondary_items`. |
| `templates/*.yml` | Templates keyed by identifier, each with an `outputs` list of `item` and `weight`. An `item` may be another template as `t.<id>`; cycles are rejected. |
| `outputs/*.yml` | Outputs keyed by identifier: `enabled`, `mystery_display.item`, `product_display.item`, `product_reveal.base_after_confirmed_aspects`, `aspects.<aspect>.required_points` (above zero), and a `result` with exactly one of `item` or `template: t.<id>`. |
| `inputs/*.yml` | Inputs keyed by identifier: `enabled`, `start_item` (`item`, `amount`), and an `outputs` list of `id` and `weight`. |

The folders load in the order aspects, templates, outputs, inputs, so outputs
may reference aspects and templates, and inputs reference outputs. Within a
folder, files load in file-name order, ignoring case. Identifiers must be
unique within each folder: when one repeats, the file that loads first keeps it
and the later copy is logged and skipped. Each start item may belong to only one
input. If an item path is listed as primary (or secondary) on two aspects, the
conflict is logged and the aspect loaded last wins.

Item paths use `vanilla.MATERIAL` (or TLibs `v.MATERIAL`), `m.TYPE.ID` for
MMOItems, and `ia.namespace:id` for ItemsAdder; other prefixes are rejected.
Paths that cannot be built are accepted with a warning. Sounds take Minecraft
sound keys such as `entity.player.levelup` or `namespace:id`, and particles
take Bukkit particle names. Text accepts `#RRGGBB` and `&` codes through TLibs.

Run `/research reload` after editing these files. A reload reports failure when
any definition is invalid, but definitions that failed validation are still
registered, so fix every logged error. Reloading does not touch active stations,
which keep their rolled output and result, so keep input and output identifiers
in place while projects use them. Research recognises its menus by title; close
open station menus before changing `labels` titles or `colors.inventory_title`.

## Commands and permissions

| Command or setting | Effect |
| --- | --- |
| `/research reload` | Reload all configuration and content. Requires `research.admin`, which defaults to operators. |
| `station.permission` | Optional permission to use stations. When set, Research ignores clicks from players without it, and the block behaves normally. |

## Integrations

- **RPCharacters Focus.** Mental points are the RPCharacters Focus pool for the player's
  active RPCharacters character, shared with Magic meditation. The cap and
  regeneration, including attribute bonuses, are set in RPCharacters `focus.yml`. A
  player without an active character has no points and cannot experiment.
- **MMOCore.** The discovery attribute is read as the attribute's total value;
  a missing attribute counts as zero.
- **TLibs.** TLibs builds and matches every item path, formats text, and supplies
  shared character identity and session events through RPCharacters' provider.
  Research needs TLibs 2.3.0 or newer; with an older TLibs it logs a severe
  error and disables itself. Estates need TLibs 2.6.0 (see below); on 2.3.0 to
  2.5.0 Research runs normally and logs that stations of dead characters stay
  with them.
- **Estates.** With TLibs 2.6.0, Research is the `research` participant in
  RPCharacters estates. When a dead character's estate is decided, every station
  whose recorded character is the dead one goes to the estate's property
  recipient (the will heir, or the death guild's leader): the station file's
  owner account and character are both rewritten, so the recipient's character
  carries on the project with its progress. A recipient on the same account keeps
  the account and takes the character. Waiting or frozen property leaves the
  stations with the dead character, unusable, until staff assign it. Moves happen
  only while the character is still dead with that death and the estate is
  decided at the current revision; a revived character keeps what had not moved.
  Before changing any station, Research writes
  `plugins/Research/data/estates/<deathId>.json` listing the stations it will move
  and the recipient, and marks each one moved; a crash between stations is
  finished at the next settle. The outcome sent to the estate lists every moved
  station's `<world>_<x>_<y>_<z>` key, which `/estate show` displays; to undo a move
  by hand, give those stations whose owner is still the recipient back to the dead
  character. A station that fails to save keeps its old owner and is retried. The
  will screen and `/estate show` list the character's stations. Research settles
  decided estates on the first tick after start-up and every hour, and reports
  only changed answers. Stations without a recorded character are never moved.
- **`ResearchCompleteEvent`.** Listen for
  `net.tfminecraft.research.event.ResearchCompleteEvent`, which fires
  synchronously after the result spawns and cannot be cancelled. It exposes
  `getPlayer()`, `getInputId()`, `getOutputId()`, and `getResultItemRef()`, the
  resolved item path rather than a `t.` template. `getProjectId()` is a
  deprecated alias for `getOutputId()`.

## Persistence and shutdown

- Each active station is a JSON file under
  `plugins/Research/data/stations/`, named `<world>_<x>_<y>_<z>.json`, holding
  the owner account and character, input, output, result path, product
  reveal, aspect points and states, tested items, and row order.
- Station files are written when a project starts, after each confirmed
  experiment, when an estate moves the station, and on a normal plugin disable.
  Each write goes to a temporary file that is flushed and then moved over the
  station file, so a crash leaves the old or the new file whole. They are deleted when a project
  completes, is scrapped, or its block is broken.
- On start, files that reference an unknown input, output, or world are skipped
  with a warning and left on disk. A missing or stale row order is reshuffled.
- Session cleanup leaves the station and its progress intact. Normal plugin
  disable returns held experiment items directly, even after the identity provider
  or Research's event listeners have stopped, and then saves the stations.
- The station JSON schema is unchanged. New ownership uses the canonical character
  UUID; existing UUID strings compare without regard to letter case and are not
  rewritten.
- **Heir backfill (once per server).** Stations saved before characters were
  recorded go to their account's reviewed heir, as locks and vehicles did in stage
  6a. On a start-up where TLibs reports reviewed heirs ready, Research inventories
  the persisted station files independently of recipe and world loading. Valid
  ownership metadata with no recorded character goes to its account's legacy heir,
  including stations skipped for an unknown input, output or world. The plan at
  `plugins/Research/data/backfill-character-v1/plan.json` records each station's
  original account and fixed heir before any change. An heir on another account
  is refused. The original station file is backed up durably to `backup/` in that
  folder (never overwritten); only the ownership field is then written atomically,
  preserving recipe, progress and extension fields. Loaded stations receive the
  same ownership change.
  `done.json` records the filled count, stations whose account had no heir, and
  invalid, missing or changed station files skipped for staff review. These lists
  are also logged. Once the marker exists, later starts do nothing. If heirs are
  not ready, or a planned station cannot be read, backed up or saved, no marker is
  written and the next start reuses the same plan. Replay checks the file's location
  and original account and leaves a station claimed by another character alone;
  incomplete or unreadable plans are refused. Stations whose account has no heir
  stay unassigned: the first ready character on their owner account claims them
  when it opens them. Stations the backfill filled belong to the heir only.

Back up the complete `plugins/Research/` directory before renaming identifiers
or migrating configuration, and stop the server cleanly before copying live
state.

## Validation

For a server-side change, verify the following on Paper 1.21.10 with the pinned
dependency set:

1. Start with both an empty data directory and a copy of representative station
   data.
2. Confirm all aspects, templates, outputs, and inputs load, and that
   `/research reload` succeeds without severe errors or unbuildable item paths.
3. Start a project with each start item, and confirm only the held item is
   consumed and that another player, or another character on the same account,
   sees the station as in use.
4. Run experiments, checking previews, mental point spending, repeat-item
   refusal, off-recipe rejection, and reveal timing at low and high values of
   the discovery attribute.
5. Complete a project, and confirm the result spawns, a test listener receives
   `ResearchCompleteEvent`, and the station is cleared.
6. Scrap one project and break the block under another.
7. Restart cleanly mid-project and confirm ownership, progress, tested items,
   row order, and the rolled result are restored.
8. With an experiment item held in the menu, switch characters, quit, permanently
   kill the character, and stop the server. Verify one refund, including an item
   dropped when inventory space is full, and unchanged station progress. Switching
   away and back must invalidate the old menu and its pending refresh.
9. Check that loading or unavailable characters cannot start or claim projects,
   and that an older station with an uppercase character UUID remains accessible
   to its owner. A provider shutdown must not transfer ownership to the account
   or another character.
