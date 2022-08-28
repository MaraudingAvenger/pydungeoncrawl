# pydungeoncrawl
A python package to run a dungeon crawl with appropriate classes and structure

## Overall design
The game will be played on one machine by one or a group of players. The objective is to come up with a series of moves that will bring the `Monster` down to zero HP in the most efficient way possible. Players program their characters' moves in a sequence that is then executed in turns against the `Monster`'s moves sequence.

---

## Game
The game begins by instantiating a `Game` object. 
* the game object will have some kind of setup function that creates a `Board` and a `Party` of adventurer pawns(?)
  * the setup function can take some kind of code/string/command to generate all the necessary things in some kind of pre-programmed way

### Game Board
The `Board` is (logically, although maybe not graphically) a 2d grid that contains valid and invalid move spaces (surrounded by lava that will damage the players if they move outside the bounds of the board)
* &#9989; The board will have some kind of representation (unicode string, tiled SVG on a site, etc.)
* &#9989; grid tiles can be of various types
* &#9989; grid tiles can be impassable (river, lava floe, wall, barbed wire, moat, etc.)
* grid tiles can impart effects on things that stand on them or pass over them (`Character` and `Monster`) (fire tiles set pawns on fire, poison tiles, etc.) ?
* grid tiles can be searchable/observable?
* grid tiles can be destructible? (destroy bridge tile, monster falls into lava/pit/spikes/etc.; useful for a monster that will charge the party)

---

## Pawn
The class from which we derive both `Character`s and `Monster`s. This is a class that represents a game piece that moves around the board and interacts with it.  
**Pawns have:**
* &#9989; a name
* &#9989; hit points
* &#9989; equipment
* &#9989; inventories
* &#9989; vital stats (str|dex|con|wis|int|chr for example that could affect abilities)


### Monster
Inherits from `Pawn`, has predefined stats, equipment, a prebuilt moves sequence *OR* a decision tree that defines its behavior
i.e. 
```python
if self.hp > (self.hp_max/2): # if more than half HP
    #move toward nearest player and attack
else:
    # use healing item
```

### Character
Inherits from `Pawn`
* Has experience points (?)
* Has mana/MP (?)

#### Character Subclasses
All inherit from `Character`. One of the following: `Ranger`, `Healer`, `Fighter`, `Mage` (?), `Monk` (?) 

#### Ranger
Ranged specialist, comes with a bow and a dagger.
* Has a hide/sneak ability(?)
* Has a backstab ability/passive bonus when attacking from the rear(?)

#### Fighter
Melee specialist, comes with a sword and shield.
* Has a power attack ability(?)
* Has a warcry/tank/aggro ability(?)

#### Healer
Healing and buff/debuff specialist, comes with a robe and a wizard hat.
* Single/group heals (?)
* Has a bless that gives +1 to damage (?)
* Has a curse/smite that deals damage, double against undead (?)
* Can cast pleasure level 9000 (see robe and wizard hat reference)

#### Mage
Glass cannon, damage dealer + status effect specialist, comes with staff/wand and spell book.
* Can apply damage + combat effect with spells (?)
  * Fireball &rarr; burning/damage over time
  * Lightning bolt &rarr; shock/stun
  * Ray of Frost &rarr; freezing/slow
  * Earthquake/Liquify Earth/Root &rarr; root/crushing dmg
* very low HP

---

# Things to discuss
* What happens when a character reaches zero HP? (dead or KO/can revive)
* How are moved *made* &rarr; designed by the player, or part of the class, put together in different combinations?
  * I strongly vote for prebuilt, and players combine them in different ways (see conditional stuff below)
* How are moves queued?
  * I think they should be like nested lists or dicts that get pushed into the `Game` or `Board` class, like:
    ```python
    [
        {Monster: [conditional_move, attack, conditional_move, attack, ...]},
        {Fighter: [conditional_move, block, attack, block, attack, block...]},
        {Ranger: [conditional_move, hide, shoot, conditional_move, hide...]},
        {Healer: [conditional_move, conditional_heal, conditional_move, ...]}
        {Mage: [liquify_earth,conditional_move,fireball,lightning_bolt, ...]}
    ]
    ```
  * Actions can be executed one at a time from each pawn inside the action queue. We can do gamey things here like "rolling initiative" to goof up the turn order and make them react to it, or make the monster go first every time, have a well defined turn order, OR if we want to make it like Gloomhaven, which could be pretty rad, we can give each ability a speed value, and have turns execute in speed-order (fast attack vs. power attack vs. quick step vs. long move, etc.)
  * Conditional actions bring a whole new level of programming to it, I like the idea of something like conditional_move, conditional_attack, conditional_ability -- we can limit the alternatives if we want to strategify this a bit.