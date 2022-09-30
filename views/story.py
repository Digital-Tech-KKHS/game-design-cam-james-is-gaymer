import arcade

from const import *


class Story(arcade.View):
    """shown when game is first started"""

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        arcade.set_viewport(0, WIDTH - 1, 0, HEIGHT - 1)

    def on_draw(self):
        """draws text for view"""
        self.clear()
        arcade.draw_text(
            "You need:\n-8 copper\n-11 steel\n-6 acid drops\nGOOOOOO! and craft the average screwdriver",
            WIDTH/2,
            500,
            arcade.color.WHITE,
            font_size=25,
            anchor_x="center",
        )

        arcade.draw_text(
            "Press Enter to Continue",
            WIDTH / 2,
            HEIGHT / 2 - 75,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )

    def on_key_press(self, key, _modifiers):
        """runs when key is pressed"""
        if key == arcade.key.ENTER:
            game = self.window.game_view
            game.setup()
            self.window.hide_view()
            self.window.show_view(self.window.game_view)
