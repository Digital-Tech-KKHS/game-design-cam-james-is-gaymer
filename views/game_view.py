import random
import arcade
import math


from views.entity import Rock

from .entity import BasicEnemy
from .entity import Rock

WIDTH = 1600
HEIGHT = 800
TITLE = "test"

CHARACTER_SCAILING = 2

DEFAULT_DAMPNING = 1.0

# player constants that will be implemented into pymunk physics engine
PLAYER_ACCELERATION = 6000
PLAYER_DEACCELERATION = 0.02
PLAYER_MASS = 20
PLAYER_FRICTION = 0.2
PLAYER_MAX_SPEED = 215
PLAYER_DAMPNING = 0.58

# meteor constants settings for physics engine to use
METEOR_MOVEMENT_CONSTANT = 7
METEOR_MASS = 0.5
METEOR_FRICTION = 2.0

MAX_SPAWN_TIME = 1


class TestGame(arcade.View):
    def __init__(self):
        super().__init__()

        self.player_sprite = None
        self.player_body = None

        self.scene = None

        self.player_speed = None

        self.accelerating_up = None
        self.accelerating_down = None
        self.accelerating_left = None
        self.accelerating_right = None

        self.physics_engine = None

        self.camera = None

        self.spawn_time = None
        self.time_between_spawn = None

        arcade.set_background_color(arcade.color.BLACK)

        self.setup()

    def setup(self):

        self.scene = arcade.Scene()
        self.scene.add_sprite_list("player")
        self.scene.add_sprite_list("rocks")
        self.scene.add_sprite_list("zombie")

        # implementing of physics engine into code ready for sprites to be put in
        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=DEFAULT_DAMPNING, gravity=(0, 0)
        )

        #self.player_bullet_list = arcade.SpriteList()

        self.camera = arcade.Camera(WIDTH, HEIGHT)

        image_source = "assets/player_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCAILING)
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 400
        self.scene.add_sprite("player", self.player_sprite)


        self.accelerating_up = False
        self.accelerating_down = False
        self.accelerating_left = False
        self.accelerating_right = False

        enemy = BasicEnemy("enemy")
        enemy.center_x = self.player_sprite.center_x + 50
        enemy.center_y = self.player_sprite.center_y + 50
        self.scene["zombie"].append(enemy)

        self.spawn_time = 0.001
        self.time_between_spawn = 0

        # adds player sprite to physics engine
        # gets player body so code can find variables on player body speed and posistion
        self.physics_engine.add_sprite(
            self.player_sprite,
            mass=PLAYER_MASS,
            friction=PLAYER_FRICTION,
            elasticity=0.4,
            moment_of_inertia=math.inf,
            max_horizontal_velocity=PLAYER_MAX_SPEED,
            max_vertical_velocity=PLAYER_MAX_SPEED,
            damping=PLAYER_DAMPNING,
        )
        self.player_body = self.physics_engine.get_physics_object(
            self.player_sprite
        ).body

    def on_draw(self):
        self.clear()

        self.camera.use()
        

        self.scene.draw()
        self.scene.draw_hit_boxes(color = arcade.color.RED)

    def on_update(self, delta_time):
        #self.scene.update()
        
        self.player_movement()

        self.center_camera()



        self.time_between_spawn += delta_time
        if self.time_between_spawn >= self.spawn_time:
            self.spawn_enemy()
            self.spawn_meteor()
            self.time_between_spawn = 0
            self.spawn_time = 0.001

        # updates physics engine
        self.physics_engine.step()

    def spawn_enemy(self):
        # retreives player position so it can spawn enemies
        player_pos = self.player_body._get_position()

        while True:
            enemy = BasicEnemy("enemy")
            enemy.center_x = random.uniform(player_pos[0] - 4000, player_pos[0] + 4000)
            enemy.center_y = random.uniform(player_pos[1] - 4000, player_pos[1] + 4000)
            # stops enemy from spawning within a certain area from the player
            if not (
                self.camera.position[0] - 50
                < enemy.center_x
                < self.camera.position[0] + WIDTH + 50
                and self.camera.position[1] - 50
                < enemy.center_y
                < self.camera.position[1] + HEIGHT + 50
            ):
                self.scene["zombie"].append(enemy)
                break

    def spawn_meteor(self):
        # retrieves player position to be able to spawn meteors
        player_pos = self.player_body._get_position()

        while True:
            meteor = Rock("meteor")
            meteor.center_x = random.uniform(player_pos[0] - 4000, player_pos[0] + 4000)
            meteor.center_y = random.uniform(player_pos[1] - 4000, player_pos[1] + 4000)
            meteor.angle = random.randint(0, 360)
            meteor.change_x = random.random() * METEOR_MOVEMENT_CONSTANT
                - METEOR_MOVEMENT_CONSTANT / 2

            meteor.change_y = random.random() * METEOR_MOVEMENT_CONSTANT
                - METEOR_MOVEMENT_CONSTANT / 2

            # stops meteor from spawning within a certain area from the player
            if not (
                self.camera.position[0] - 50
                < meteor.center_x
                < self.camera.position[0] + WIDTH + 50
                and self.camera.position[1] - 50
                < meteor.center_y
                < self.camera.position[1] + HEIGHT + 50
            ):
                self.scene["rocks"].append(meteor)

                # creates a mass which is determined by overall area size of the sprite
                # creates an individual body for each meteor and adds it into physics engine
                mass = METEOR_MASS * (meteor.center_y * meteor.center_y )
                self.physics_engine.add_sprite(meteor, mass=mass, elasticity=0.7, moment_of_inertia=math.inf, friction=METEOR_FRICTION, damping=PLAYER_DAMPNING
                

                break

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.accelerating_up = True
        if key == arcade.key.S:
            self.accelerating_down = True
        if key == arcade.key.D:
            self.accelerating_right = True
        if key == arcade.key.A:
            self.accelerating_left = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.accelerating_up = False
        if key == arcade.key.S:
            self.accelerating_down = False
        if key == arcade.key.D:
            self.accelerating_right = False
        if key == arcade.key.A:
            self.accelerating_left = False
                                               
    def player_movement(self):
        # player bodies movement control
        # applies a force to the player body center and moves it in a
        # direction determined by force applied over 2d vectors
        if self.accelerating_right:
            self.player_body.apply_force_at_world_point(
                (PLAYER_ACCELERATION, 0), (0, 0)
            )
        if self.accelerating_left:
            self.player_body.apply_force_at_world_point(
                (-PLAYER_ACCELERATION, 0), (0, 0)
            )
        if self.accelerating_up:
            self.player_body.apply_force_at_world_point(
                (0, PLAYER_ACCELERATION), (0, 0)
            )
        if self.accelerating_down:
            self.player_body.apply_force_at_world_point(
                (0, -PLAYER_ACCELERATION), (0, 0)
            )                                               

    def center_camera(self):
        # retrives player pos for camera centering
        player_pos = self.player_body._get_position()

        screen_center_x = player_pos[0] - WIDTH / 2
        screen_center_y = player_pos[1] - HEIGHT / 2
        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)
