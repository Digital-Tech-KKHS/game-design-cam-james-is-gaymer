import arcade
from pyglet.math import Vec2
from const import *
import arcade.gui

class InventoryView(arcade.View):
    def __init__(self, window: arcade.Window = None):
        super().__init__(window)

        self.inventory_grid = None
        self.camera = arcade.Camera()
    
    def on_show(self):
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.layout = arcade.gui.UIBoxLayout()

        self.inventory_grid = arcade.Sprite("assets\inventory_grid.png", 5)
        self.inventory_grid.center_x = WIDTH/2
        self.inventory_grid.center_y = HEIGHT/2

        for i, resource in enumerate(self.window.resources):
            resource.center_x = 200 + 50 * (i % 4)
            resource.center_y = 200 + 50 * (i // 4)
        

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.inventory_grid.draw()
        self.manager.draw()
        self.window.resources.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.E:
            self.window.show_view(self.window.game_view)