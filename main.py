# import needed things
import arcade

from const import *
from views.game_view import TestGame
from views.inventory import InventoryView


class GameWindow(arcade.Window):
    """creates window for game to be run from"""

    def __init__(self, width, height, title):
        """initializer"""
        super().__init__(width, height, title)

        # creates views
        self.game_view = TestGame()
        self.inventory = InventoryView()

        # not needed
        self.screwdriver = False

        # creates a sprite list to hold resources in inventory
        self.resources = arcade.SpriteList()


# runs game
window = GameWindow(WIDTH, HEIGHT, TITLE)
window.show_view(window.game_view)
arcade.run()
