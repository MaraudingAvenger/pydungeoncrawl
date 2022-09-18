# Board game board
This section will contain all the logic for a working game board. Board shouldn't do anything with `Pawn`s or `Equipment` -- it should only be the decoupled play space. Putting the two sides together (entities and the board) will be the job of the `game.controller.Controller` which will also instantiate the `Board` object as well. 

## stuff and things
* This is default a square
  * I'm okay with it staying that way
* This needs to have a default "terrain" configuration
* This needs to be able to accept an optional configuration and poop out a configured board from it
  * Maybe a config string? b64 encoded thing? not sure what the input will look like, but I want it to work like megaman.
* I really want to implement something with wave function collapse to generate "terrain"
* Possibilities are endless here. The implementation is super basic right now with just a `Square` and a `Board` class. I might separate these into their own files just for overall readability and ease of access
