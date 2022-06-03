import random
import PIL
import arcade

from views.game_view import METEOR_MASS

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
        num = random.randint(1, 5)
        super().__init__(f"meteor_{num}")

        image = PIL.Image.open(f"assets/meteor_{num}.png")

        rock_width, rock_height = image.size
        self.rock_area = rock_height * rock_width
        self.mass = self.rock_area * METEOR_MASS
