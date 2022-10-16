import arcade

from const import *


class StartView(arcade.View):
    """shown when game is first started"""

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        arcade.set_viewport(0, WIDTH - 1, 0, HEIGHT - 1)

    def on_draw(self):
        """draws text for view"""
        self.clear()
        arcade.draw_text(
            "Space Zombie Survival",
            600,
            HEIGHT - 400,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
        )

        arcade.draw_text(
            "Press Enter to Start",
            WIDTH / 2,
            HEIGHT / 2 - 75,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )

    def on_key_press(self, key, _modifiers):
        """runs when key is pressed"""
        if key == arcade.key.ENTER:

            self.window.show_view(self.window.story_view)
