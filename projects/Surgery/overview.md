# Surgery

**A physician operates on another character's healing injury, using Victorian instruments, and a successful operation cures that ailment in RPCharacters.**

![Java](https://img.shields.io/badge/Java-21-orange?logo=openjdk&logoColor=white)
![Paper](https://img.shields.io/badge/Paper-1.21.10-blue)
![Maven](https://img.shields.io/badge/Build-Maven-red?logo=apachemaven&logoColor=white)

Built for the [TFMC](https://www.patreon.com/c/TFMCRP) roleplay server. Permanent injuries cannot be treated. Healing ailments such as a broken arm, a broken leg, or a half-blind eye can.

## What it does

A physician offers `/surgery <player>`. The patient accepts, and an inventory operating table opens on that character's worst healing injury (the one with the most time left). Each move uses a surgical instrument from the physician's inventory. Success removes the ailment through RPCharacters. Failure, after the patient has been sedated or cut, adds healing time. Walking away before that point cancels with no penalty.

| | |
|---|---|
| **Real ailments** | The diagnosis is the patient's RPCharacters healing injury, not a random name |
| **Consent** | The patient accepts or denies the offer, which states the ailment and the failure cost |
| **Physicians** | Operating requires `professions.physician` by default |
| **Victorian instruments** | Stethoscope, chloroform, carbolic acid, scalpel, catgut, artery forceps, silver wire, splint, smelling salts, and the rest |
| **One procedure per ailment** | Incisions, bones, and complications live in `config.yml`, keyed by trait id |
| **Complications** | Haemorrhage, shock, and sepsis change bleeding, collapse, and fever |

## How it works

1. `SurgeryCommand` checks permission, distance, and that the patient has a healing injury, then stores an offer.
2. On accept, `SurgeryMenuBuilder` opens the GUI and loads the procedure for that trait id.
3. Tool clicks go through `SurgeryItemHandler`. Instruments resolve through the TLibs item API.
4. `SurgeryMechanicsManager` advances chloroform, fever, bleeding, and the procedure's complications.
5. `SurgeryCompletionHandler` cures the ailment with `HealingInjuries.cure` on success, or `HealingInjuries.extend` on a penalised failure.

```
src/main/java/net/tfminecraft/surgery/
├── SurgeryPlugin.java
├── commands/SurgeryCommand.java
├── listeners/PlayerListener.java
├── managers/          # menu, items, vitals, completion
└── procedures/        # ailment lookup and procedure config
```

## Installation

1. Install **TLibs** and **RPCharacters**, then drop `surgery-<version>.jar` into `plugins/`.
2. Restart the server. Surgery declares a hard dependency on both.
3. Give physicians `professions.physician` (the same permission that crafts the instruments).
4. Point `surgeryItemsConfig.yml` at the surgical items. The defaults are the existing `m.surgery.*` MMOItems ids.

| Dependency | Required |
|---|---|
| Paper 1.21.10 | Yes |
| Java 21 | Yes |
| TLibs | Yes |
| RPCharacters | Yes. Surgery calls `net.tfminecraft.rpcharacters.api.HealingInjuries` |
| MMOItems / ItemsAdder | Optional item and texture sources |

## Usage

| Command | Who | Effect |
|---|---|---|
| `/surgery <player>` | Physician, within 5 blocks | Offer to operate on the patient's worst healing injury |
| `/surgery accept` | Patient | Begin the operation |
| `/surgery deny` | Patient | Decline |

### A procedure

1. Examine with the **stethoscope**. This names the procedure and, for a septic wound, starts the fever.
2. Put the patient under with **chloroform** before cutting. Cutting an awake patient fails the surgery.
3. Clean with **carbolic acid**. Take the temperature with the **clinical thermometer**, then use **willow-bark tincture** if they are feverish.
4. Open with the **scalpel** until the procedure's incision count is met. Bones, if any, are exposed at that point.
5. Bind shattered bone with **silver wire**, then set broken bone with the **splint**.
6. **Sea sponge** clears blood. **Artery forceps** stop bleeding from an open wound. **Transfusion syringe** strengthens the pulse. **Smelling salts** revive a patient who collapsed.
7. Apply the **linen dressing** once the incisions are made and the bones are set.
8. Close with **catgut suture**. **Finish Surgery** succeeds only when the dressing is on, the pulse is strong, the patient is unconscious, the temperature is at or below the success threshold, the site is clean, the incisions are closed, the bones are set, and the patient is not bleeding.

### Shipped procedures

| Trait | Procedure | Notes |
|---|---|---|
| `broken_arm` | Fractured Arm | 2 incisions, 2 broken bones |
| `broken_leg` | Compound Fracture of the Leg | 2 incisions, 2 broken bones, 1 shattered, haemorrhage |
| `half_blind` | Injured Eye | 1 incision, shock and sepsis |
| anything else healing | Injury | 2 incisions, no bones |

A healing trait added later needs a `procedures:` entry only when it should differ from the default.

### Failure

Temperature at or above 110°F, an expired collapse countdown, consecutive extremely weak pulse, consecutive red temperature, cutting while awake, too much chloroform, or closing the menu after the patient was sedated or cut. That last group adds `failure-healing-penalty` (12 hours by default) to the ailment. Closing the menu before then cancels with no penalty.

## Configuration

`config.yml` holds the physician permission, the failure penalty, request timeout, distance, procedures, vitals, and the console commands run on completion (`%surgeon%`, `%player%`, `%ailment%`).

`surgeryItemsConfig.yml` maps each instrument to a TLibs item path. The keys are the Victorian names (`stethoscope`, `chloroform`, `dressing`, …). Unknown keys fall back to the built-in `m.surgery.*` paths, which are unchanged so tools players already crafted still match.

`messages.yml` holds every player-facing string.

## Building from source

```bash
git clone --branch main https://github.com/TF-Minecraft/TLibs.git tlibs
git clone https://github.com/TF-Minecraft/Surgery.git surgery
cd surgery
python3 ../tlibs/tools/install-plugins.py --pom pom.xml --mode pinned
mvn clean verify
```

Use JDK 21. The installer verifies pinned TLibs and RPCharacters releases. Paper API resolves from Maven.

## Author

**Justinas Launikonis** — [GitHub](https://github.com/JustinasLa) · [Support TFMC](https://www.patreon.com/c/TFMCRP)
