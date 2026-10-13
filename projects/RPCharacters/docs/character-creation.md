# In-game character creation

[Project index](../README.md) · [Character selection](character-bodies.md)

The **New character** button in character selection and `/rpcharacter create`
open a native Minecraft dialog wizard. It uses the same `stages.yml` definitions
as the website creator, with the configured in-game stage order and gates.
Existing slot limits, switching cooldowns and character restrictions still apply.

## Screens and navigation

Instructions appear together on a screen and remain until the player clicks
**Next**. Shared instruction stages use their website copy when it is available;
game-only instructions keep their game copy.

Names and ages use fields; descriptions and player-authored clues use multiline
fields. Real-life age attestation uses explicit **Yes** and **No** choices.
Race, class and trait screens show selectable buttons, details and remaining
points. Long lists have **Previous choices** and **More choices** pages. Attribute
screens use increase/decrease buttons and require the whole point budget.

**Next** validates and saves the current step. Validation errors appear on the
same screen, retaining the submitted text. **Back** retains field text and
unconfirmed choices for the session. A previously saved step can be submitted
again. The step count reflects stages available to this character.

**Esc** closes the screen. `/rpcharacter create` or `/rpcharacter help` reopens
the current draft. Text is captured when a screen button is clicked; typing
dismissed with Esc is not submitted. Normal chat cannot submit creation fields.

## Review and finish

The review screen shows committed values for every available choice. Long
reviews have page controls. Clicking **Edit** opens that step; **Save and review**
validates the change and returns directly to review. **Back to review** returns
without committing the edited step.

Changing a race or another prerequisite clears traits that are no longer
available, including dependent traits. Newly available or invalidated required
steps must be confirmed before **Create character** can finish. Final validation
checks the name, class, birthday, description, clues, stage gates, trait
restrictions and attribute spending. Slot availability is rechecked before the
character is added to the roster.

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
review editing, cancel/resume, logout and the final character activation.
Unit tests do not prove client rendering or live server integration.

## Source references

- [Wizard screens](https://github.com/TF-Minecraft/RPCharacters/blob/main/src/main/java/net/tfminecraft/rpcharacters/creation/CreationWizard.java)
- [Creation lifecycle](https://github.com/TF-Minecraft/RPCharacters/blob/main/src/main/java/net/tfminecraft/rpcharacters/creation/CharacterCreation.java)
- [Shared creation rules](https://github.com/TF-Minecraft/RPCharacters/blob/main/src/main/java/net/tfminecraft/rpcharacters/creation/CreationRules.java)
- [Stage defaults](https://github.com/TF-Minecraft/RPCharacters/blob/main/src/main/resources/stages.yml)
