import arcade

SCALEING = 2


class Entity(arcade.Sprite):
    def __init__(self, name_file):

        main_path = f"assets/{name_file}_idle.png"
        super().__init__(main_path)
        self.scale = SCALEING


class Enemy(Entity):
    def __init__(self, name_file):
        super().__init__(name_file)


class BasicEnemy(Enemy):
    def __init__(self, name_file):
        super().__init__("enemy")
