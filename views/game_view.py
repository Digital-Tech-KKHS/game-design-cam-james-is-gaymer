import math
import random
from email.mime import image

from pyglet.math import Vec2
import arcade
from pyglet.math import Vec2

from const import METOR_MAX_SPEED, METOR_MIN_SPEEED

from .entity import BasicEnemy, Bullet, Rock
from const import *



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

        self.gun_select = None
        self.laser_on = False

        arcade.set_background_color(arcade.color.BLACK)

        self.setup()

    def setup(self):

        self.scene = arcade.Scene()
        self.scene.add_sprite_list("bullets")
        self.scene.add_sprite_list("mining_laser")
        self.scene.add_sprite_list("player")
        self.scene.add_sprite_list("rocks")
        self.scene.add_sprite_list("zombie")
        self.scene.add_sprite_list("health")

        # implementing of physics engine into code ready for sprites to be put in
        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=DEFAULT_DAMPNING, gravity=(0, 0)
        )

        # self.player_bullet_list = arcade.SpriteList()

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


        self.spawn_time = 0.001
        self.time_between_spawn = 0

        # adds player sprite to physics engine
        # gets player body so code can find variables ]
        # on player body speed and posistion
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

        self.gun_select = 1



    def on_draw(self):
        self.clear()

        self.camera.use()

        self.scene.draw()

    

    def on_update(self, delta_time):
        # self.scene.update()
        self.scene['mining_laser'].clear()

        self.player_movement()
        for enemy in self.scene["zombie"]:
            enemy.seek(Vec2(self.player_sprite.center_x, self.player_sprite.center_y))
            enemy.update()

        self.center_camera()

        self.meteor_kill()

        self.bullet_kill()

        self.time_between_spawn += delta_time
        if self.time_between_spawn >= self.spawn_time:
            #self.spawn_enemy()
            self.spawn_meteor()
            self.time_between_spawn = 0
            self.spawn_time = 0.001  # random.uniform(3, MAX_SPAWN_TIME)

        # for rock in self.scene["rocks"]:
        #     if rock.center_x > (self.player_sprite.center_x + 50):
        #         rock.kill()

        # updates physics engine
        self.physics_engine.step()
        if self.laser_on:
            self.fire_laser()

    def spawn_enemy(self):
        # retreives player position so it can spawn enemies
        player_pos = self.player_body._get_position()
        if len(self.scene["zombie"]) < 150:
            while True:
                enemy = BasicEnemy("enemy")
                enemy.center_x = random.uniform(player_pos[0] - 1000, player_pos[0] + 1000)
                enemy.center_y = random.uniform(player_pos[1] - 1000, player_pos[1] + 1000)
                # stops enemy from spawning within
                # a certain area from the player
                if not (
                    self.camera.position[0] - 50
                    < enemy.center_x
                    < self.camera.position[0] + WIDTH + 50
                    and self.camera.position[1] - 50
                    < enemy.center_y
                    < self.camera.position[1] + HEIGHT + 50
                ):
                    self.scene["zombie"].append(enemy)

                    self.physics_engine.add_sprite(enemy,PLAYER_MASS, PLAYER_FRICTION, 0.7)
                    self.enemy_body = self.physics_engine.get_physics_object(enemy).body
                    break

    def spawn_meteor(self):
        # retrieves player position to be able to spawn meteors
        player_pos = self.player_body._get_position()
        if len(self.scene["rocks"]) < 300:

            while True:
                meteor = Rock("meteor")
                meteor.center_x = random.uniform(
                    player_pos[0] - 4100, player_pos[0] + 4100
                )
                meteor.center_y = random.uniform(
                    player_pos[1] - 4100, player_pos[1] + 4100
                )
                meteor.angle = random.randint(0, 360)

                # stops meteor from spawning within
                # a certain area from the player
                if not (
                    self.camera.position[0] - 50
                    < meteor.center_x
                    < self.camera.position[0] + WIDTH + 50
                    and self.camera.position[1] - 50
                    < meteor.center_y
                    < self.camera.position[1] + HEIGHT + 50
                ):
                    self.scene["rocks"].append(meteor)
                    

                    # runs function in rock class to find image width and height
                    # calculates mass with a mass constant


                    # creates an individual body for each,
                    # meteor and adds it into physics engine
                    self.physics_engine.add_sprite(
                        meteor, mass=meteor.rock_mass, damping=METEOR_FRICTION, elasticity=0.7
                    )
                    self.rock_body = self.physics_engine.get_physics_object(meteor).body

                    # runs speed function in rock class
                    # gives speed in a single variable in a tuple
                    # applies force to specified body
                    speed_x = random.uniform(METOR_MIN_SPEEED, METOR_MAX_SPEED)
                    speed_y = random.uniform(METOR_MIN_SPEEED, METOR_MAX_SPEED)
                    rock_speed = (speed_x, speed_y)
                    self.rock_body.apply_force_at_world_point((rock_speed), (0, 0))

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
        if key == arcade.key.KEY_1:
            self.gun_select = 1
        if key == arcade.key.KEY_2:
            self.gun_select = 2

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

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.gun_select == 1:
            player_pos = Vec2(self.player_sprite.center_x, self.player_sprite.center_y)
            mouse_pos = Vec2(x, y)
            mouse_pos += self.camera.position
            speed = mouse_pos - player_pos
            scaled_speed = speed.from_magnitude(MAX_SPEED)
            bullet = Bullet()
            bullet.center_x = self.player_sprite.center_x
            bullet.center_y = self.player_sprite.center_y
            self.physics_engine.add_sprite(bullet, mass=1000)
            bullet_body = self.physics_engine.get_physics_object(bullet).body
            bullet_body._set_velocity(scaled_speed)
            self.scene["bullets"].append(bullet)
        if self.gun_select == 2:
            self.laser_on = True
        
    def fire_laser(self):
        x = self.window._mouse_x
        y = self.window._mouse_y
        image_source1 = "assets\mining_laser.png"
        image_source2 = "assets\mining_laser_contact.png"
        pos = (self.player_sprite.center_x, self.player_sprite.center_y)
        diff_y = y - self.player_sprite.center_y
        diff_x = x - self.player_sprite.center_x
        diff_y += self.camera.position[1]
        diff_x += self.camera.position[0]
        angle_radians = math.atan2(diff_y, diff_x)
        angle_degrees = math.degrees(math.atan2(diff_y, diff_x)) + 90
        for i in range(50):
            hypot = i * 16
            laser = arcade.Sprite(image_source1)
            laser.center_x = pos[0] + (hypot * math.cos(angle_radians))
            laser.center_y = pos[1] + (hypot * math.sin(angle_radians))
            laser.angle = angle_degrees
            laser.alpha = 255 - i * (255/50)
            self.scene["mining_laser"].append(laser)
            if arcade.check_for_collision_with_list(laser, self.scene['rocks']):
                contact = arcade.Sprite(image_source2)
                contact.center_x = laser.center_x + (5 * math.cos(angle_radians))
                contact.center_y = laser.center_y + (5 * math.sin(angle_radians))
                contact.angle = angle_degrees
                contact.alpha = laser.alpha
                self.scene["mining_laser"].append(contact)
                break 

    def on_mouse_release(self, *args, **kwargs):
        self.laser_on = False


    def meteor_kill(self):
        player_pos = self.player_body._get_position()
        for rock in self.scene["rocks"]:
            if rock.center_x >= (player_pos[0] + 4100) or rock.center_x <= (
                player_pos[0] - 4200
            ):
                rock.kill()
            if rock.center_y >= (player_pos[1] + 4100) or rock.center_y <= (
                player_pos[1] - 4200
            ):
                rock.kill()

    def bullet_kill(self):
        
        player_pos = self.player_body._get_position()
        for bullet in self.scene["bullets"]:
            collision = arcade.check_for_collision_with_list(
                bullet, self.scene["rocks"]
                )
            for b in collision:
                    bullet.kill()
            if bullet.center_x >= (player_pos[0] + WIDTH) or bullet.center_x <= (
                player_pos[0] - WIDTH
                ):
                bullet.kill()
            if bullet.center_y >= (player_pos[1] + HEIGHT) or bullet.center_y <= (
                player_pos[1] - HEIGHT
                ):
                bullet.kill()
            for zombie in self.scene['zombie']:
                good_collision = arcade.check_for_collision(bullet, zombie)
                if good_collision:
                    bullet.kill()
                    zombie.kill()

    def enemy_kill(self):
        player_pos = self.player_body._get_position()
        for enemy in self.scene["zombie"]:
            if enemy.center_x >= (player_pos[0] + 4100) or enemy.center_x <= (
                player_pos[0] - 4200
            ):
                enemy.kill()
            if enemy.center_y >= (player_pos[1] + 4100) or enemy.center_y <= (
                player_pos[1] - 4200
            ):
                enemy.kill()
