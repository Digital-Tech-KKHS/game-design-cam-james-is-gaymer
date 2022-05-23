import arcade
from pyglet.math import Vec2

class Vehicle:
    def __init__(self, pos):
        self.pos = Vec2()
        self.vel = Vec2()
        self.acc = Vec2()
        self.forces = []
        self.max_speed = 20
        self.max_force = 0.1

    def draw(self):
        arcade.draw_circle_filled(self.pos[0], self.pos[1], 25, arcade.color.PURPLE_PIZZAZZ)

    def update(self):
        self.acc = sum(self.forces).clamp(-self.max_force, self.max_force)
        self.vel += self.acc
        self.vel = self.vel.clamp(-self.max_speed, self.max_speed)
        self.pos += self.vel
        self.forces = []
        self.acc = 0

    def seek(self, target: Vec2):
        ideal = target - self.pos
        ideal = ideal.from_magnitude(self.max_speed)
        force = ideal - self.vel
        force = force.clamp(-self.max_force, self.max_force)
        self.forces.append(force)

class Game(arcade.Window):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)
        self.vehicle = Vehicle(Vec2())

    def on_draw(self):
        self.clear()
        arcade.draw_circle_filled(self._mouse_x, self._mouse_y, 25, arcade.color.ALABAMA_CRIMSON)
        self.vehicle.draw()

    def update(self, delta_time: float):
        self.vehicle.seek(Vec2(self._mouse_x, self._mouse_y))
        self.vehicle.update()

game = Game()
arcade.run()