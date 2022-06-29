import arcade

from const import *
from views.game_view import TestGame
from views.inventory import InventoryView

class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.game_view = TestGame()
        self.inventory = InventoryView()

window = GameWindow(WIDTH, HEIGHT, TITLE)
window.show_view(window.game_view)
arcade.run()
