import arcade

from views.game_view import TestGame

WIDTH = 1600
HEIGHT = 800
TITLE = "test"


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.game_view = TestGame()


window = GameWindow(WIDTH, HEIGHT, TITLE)
window.show_view(window.game_view)
arcade.run()
