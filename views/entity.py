import arcade

ENEMY_SCALEING = 2
DEBRIS_SCALING = 1


class Entity(arcade.Sprite):
    def __init__(self, name_file):

        main_path = f"assets/{name_file}_idle.png"
        super().__init__(main_path)



class Enemy(Entity):
    def __init__(self, name_file):
        super().__init__(name_file)
        self.scale = ENEMY_SCALEING


class BasicEnemy(Enemy):
    def __init__(self, name_file):
        super().__init__("enemy")

class Debris(Entity):
    def __init__(self, name_file):
        super().__init__(name_file)
        self.scale = DEBRIS_SCALING

class Scrap(Debris):
    def __init__(self, name_file):
        super().__init__(name_file)

class Rock(Debris):
    def __init__(self, name_file):
        super().__init__(name_file)

class Rocket(Scrap):
    def __init__(self, name_file):
        super().__init__("rocket")