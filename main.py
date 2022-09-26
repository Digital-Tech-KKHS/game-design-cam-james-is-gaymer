import arcade

from const import *
from views.game_view import TestGame
from views.start import StartView
from views.story import Story
from views.win import Win
from views.death import Death
from views.controls import Controls
from views.pause import Pause
from game_play.inventory import InventoryView


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.game_view = TestGame()
        self.start_view = StartView()
        self.story_view = Story()
        self.win_view = Win()
        self.death_view = Death()
        self.pause_view = Pause()
        self.controls_view = Controls()
        self.inventory = InventoryView()

        self.screwdriver = False

        self.resources = arcade.SpriteList()


window = GameWindow(WIDTH, HEIGHT, TITLE)
window.show_view(window.game_view)
arcade.run()
