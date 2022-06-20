import random
from pyglet.math import Vec2
import math
import arcade
from PIL import Image



ENEMY_SCALEING = 2

MAX_SPEED = 100


class Entity(arcade.Sprite):
    def __init__(self, name_file):

        main_path = f"assets/{name_file}.png"
        super().__init__(main_path)





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
        self.net = sum(self.forces).clamp(-self.max_force, self.max_force)
        self.physics_body.apply_force_at_world_point(
            self.net, (self.center_x, self.center_y)
        )
        vel = Vec2(self.physics_body.velocity.x, self.physics_body.velocity.y)
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