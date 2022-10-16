import math
import random

import arcade
from PIL import Image
from pyglet.math import Vec2

from const import *


class Entity(arcade.Sprite):
    def __init__(self, name_file):

        main_path = f"assets/{name_file}.png"
        super().__init__(main_path)
        self.cur_texture = 0

    @property
    def pos(self):
        return Vec2(self.center_x, self.center_y)


class Debris(Entity):
    def __init__(self, name_file):
        super().__init__(name_file)
        self.scale = random.randint(1, 10)


class Scrap:
    def __init__(self):
        super().__init__()
        pass


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
        self.max_speed = ENEMY_MAX_SPEED
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
            self.physics_body.angle = Vec2(
                self.physics_body.velocity[0], self.physics_body.velocity[1]
            ).heading

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


class Enemy(Vehicle):
    def __init__(self, name_file):
        super().__init__(name_file)
        self.scale = ENEMY_SCALEING
        self.enemy_texures = []
        self.odo = 0
        # loads animation
        for i in range(4):
            self.enemy_texures.append(
                arcade.load_texture(f"assets/{name_file}{i + 1}.png")
            )

    def update_animation(self, delta_time: float = 1 / 60):
        self.odo += 1
        if self.odo < 10:
            return

        self.odo = 0
        self.cur_texture += 1
        if self.cur_texture > 3:
            self.cur_texture = 0
        self.texture = self.enemy_texures[self.cur_texture]


class BasicEnemy(Enemy):
    def __init__(self, name_file):
        super().__init__("enemy")
