# In-game character creation

[Project index](../README.md) · [Character selection](character-bodies.md)

The **New character** tab in character selection opens a welcome page.
**Create character** starts the native Minecraft dialog wizard. Character
creation is controlled entirely through its menus. It uses the same `stages.yml` definitions
as the website creator, with the configured in-game stage order and gates.
Existing slot limits, switching cooldowns and character restrictions still apply.

## Screens and navigation

Instructions appear together on a screen and remain until the player clicks
**Next**. Shared instruction stages use their website copy when it is available;
game-only instructions keep their game copy.

Names and clues use single-line fields; description uses a multiline field.
Age uses a slider bounded by the chosen race. Description also includes optional gender. Real-life age attestation
uses an explicit **Yes** or **No** choice followed by **Next**.

The name screen contains one name field and its preview. Donors can open
**Edit colours** to choose default, solid, gradient or custom hex colours within
their existing rank allowance (up to eight stops). Solid colour uses one picker;
gradient uses two; custom uses one space-separated hex field for longer gradients.
**Preview** checks and shows the colours. **Use colours** returns to the name;
**Back to name** discards colour-editor changes. Only **Next** commits the name
and colours. The name screen never shows unused colour slots.

Race, class and traits use direct clickable choice rows, with a checkbox marker
and hover description. Class colours remain visible. Unavailable choices stay
grey and cannot be ticked; their hover text names the conflicting trait or
explains the missing requirement, playtime gate, point cost or filled pick limit.
Unticking a choice reopens available alternatives. Longer lists use **Previous
choices** and **More choices** links only where another page exists.
Affected attributes appear as a compact current/result line, for example
**Dexterity: 2 → 3 (+1)**. Gains are green and losses red. Values include the
draft's race, saved traits and current ticks; single-pick replacement removes
the old choice's contribution. A removable checked trait's tooltip previews
unticking it. These previews do not change the character or allocate points.
Point costs use a separate colour. Attribute choices show the
point cost beside each rank and exclude ranks that exceed the entire budget.
**Check points** reports what remains; **Balanced** fills a valid allocation for
review. Only **Next** commits the allocation, which must use the whole budget.
Age and attribute inputs change locally. Clicking a choice updates its marker
and availability through a guarded callback, replacing the dialog directly.

**Back** and **Next** occupy a separate navigation row below the form. **Next**
validates and saves the current step, including dependencies, conflicts and
budgets. Errors appear inline and retain the entered values. **Back** retains
unconfirmed form values for this session. The step count reflects stages
available to this character. Saves do not send legacy chat messages, titles or inventory-close packets.
Next/Back replace the dialog directly without briefly returning to gameplay.
Short clue inputs avoid the multiline character counter overlapping navigation.

**Esc** cannot close selection, creation or discard confirmation. In the
character world, discarding a draft returns to selection; playing a character
or disconnecting leaves the menus. Normal chat cannot submit creation fields.
`/rpcharacter create` no longer starts creation. Navigation commands are retained
for existing-character editing and staff previews; a native draft uses its
screen controls. `/rpcharacter select` can recover the current menu.

## Review and finish

The review screen shows committed values for every available choice. Long
reviews have page links only where another page exists. Clicking **[Edit]** next
to a value opens that step; **Save and review**
validates the change and returns directly to review. **Back to review** returns
without committing the edited step.

Changing a race or another prerequisite clears traits that are no longer
available, including dependent traits. Newly available or invalidated required
steps must be confirmed before **Create character** can finish. Final validation
checks the name, class, birthday, description, clues, stage gates, trait
restrictions and attribute spending. Slot availability is rechecked before the
character is added to the roster. The coloured name shows the chosen appearance;
there is no separate hex-colour row. Back/Create occupy the action row without
empty spacer buttons.

**Cancel creation** asks whether to discard the draft. **Keep creating** returns
to the screen; **Discard draft** cancels. Logging out also discards the unfinished
draft. Screen callbacks accept only the current player connection and screen
revision, so a repeated or delayed click cannot create another character or
change a later step.

Skin uploads remain on the website's Wardrobe page. Editing an existing
character with `/rpcharacter edit` and staff stage previews retain their current
interfaces and paid-change rules.

## Verification

Run `tfmc-mvn -o -B clean verify` from the RPCharacters checkout with Java 21 and
the pinned dependencies prepared. Dialog tests exercise fields, choices,
navigation, review editing, point budgets, clue validation, cancellation and
stale callbacks. The repository enforces 100% production line coverage.

For a requested Dev playtest, exercise the full configured creator on Paper
1.21.10 with a Minecraft client, including a small window and different GUI
scales. Check readable option details, page controls, inline errors, Back,
review editing and boundary page links, donor palette/custom gradients, rank limits, optional gender,
Esc at every screen, discard returning to selection, logout and final character
activation. Check disabled-choice hover reasons and immediate pick limits.
Local sliders must leave the same screen in place; choice updates and Next/Back
must preserve the cursor, with no waiting screen or legacy chat/title overlay.
Unit tests do not prove client rendering or live server integration.

## Source references

- [Wizard screens](https://github.com/TF-Minecraft/RPCharacters/blob/main/src/main/java/net/tfminecraft/rpcharacters/creation/CreationWizard.java)
- [Creation lifecycle](https://github.com/TF-Minecraft/RPCharacters/blob/main/src/main/java/net/tfminecraft/rpcharacters/creation/CharacterCreation.java)
- [Shared creation rules](https://github.com/TF-Minecraft/RPCharacters/blob/main/src/main/java/net/tfminecraft/rpcharacters/creation/CreationRules.java)
- [Stage defaults](https://github.com/TF-Minecraft/RPCharacters/blob/main/src/main/resources/stages.yml)
