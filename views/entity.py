from re import X
import arcade
import random

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
        self.scale = random.randint(1,10)

class Scrap(Debris):
    def __init__(self, name_file):
        super().__init__(name_file)

class Rock(Debris):
    def __init__(self, name_file):
        num = random.randint(1,5)
        print(num)
        super().__init__(f"meteor_{num}")
    
