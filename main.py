import arcade

#window constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "game"

ACCELERATION = 1

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.scene = None
        self.player_sprite = None

        self.accelerating_up = None


    def setup(self):
        self.scene = arcade.Scene()

        self.player_sprite = arcade.Sprite("//dataserver2/CCampbell$/dev/13 game project/assets/zombie_idle.png")
        self.player_sprite.center_x = SCREEN_WIDTH/2
        self.player_sprite.center_y = SCREEN_HEIGHT/2

        self.scene.add_sprite("Player", self.player_sprite)

        self.accelerating_up = False


    def on_draw(self):
        self.clear()
        self.scene.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.accelerating_up = True


    def on_update(self, delta_time):
        self.player_sprite.update()

        if self.accelerating_up == True:
            self.player_sprite.change_y += ACCELERATION

            





def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
