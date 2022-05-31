import arcade
import random
from pyglet.math import Vec2
import math

class Vehicle(arcade.Sprite):
    def __init__(self, pos):
        super().__init__(":resources:images/space_shooter/playerShip1_orange.png", 0.3)
        self.pos = Vec2(random.randint(0,800),random.randint(0,800))
        self.vel = Vec2()
        self.acc = Vec2()
        self.forces = []
        self.max_speed = 20
        self.max_force = 0.2
        



    def update(self):
        self.acc = sum(self.forces).clamp(-self.max_force, self.max_force)
        self.vel += self.acc
        self.vel = self.vel.clamp(-self.max_speed, self.max_speed)
        self.pos += self.vel
        self.forces = []
        self.acc = 0
        self.center_x = self.pos[0]
        self.center_y = self.pos[1]
        self.angle = math.degrees(self.vel.heading) - 90

    def seek(self, target: Vec2):
        ideal = target - self.pos
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

        

    def setup(self):
            
            self.scene = arcade.Scene()
            self.scene.add_sprite_list("vehicle")
            for i in range(50):
                self.vehicle = Vehicle(Vec2())
                self.scene.add_sprite("vehicle", self.vehicle)


    def on_draw(self):
        self.clear()
        arcade.draw_circle_filled(self._mouse_x, self._mouse_y, 25, arcade.color.ALABAMA_CRIMSON)
        self.scene.draw()

    def update(self, delta_time: float):
        for vehicle in self.scene["vehicle"]:
            vehicle.seek(Vec2(self._mouse_x, self._mouse_y))
            vehicle.update()
            for other in self.scene["vehicle"]:
                if vehicle is not other:
                    vehicle.flee(other.pos, 150)

game = Game()
game.setup()
arcade.run()