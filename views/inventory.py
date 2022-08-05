import arcade
from pyglet.math import Vec2
from const import *


class InventoryView(arcade.View):
    def __init__(self, window: arcade.Window = None):
        super().__init__(window)

        self.inventory_grid = None
        self.camera = arcade.Camera()

    def on_show(self):
        self.inventory_grid = arcade.Sprite("assets\inventory_grid.png", 5)
        self.inventory_grid.center_x = WIDTH / 2
        self.inventory_grid.center_y = HEIGHT / 2

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.inventory_grid.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.E:
            self.window.show_view(self.window.game_view)
