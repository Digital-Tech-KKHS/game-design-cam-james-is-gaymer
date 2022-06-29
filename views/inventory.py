import arcade


class InventoryView(arcade.View):
    def __init__(self, window: arcade.Window = None):
        super().__init__(window)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_filled(0,0,200,200,arcade.color.WHITE)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.E:
            self.window.show_view(self.window.game_view)