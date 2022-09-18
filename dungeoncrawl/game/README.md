# Game Logic Goes Here
This section contains the actual game-running logic and functionality for everything. This might be more useful if it was outside of a subfolder and just in the main area &rarr; `game.py` or something. As it stands, the "game" will be instantiated using something like:

```python
from pydungeoncrawl.game.controller import Controller

...

controller = Controller()
controller.setup()
...
controller.run(player_moves)
```

...which isn't the best way to arrange things. Better would be to do something like:

```python
from pydungeoncrawl.game import Game # i.e. in game.py in the main area of the package
```

Either way, that's more stylistic than actually *functional*, but yeah.

## `Controller`
> **Probably renaming to `Game`**

This is the actual "game" class. This is the thing that's going to be doing all the setup of the board and connecting the `Pawn`s and the `Board`, actually executing all the moves that each `Pawn` makes.

It will also be responsible for feeding back information from the board to the `Pawn` as well; things like incrementing timers on `Effect`s, applying damage, etc. 