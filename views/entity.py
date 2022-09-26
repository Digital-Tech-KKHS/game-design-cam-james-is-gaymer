# import needed things

import random

import arcade
from PIL import Image
from pyglet.math import Vec2

from const import *


class Entity(arcade.Sprite):
    """class for all sprites"""
    def __init__(self, name_file):
        """initializer"""
        main_path = f"assets/{name_file}.png"
        super().__init__(main_path)

    @property
    def pos(self):
        """finds position of sprite"""
        return Vec2(self.center_x, self.center_y)


class Debris(Entity):
    """class for all space debris"""
    def __init__(self, name_file):
        """initializer"""
        super().__init__(name_file)
        # sets any debris to a random size
        self.scale = random.randint(1, 10)





class Rock(Debris):
    """class for meteors"""
    def __init__(self, name_file):
        """initializer"""
        # chooses meteor type
        self.num = random.randint(1, 5)
        super().__init__(f"meteor_{self.num}")
        image = Image.open(f"assets/meteor_{self.num}.png")
        # finds size of image to set mass and health
        rock_width, rock_height = image.size
        self.rock_area = rock_height * rock_width
        self.rock_mass = (self.rock_area * self.scale) * METEOR_MASS
        self.rock_health = (self.rock_area * self.scale) * METEOR_HEALTH_CONSTANT

    def take_damage(self):
        """decreases rock health when """
        self.rock_health -= PLAYER_MINING_LASER_DAMAGE


class Bullet(Entity):
    """class for bulets"""
    def __init__(self):
        """initializer"""
        super().__init__(name_file="bullet")


class Vehicle(Entity):
    """class for ai"""
    def __init__(self, name_file):
        """initializer"""
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
        """updates ai"""
        # updates physics enhine
        physics_engine = self.physics_engines[0]
        self.physics_body = physics_engine.get_physics_object(self).body
        # reduces agular veocity
        self.physics_body.angular_velocity *= 0.7
        if self.forces:
            # applies force on sprite
            self.net = sum(self.forces).clamp(-self.max_force, self.max_force)
            self.physics_body.apply_force_at_world_point(
                self.net, (self.center_x, self.center_y)
            )
            # finds current velocity
            self.vel = Vec2(self.physics_body.velocity.x, self.physics_body.velocity.y)
            # changes angle
            self.physics_body.angle = Vec2(
                self.physics_body.velocity[0], self.physics_body.velocity[1]
            ).heading
        # removes all forces
        self.forces = []
        self.net = 0

    def seek(self, target: Vec2):
        """gos toward target"""
        # finds location that the ai wants to be
        ideal = target - Vec2(self.center_x, self.center_y)
        ideal = ideal.from_magnitude(self.max_speed)
        # applies correct amount of force to get to the target accounting for current speed
        force = ideal - self.vel
        # makes it lower than max force
        force = force.clamp(-self.max_force, self.max_force)
        # adds forces to list
        self.forces.append(force)

    def flee(self, target: Vec2, radius):
        """goes away from target"""
        # checks if too close to target
        if self.pos.distance(target) < radius:
            # finds location that the ai wants to be
            ideal = -(target - self.pos)
            ideal = ideal.from_magnitude(self.max_speed)
            # applies correct amount of force to get to the target accounting for current speed
            force = ideal - self.vel
            # makes it lower than max force
            force = force.clamp(-self.max_force, self.max_force)
            # adds forces to list
            self.forces.append(force)


class Enemy(Vehicle):
    """class for all enemies"""
    def __init__(self, name_file):
        """initializer"""
        super().__init__(name_file)
        # scales enemy
        self.scale = ENEMY_SCALEING


class BasicEnemy(Enemy):
    # class for meelee enemy
    def __init__(self, name_file):
        """initializer"""
        super().__init__("enemy_idle")
