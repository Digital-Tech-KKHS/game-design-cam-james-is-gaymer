import arcade
from arcade.experimental import Shadertoy


class Explosion:
    def __init__(self, size, position):
        shader_file_path_2 = 'explosion.glsl'
        self.shadertoy_2 = Shadertoy(size, main_source=open(shader_file_path_2).read())
        self.shadertoy_2.program['pos'] = position
        self.time = 0.0
        self.shadertoy_2.render(time=self.time)
        print("DKBHS")
  

    def update(self, delta_time):
        self.time += delta_time

    #def render(self):
         
        #print("KIHUUIGUB")
