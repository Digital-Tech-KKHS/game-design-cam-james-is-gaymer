import arcade

from const import *


class Controls(arcade.View):
    """shown when game is first started"""

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        arcade.set_viewport(0, WIDTH - 1, 0, HEIGHT - 1)

    def on_draw(self):
        """draws text for view"""
        self.clear()
        arcade.draw_text(
            "W = Move UP",
            WIDTH / 2,
            HEIGHT - 100,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
        )
        arcade.draw_text(
            "S = Move DOWN",
            WIDTH / 2,
            HEIGHT - 200,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
        )
        arcade.draw_text(
            "A = Move LEFT",
            WIDTH / 2,
            HEIGHT - 300,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
        )
        arcade.draw_text(
            "D = Move RIGHT",
            WIDTH / 2,
            HEIGHT - 400,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
        )
        arcade.draw_text(
            "1 = Bombardment Bullet",
            WIDTH / 2,
            HEIGHT - 500,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
        )
        arcade.draw_text(
            "2 = Mining Laser",
            WIDTH / 2,
            HEIGHT - 600,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
        )
        arcade.draw_text(
            "RIGHT CLICK = Fire Weapon",
            WIDTH / 2,
            HEIGHT - 700,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
        )

        arcade.draw_text(
            "Press Left SHIFT to return to pause",
            WIDTH / 2,
            HEIGHT / 2 - 780,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )

    def on_key_press(self, key, _modifiers):
        """runs when key is pressed"""
        if key == arcade.key.LSHIFT:
            # self.window.show_view(self.window.story_view)

            self.window.show_view(self.window.pause_view)
