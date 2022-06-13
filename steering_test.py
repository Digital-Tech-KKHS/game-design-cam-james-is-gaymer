import math
import random

import arcade
from pyglet.math import Vec2

PLAYER_ACCELERATION = 6000
PLAYER_DEACCELERATION = 0.02
PLAYER_MASS = 20
PLAYER_FRICTION = 0.2
PLAYER_MAX_SPEED = 10000
PLAYER_DAMPNING = 0.58

DEFAULT_DAMPNING = 1.0

class Vehicle(arcade.Sprite):
    def __init__(self, pos):
        super().__init__(":resources:images/space_shooter/playerShip1_orange.png", 0.3)
        #self.pos = Vec2(random.randint(0, 800), random.randint(0, 800))
        self.center_x = random.randint(0, 800)
        self.center_y = random.randint(0, 800)
        self.vel = Vec2()
        self.acc = Vec2()
        self.forces = []
        self.max_speed = 200
        self.max_force = 100
        self.body: arcade.PymunkPhysicsObject = None

    def update(self):
        self.acc = sum(self.forces).clamp(-self.max_force, self.max_force)
        self.body.apply_force_at_world_point(self.acc, (self.center_x,self.center_y))
        vel = Vec2(self.body.velocity.x)
        self.body.angle = 
        # self.vel += self.acc
        # self.vel = self.vel.clamp(-self.max_speed, self.max_speed)
        # self.pos += self.vel
        self.forces = []
        self.acc = 0
        # self.center_x = self.pos[0]
        # self.center_y = self.pos[1]
        # self.angle = math.degrees(self.vel.heading) - 90

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


class Game(arcade.Window):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)

        self.physics_engine = None

    def setup(self):

        self.scene = arcade.Scene()
        self.scene.add_sprite_list("vehicle")

        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=DEFAULT_DAMPNING, gravity=(0, 0)
        )

        for i in range(50):
            self.spawn_vehicle()

    def spawn_vehicle(self):
        self.vehicle = Vehicle(Vec2())
        self.scene.add_sprite("vehicle", self.vehicle)
        self.physics_engine.add_sprite(
            self.vehicle,
            mass=PLAYER_MASS,
            friction=PLAYER_FRICTION,
            elasticity=0.4,
            moment_of_inertia=20,
            max_velocity=PLAYER_MAX_SPEED,
            damping=PLAYER_DAMPNING,
        )

        self.vehicle.body = self.physics_engine.get_physics_object(
            self.vehicle
        ).body

        

    def on_draw(self):
        self.clear()
        arcade.draw_circle_filled(
            self._mouse_x, self._mouse_y, 25, arcade.color.ALABAMA_CRIMSON
        )
        self.scene.draw()

    def update(self, delta_time: float):
        for vehicle in self.scene["vehicle"]:
            vehicle.seek(Vec2(self._mouse_x, self._mouse_y))
            vehicle.update()
            # stops vehicle from fleeing from itself
            #for other in self.scene["vehicle"]:
             #   if vehicle is not other:
              #      vehicle.flee(other.pos, 150)

        self.physics_engine.step()


game = Game()
game.setup()
arcade.run()
