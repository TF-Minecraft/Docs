# Model bones

Vehicles are ModelEngine models. The plugin moves specific bones itself, so those bones must not be animated in Blockbench. Looping clips such as a spinning propeller or a moving track should be set to loop.

Bone names in the model and in the vehicle YAML have to match. A skin can use a different `.bbmodel`, but every bone the config names has to exist on that model too.

## Body

**Controller bone.** This is `behaviour.rotator` (often `body_controller`). Put it outside the main body bone, and do not parent the hitbox bone under it. The plugin rotates this bone. Its pivot is the point the model turns around, so place it at the center of the vehicle.

**Movement vector.** `behaviour.vector` is two bones written as `first.second`, for example `move.movealign`. The direction from the first bone to the second is forward. Offset the second bone ahead of the first. If they share a position, the vector is zero and the vehicle will not move. Parent them under the body if forward should follow the model's animation. Parent them under the controller if it should not.

**Seats.** ModelEngine treats a bone whose name starts with `p_` as a passenger seat. The name inside the seat entry must be that bone's name. `captain(p_captain)` matches a bone named `p_captain`. The shipped configs use the same short name in both places (`captain(captain)`), which works when the mount bone is named `captain`.

The seat menu has 27 slots, and two of them are reserved, so a vehicle cannot usefully define a full inventory of seats.

## Weapons

A weapon that aims needs three pairs of bones:

- `body-bone` yaws left and right. Its pivot is the yaw pivot.
- `head-bone` pitches up and down. Its pivot is the pitch pivot. `head-axis` is `x` unless the pitch axis on the model is different.
- Each entry in `bones` is a vector, `exit.exitalign`. The shot leaves along that direction. Each vector is loaded separately, so two vectors consume two rounds and fire in turn.

Do not animate the controller or rotator bones.

A `fixed: true` weapon does not use body and head bones. Fixed vehicles such as an emplaced gun still need a `behaviour.rotator`. Point the movement vector at the same bone twice (`weapon_body.weapon_body`) when the vehicle should not drive.

## Trains and tow points

`behaviour.train.front-connector` and `back-connector` are bones at the couplers. The distance between a car's coupler and the next car's coupler is the spacing along the track.

`towing.bone` is the hitch bone on the vehicle that pulls.

## Effects

`vfx` on a component is a list of bones that show fire and smoke when that component is damaged. Engine `particle-bones` is where engine particles spawn. Weapon `bones` are also where muzzle particles spawn.
