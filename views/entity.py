import random
from pyglet.math import Vec2
import math
import arcade
from PIL import Image
from const import *




class Entity(arcade.Sprite):
    def __init__(self, name_file):

        main_path = f"assets/{name_file}.png"
        super().__init__(main_path)





class Debris(Entity):
    def __init__(self, name_file):
        super().__init__(name_file)
        self.scale = random.randint(1, 10)


class Scrap():
    def __init__(self):
        super().__init__()

        self.common = ["assets/drop_1.png", "assets/drop_2.png", "assets/drop_3.png"]
        self.rare = ["assets/drop_4.png"]
        self.legendary = ["assets/drop_5.png"]
        
    def get_drop(self):
        drop_choice = random.random()
        if drop_choice < 0.6:
            return
        if 0.6<= drop_choice > 0.8:
            num = random.randint(0, 2)
            choice = self.common[num]
            return arcade.Sprite(choice)
        elif 0.8 <= drop_choice > 0.95:
            choice = self.rare
            return arcade.Sprite(choice)
        elif 0.95 <= drop_choice >= 1:
            choice = self.legendary
            return arcade.Sprite(choice)
        
        


class Rock(Debris):
    def __init__(self, name_file):

        self.num = random.randint(1, 5)
        super().__init__(f"meteor_{self.num}")
        image = Image.open(f"assets/meteor_{self.num}.png")
        rock_width, rock_height = image.size
        self.rock_area = rock_height * rock_width
        self.rock_mass = (self.rock_area * self.scale) * METEOR_MASS
        self.rock_health = (self.rock_area * self.scale) * METEOR_HEALTH_CONSTANT 
    
    def take_damage(self):
        self.rock_health -= PLAYER_MINING_LASER_DAMAGE



class Bullet(Entity):
    def __init__(self):
        super().__init__(name_file="bullet")

class Vehicle(Entity):
    def __init__(self, name_file):
        super().__init__(name_file)
        self.center_x = random.randint(0, 800)
        self.center_y = random.randint(0, 800)
        self.vel = Vec2()
        self.net = Vec2()
        self.forces = []
        self.max_speed = MAX_SPEED
        self.max_force = 10000
        self.body: arcade.PymunkPhysicsObject = None

    def update(self):
        physics_engine = self.physics_engines[0]
        self.physics_body = physics_engine.get_physics_object(self).body
        self.physics_body.angular_velocity *= 0.7
        if self.forces:
            self.net = sum(self.forces).clamp(-self.max_force, self.max_force)
            self.physics_body.apply_force_at_world_point(
                self.net, (self.center_x, self.center_y)
            )
            self.vel = Vec2(self.physics_body.velocity.x, self.physics_body.velocity.y)
            self.physics_body.angle = (
                Vec2(self.physics_body.velocity[0], self.physics_body.velocity[1]).heading
            )

        self.forces = []
        self.net = 0

    def seek(self, target: Vec2):
        ideal = target - Vec2(self.center_x, self.center_y)
        ideal = ideal.from_magnitude(self.max_speed)
        force = ideal - self.vel
        force = force.clamp(-self.max_force, self.max_force)
        self.forces.append(force)

    def flee(self, target: Vec2, radius):
        if self.pos.distance(target) < radius:
            ideal = -(target - self.pos)
            ideal = ideal.from_magnitude(self.max_speed)
            force = ideal - self.vel
            force = force.clamp(-self.max_force, self.max_force)
            self.forces.append(force)

    @property
    def pos(self):
        return Vec2(self.center_x, self.center_y)


class Enemy(Vehicle):
    def __init__(self, name_file):
        super().__init__(name_file)
        self.scale = ENEMY_SCALEING


class BasicEnemy(Enemy):
    def __init__(self, name_file):
        super().__init__("enemy_idle")
