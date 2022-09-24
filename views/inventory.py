# import needed things
from msilib.schema import UIText
from tkinter import Y

import arcade
import arcade.gui
from pyglet.math import Vec2

from const import *

from .collectables import Acid, ScrapCopper, ScrapSteel


class InventoryView(arcade.View):
    """inventory and crafting"""
    def __init__(self, window: arcade.Window = None):
        """initializer"""
        super().__init__(window)

        self.inventory_grid = None
        self.camera = arcade.Camera()

    def on_show(self):
        """runs when the inventory is open"""
        self.button_refresh()

    def on_draw(self):
        """draws inventory"""
        arcade.start_render()
        self.camera.use()
        self.inventory_grid.draw()
        self.manager.draw()
        self.window.resources.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        """runs key binds for inventory"""
        # exit inventory
        if symbol == arcade.key.E:
            self.window.show_view(self.window.game_view)

    def on_click_resource(self, event):
        """removes an item when it is clicked"""
        # removes the resource from stored inventory
        self.window.resources.remove(event.source.resource)
        
        # adds it back to the game
        event.source.resource.center_x = (
            self.window.game_view.player_sprite.center_x + 50
        )
        event.source.resource.center_y = (
            self.window.game_view.player_sprite.center_y + 50
        )
        self.window.game_view.scene["scrap"].append(event.source.resource)

        self.button_refresh()

    def on_click_screwdriver(self, event):
        """sees if the game can be won"""
        steel = 0
        copper = 0
        acid = 0
        # change it pls
        if self.window.screwdriver == False:
            # checks how many of each resource is in inventory
            for resource in self.window.resources:
                print(resource)
                if isinstance(resource, ScrapSteel):
                    steel += 1
                if isinstance(resource, ScrapCopper):
                    copper += 1
                if isinstance(resource, Acid):
                    acid += 1
            # if the player has enough resources than they win game
            if steel >= 11 and copper >= 8 and acid >= 6:
                print("win")
            else:
                print("no")

    def button_refresh(self):
        """creates the inventory grid with all resources and the win game button"""
        # creates manager to use GUI
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # creates the grid
        self.inventory_grid = arcade.Sprite("assets\inventory_grid.png", 5)
        self.inventory_grid.center_x = 250
        self.inventory_grid.center_y = 750

        # places resources in apropriate grid spots
        for i, resource in enumerate(self.window.resources):
            # location of resource
            x = self.inventory_grid.center_x - 210 + 85 * (i % 5)
            y = self.inventory_grid.center_y + 135 - 85 * (i // 5)
            print(i)

            # creates resource buttons with functions
            item_button = arcade.gui.UITextureButton(
                x, y, 16 * 5, 16 * 5, arcade.load_texture(resource.main_path), scale=5
            )
            self.manager.add(item_button)
            item_button.on_click = self.on_click_resource
            item_button.resource = resource

        # creates win buttons with functions
        screwdriver_button = arcade.gui.UITextureButton(
            600,
            800,
            16 * 5,
            16 * 5,
            arcade.load_texture("./assets/screwdriver.png"),
            scale=5,
        )
        self.manager.add(screwdriver_button)

        screwdriver_button.on_click = self.on_click_screwdriver
