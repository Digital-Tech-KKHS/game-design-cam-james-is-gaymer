from tkinter import Y
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
        self.button_refresh()



    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.inventory_grid.draw()
        self.manager.draw()
        self.window.resources.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.E:
            self.window.show_view(self.window.game_view)

        if symbol == arcade.key.Q:
            print(self.window._mouse_x)
            print(self.window._mouse_y)

    def on_click_resource(self, event):
        self.window.resources.remove(event.source.resource)
        event.source.resource.center_x = self.window.game_view.player_sprite.center_x + 50
        event.source.resource.center_y = self.window.game_view.player_sprite.center_y + 50
        self.window.game_view.scene["scrap"].append(event.source.resource)
        
        
        self.button_refresh()


    def button_refresh(self):
        self.manager = arcade.gui.UIManager()
        self.manager.enable()


        self.inventory_grid = arcade.Sprite("assets\inventory_grid.png", 5)
        self.inventory_grid.center_x = WIDTH/2
        self.inventory_grid.center_y = HEIGHT/2

        for i, resource in enumerate(self.window.resources):
            x = 740 + 85 * (i % 5)
            y = 635 - 85 * (i // 5)
            print(i)
            item_button = arcade.gui.UITextureButton(x, y, 16*5, 16*5, arcade.load_texture(resource.main_path), scale= 5)
            self.manager.add(item_button)

            item_button.on_click = self.on_click_resource
            item_button.resource = resource

