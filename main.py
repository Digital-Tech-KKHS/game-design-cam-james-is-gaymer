# import needed things
import arcade

from const import *
from views.controls import Controls
from views.death import Death
from views.game_view import TestGame
from views.inventory import InventoryView
from views.pause import Pause
from views.start import StartView
from views.story import Story
from views.win import Win


class GameWindow(arcade.Window):
    """creates window for game to be run from"""

    def __init__(self, width, height, title):
        """initializer"""
        super().__init__(width, height, title)

        # creates views
        self.game_view = TestGame()
        self.start_view = StartView()
        self.story_view = Story()
        self.win_view = Win()
        self.death_view = Death()
        self.pause_view = Pause()
        self.controls_view = Controls()
        self.inventory = InventoryView()

        # not needed
        self.screwdriver = False

        # creates a sprite list to hold resources in inventory
        self.resources = arcade.SpriteList()
        self.show_view(self.start_view)


# runs game
window = GameWindow(WIDTH, HEIGHT, TITLE)
arcade.run()
