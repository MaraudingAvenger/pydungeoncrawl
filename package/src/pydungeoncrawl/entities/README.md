# Base classes
This section contains most of the base classes for things, although it contains a couple of implementations too.

## `items.py`
Contains base classes for `Weapon`s and `Wearable`s (both inherit from `Equipment`), and `Loot`. This doesn't contain any actual implementations of any of these things; it's just supposed to be representative of the different types of interactable non-sentient things that players will have/use/acquire.

## `effects.py`
Contains the base class `Effect` and several example implementations that can affect grid squares (`Burning`, `Freezing`), spell effects for pawns (`Haste`, `Bless`), and example weapon effects (`Curse`, `Fire`). These aren't set in stone by any means, and should just be used as examples. 
* I've consolidated damage-related stuff into 3 types:  
  * **damage_over_time** deals damage (or negative damage, a.k.a. *healing-over-time*) to the entity that has that effect...over time.  
  * **bonus_damage_output** increases or decreases the damage that the effect-bearer... outputs.  
  * **bonus_damage_received** increases or decreases the damage that the effect-bearer... receives from other sources.  

  The other attributes for that are bonus movement and bonus max health

* *(old notes on effects.py):*
  * *I think `change_damage_dealt` should probably be consolidated into `damage`. The previous thought was to have two categories of attribute -- damage to self and damage to others, like, damage that's dealt to the wielder and damage that's dealt to other things when the wielder has this effect... it's probably too complicated the way that it is.*
  * *It might work better to have a dict with a "self" side and "others" side or something? idk.*

## `armor.py` and `weapons.py`
Contain implementations of `entities.items.Weapon` and `entities.items.Wearable`. They're not set in stone by any means, but I figure we can fill these up with some implementations of things and use them in loot generators and such. There's a `FireSword` class that implements a weapon effect as well -- we might want to generalize it into something like a "MagicWeapon" that has an effect slot.

## `stats.py`
Contains the `Stat` class and the `Stats` class. `Stat` is a general implementation of some kind of stat, that's roll-able and set-able and has a modifier, DnD style. i.e. a 20 in a stat will give a +5 to checks that use that stat. This could be too much. I don't know, it's done and it wasn't complex or anything to implement, so we might as well use it.

`Stats` is a collection of `Stat`s. It's got convenience methods to access each individual stat and to access them as a group. Right now it's arranged into (again) DnD-like configuration (strength, dexterity, constitution, wisdom, intelligence, charisma), but it doesn't have to be at all. We can change it to be something like `attack`, `defense`, `magic`, `fart_potency` -- i.e. whatever we want; this is just an implementation to show how it all works.

## `pawn.py`
Contains the `Pawn` base class that should probably be converted to an `ABC` with `@abstract_method`s that `Character` and `Monster` implement. I'll figure it out.
* I implemented a bunch of things to do with movement and calculating distances to things. I figure the base class should have all of this functionality. This is all implemented for Pawn things, but I haven't made any kind of `Terrain` class, which we might need to do. Not sure.

# Upcoming
* `Terrain` class? `MapFeature` class? Something like that. Kind of like a pawn but doesn't have all the movement related things or distance calculations......... might just refactor pawn to take a base class of Entity, and then have them both inherit from that. Not sure how to proceed -- this is starting to sound a LOT like how Unreal Engine names things lol.
* probably `character.py` to go with `monster.py` and implement the player version of a pawn
* ...not sure what else!
