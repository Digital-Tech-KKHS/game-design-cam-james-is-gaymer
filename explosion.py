import arcade
from arcade.experimental import Shadertoy


class Explosion:
    """runs explosion shader every time it is called"""
    def __init__(self, size, position):
        """sets up shader and retrives needed parameters 
        from game to get right position on screen
        """
        shader_file_path_2 = "explosion.glsl"
        self.shadertoy_2 = Shadertoy(size, main_source=open(shader_file_path_2).read())
        self.shadertoy_2.program["pos"] = position
        self.time = 0.0
        self.shadertoy_2.render(time=self.time)

    def update(self, delta_time):
        """allows shader to update and change each frame
        """
        self.time += delta_time

    def draw(self):
        """draws shader on screen
        """
        self.shadertoy_2.render(time=self.time)
