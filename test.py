import random
import os
import time

from termcolor import colored

from dungeoncrawl.entities.characters import DummyHero, Party
from dungeoncrawl.bosses import DummyBoss
from dungeoncrawl.controller import DummyGame
from dungeoncrawl.utilities.game_setup import json_to_board

boss = DummyBoss()
tank = DummyHero("Tits McGee", (0,0), "tank", "🛡️")
healer = DummyHero("Dingding", (0,0), "healer", "🔅")
dps1 = DummyHero("Balls McPherson", (0,0), "dps", "🗡️")
dps2 = DummyHero("The Scroat", (0,0), "dps", "☘️")

party = Party(tank, healer, dps1, dps2)

board = json_to_board('C:\\Users\\marau\\Coding\\Python\\pynight\\pydungeoncrawl\\dungeoncrawl\\base_maps\\pathtest.json')

game = DummyGame(board, party, boss, show_board=False)

for turn in game:
    print(game)
    for player in party:
        if player.distance_from(boss) > 1.5:
            if player.last_action_failed:
                random.choice([
                    player.move_up,
                    player.move_down,
                    player.move_left,
                    player.move_right,
                    player.move_up_left,
                    player.move_up_right,
                    player.move_down_left,
                    player.move_down_right
                ])()
            else:
                player.move_toward(boss)
        else:
            player.ball_punch(boss) #type: ignore
    time.sleep(0.1)
    os.system('cls')
if boss.is_alive:
    print(colored("YOU DIED", "red"))
else:
    print(colored("you win!", "green"))