import arcade

class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()

        main_path = "assets/player_idle.png"
        self.idle_image = arcade.load_texture_pair(main_path)

        self.accelerating_up = None
        self.accelerating_down = None
        self.accelerating_left = None
        self.accelerating_right = None

        self.physics_engine = None

        #self.setup()
    
    #def setup(self):
      
        #self.accelerating_up = False
        #self.accelerating_down = False
        #self.accelerating_left = False
        #self.accelerating_right = False