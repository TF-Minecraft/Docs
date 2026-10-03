# CompanionPets gameplay

[CompanionPets](../README.md) · [All projects](../../../README.md)

CompanionPets keeps one record per pet: name, sex, personality, needs, bond,
tricks, and a rolled favourite toy. The Minecraft entity is only the body that
is currently in the world.

## Hatching and shelters

- Use a configured egg, name the pet in chat, and confirm. The egg is spent
  only after the name is confirmed and there is room in the outside quota.
- Sneak and right-click with a barrel to place a shelter. Right-click it to
  open the list. Click a pet to open its sheet, the same one as
  sneak-right-clicking it in the world. From the sheet you bring it out, call
  it, store it, let it go, or look up the tricks it has learned.
- Several pets can be outside at once.

Plugin replies and egg, rename and release dialogue inputs are private. Ordinary
spoken pet orders remain roleplay chat.

## Care

- Sneak and right-click the pet with an empty hand for its info screen. A
  plain right-click checks on the pet: it tells you what is wrong, or you pet
  it when it is fine. If the owner is far away or offline, it whines that it
  misses them.
- Food, a brush, and medicine act immediately. Anyone nearby can feed, clean,
  and heal. Play and tricks belong to the owner. Food past a full stomach makes
  the pet feel worse. A hit makes it yelp and flinch.
- Pets only sit through the trained Sit trick. A worn-out pet lies down on its
  own when exhausted, and the learned Lay trick puts it to rest sooner.

Needs stay still in the shelter and while the owner is offline. Outside, they
fall at the normal rate when the owner is nearby and at the away rate when the
owner is online but far.

Sitting, lying from weakness or exhaustion, and sleeping all recover energy at
the `care.sleep-minutes-to-full` rate, without idle energy loss. Away recovery
uses the same away rate; frozen presence pauses it. Standing still with Stay
does not count as rest. Only sleeping reduces hunger decay, through
`care.sleeping-hunger-multiplier`. Automatic exhaustion sleep ends at full
energy; an explicit Lay order continues until another order changes it.

## Training and orders

- Teach a trick by holding any accepted treat, looking at the pet, and saying
  the whole chat line. Use the learned word while looking at the pet, or say
  `<name> <word>` / `<word> <name>` without aiming. Names and command words may
  contain spaces. Only your own loaded pets in the same world and within
  `orders.hearing-radius` (12 blocks) hear named orders. Duplicate names require
  aiming to choose the intended pet. Jump makes a sitting pet stand first.
- Follow is one trick, learned at 100% by default and shown with its command
  words on the Tricks page. Say `follow` while looking or `<name> follow`.
  Come is a separate trick; saved Come words and progress stay with Come.
  Existing custom word bindings are never overwritten.
- Sit, Stay (standing) and Lay (sleeping) remain in place until following is
  resumed, and survive restarts. Lay stays asleep even at full energy. Automatic
  exhaustion sleep can still end when recovered. Needs and illness can prevent a
  pet from moving even after release.

Follow is continuous following. Come gets the pet up, walks to the owner's
current position and restores its earlier Sit, Stay or Lay posture on arrival.
From Follow it resumes following. Repeating Come during the trip preserves the
original posture; a new Follow, Sit, Stay or Lay order cancels the pending
return. Timeout or disconnection restores the posture at the pet's current
position; normal reload or shutdown also restores pending holds.

Name calls own the native MOVE goal and refresh the destination from the owner's
current position. Sit, Stay and Lay cancel the call and clear both pathfinding
and native travel inputs immediately, preserving vertical physics. Their holds
also apply during model animations, so a posture cannot slide along an old
movement route. Stay uses the standing idle pose, independently of stale
vanilla sitting flags. Native entity teleports are cancelled while a pet has a
hold order, including the tameable mob's built-in teleport to its owner. Follow
and temporary Come movement remain permitted; an explicit profile Call switches
to Follow before teleporting.

Which tricks each type can learn, the default tricks and custom tricks are set in
the [configuration guide](configuration.md#learnable-tricks-per-pet-type).

## Play and social behaviour

- Right-click the air with a listed toy to throw it. The summoned pet fetches
  that item and drops it in front of the owner.
- Say a following pet's exact name in chat to call it close. It then waits
  quietly for `roaming.name-attention-seconds` (10 seconds), counted after
  arrival. Calling a pet that is already sitting, staying or sleeping does not
  cancel that order.
- When its owner stands still, a following pet explores nearby and alternates
  between looking at its owner, nearby players, and other pets.
- Pets occasionally dig up a gift for their owner. The possible items and their
  weights are in `moments.dig-loot`. Random moments and the operator preview
  commands require the pet to be awake and following.
- Nearby pets approach to sniff and play chase. Two territorial pets may bark
  repeatedly at each other, but the plugin never makes pets attack each other.
  Right-click a barking pet three times with an empty hand to calm it. Each
  vanilla species keeps its own hunting and combat behaviour. A vanilla animal
  targeting a player can also be calmed with repeated right-clicks.

## Belly rub moment

Owner petting with an empty hand can trigger `lie_back` → `belly_up` → `get_up`
on modelled pets that have all three clips. Vanilla pets and incomplete models
keep their normal petting interaction. The chance, idle time, cooldown and
minimum mood are [configured](configuration.md#belly-rub-moment) under
`moments.belly-up`.

The pet must be healthy with no low needs, hunger ≥ 60, energy ≥ 40, health ≥ 70
and the configured mood. The owner must be within six blocks. Training, combat,
fetching and active play prevent it. While belly-up, owner right-clicks scratch
its belly and restart the idle timer. Rewards retain their usual cooldown.
Navigation pauses through the transitions, then the pet resumes its previous
order. Damage, water, orders, illness, leaving or storage interrupt the moment.

## Menus

Trick menus show learned tricks, then tricks in practice, then unknown tricks.
Within each group the order is Follow, Come, Sit, Stay, Lay, Paw, Speak, Beg,
Jump, followed by custom tricks in configuration order. Trick inventories have
three rows, with 18 entries per page from slot 0. All nine slots in the third
row are reserved for navigation; the nineteenth trick starts on the next page.
Follow is available as a learned trick rather than a separate profile button.
The Tricks button occupies the middle of the profile's bottom row. Sex uses
white dye for both sexes, with neutral text and no sex symbols.

Pet lists hold 45 entries per page and fill rows from left to right, top to
bottom, sorted by name with a stable identity tie-breaker. The footer is
reserved for navigation. An arrow always occupies the bottom right corner, with
the page counter in its title (1/1, 1/2, and so on). Left-click opens the next
non-empty page; right-click opens the previous page. Both gestures are explained
on the arrow. At either boundary it plays a private denial sound and keeps the
same inventory. Empty slots use light grey glass.

Back uses an item frame in the bottom left corner and always returns to the
parent menu, independently of the current page. Pet lists and the shelter have
no Back button. Profiles opened directly from the animal have no Back button;
profiles reached from the shelter return there, and keep that parent when
browsing their tricks.
