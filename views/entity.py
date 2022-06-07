import random

import arcade
from PIL import Image

# from views.game_view import METEOR_MASS

ENEMY_SCALEING = 2


class Entity(arcade.Sprite):
    def __init__(self, name_file):

        main_path = f"assets/{name_file}.png"
        super().__init__(main_path)


class Enemy(Entity):
    def __init__(self, name_file):
        super().__init__(name_file)
        self.scale = ENEMY_SCALEING


class BasicEnemy(Enemy):
    def __init__(self, name_file):
        super().__init__("enemy_idle")


class Debris(Entity):
    def __init__(self, name_file):
        super().__init__(name_file)
        self.scale = random.randint(1, 10)


class Scrap(Debris):
    def __init__(self, name_file):
        super().__init__(name_file)


class Rock(Debris):
    def __init__(self, name_file):

        self.num = random.randint(1, 5)
        super().__init__(f"meteor_{self.num}")

    def meteor_mass(self, mass_constant):
        """takes mass constant given from main game
        calculates image size by using PIL(via pixel amount)
        finds area of image
        calculates sprite mass and returns to main game"""

        image = Image.open(f"assets/meteor_{self.num}.png")
        rock_width, rock_height = image.size
        self.rock_area = rock_height * rock_width
        self.rock_mass = self.rock_area * mass_constant
        return self.rock_mass

    def meteor_speed(self, max_speed, min_speed):
        """brings max and min values from game view then calculates
        the speed of x and y axis then puts it in a tuple and
        returns to main game to be implemented"""

        speed_x = random.uniform(min_speed, max_speed)
        speed_y = random.uniform(min_speed, max_speed)
        speed_vec = (speed_x, speed_y)
        return speed_vec
