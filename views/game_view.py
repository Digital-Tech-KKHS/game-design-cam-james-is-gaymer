import math
import random

import arcade
from pyglet.math import Vec2

from const import *
from game_play.collectables import *
from game_play.entity import *
from game_play.explosion import Explosion
from views.inventory import InventoryView



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

        self.scrap_steel = int
        self.scrap_copper = int
        self.acid = int

        self.time = 0.0
        self.reset = 0.0
        self.player_health = PLAYER_HEALTH
        self.color = arcade.color.GREEN

        self.explosion = []
        self.background = None

        self.laser_sound = 0

        self.setup()

    def setup(self):
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("bullets")
        self.scene.add_sprite_list("mining_laser")
        self.scene.add_sprite_list("player")
        self.scene.add_sprite_list("rocks")
        self.scene.add_sprite_list("zombie")
        self.scene.add_sprite_list("scrap")

        self.background = arcade.load_texture("assets/background.png")

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

        self.scrap_steel = 0
        self.scrap_copper = 0
        self.acid = 0

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

        arcade.draw_lrwh_rectangle_textured(
            self.camera.position[0],
            self.camera.position[1],
            WIDTH,
            HEIGHT,
            self.background,
        )

        self.camera.use()

        self.scene.draw()

        for explosion in self.explosion:
            explosion.draw()

        player_pos = self.player_body._get_position()
        arcade.draw_rectangle_filled(
            player_pos[0],
            player_pos[1] - 480,
            self.player_health / 3,
            15,
            self.color,
        )

    def on_update(self, delta_time):
        self.scene.update()

        self.scene["mining_laser"].clear()

        self.player_movement()
        for enemy in self.scene["zombie"]:
            enemy.seek(Vec2(self.player_sprite.center_x, self.player_sprite.center_y))
            enemy.update()
            for other in self.scene["zombie"]:
                if enemy is not other:
                    enemy.flee(other.pos, 150)

            for rocks in self.scene["rocks"]:
                enemy.flee(rocks.pos, 300)
        for explosion in self.explosion:
            explosion.update(delta_time)
            if explosion.time >= 2.0:
                self.explosion.remove(explosion)

        if self.player_health >= 50:
            self.color = arcade.color.RED

        self.center_camera()

        self.meteor_kill()

        self.bullet_kill()
        self.enemy()

        self.pick_up()

        self.time_between_spawn += delta_time
        if self.time_between_spawn >= self.spawn_time:

            self.spawn_enemy()

            self.spawn_meteor()
            self.time_between_spawn = 0
            self.spawn_time = 0.001  # random.uniform(3, MAX_SPAWN_TIME)

        # updates physics engine
        self.physics_engine.step()
        if self.laser_on:
            self.fire_laser()


        self.scene.update_animation(1 / 60)

        if self.player_health <= 0:
            print("YOU LOST")
            self.window.show_view(self.window.death_view)


    def spawn_enemy(self):
        # retreives player position so it can spawn enemies
        player_pos = self.player_body._get_position()

        if len(self.scene["zombie"]) < 20:

            while True:
                enemy = BasicEnemy("enemy")
                enemy.center_x = random.uniform(
                    player_pos[0] - 1000, player_pos[0] + 1000
                )
                enemy.center_y = random.uniform(
                    player_pos[1] - 1000, player_pos[1] + 1000
                )
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

                    self.physics_engine.add_sprite(
                        enemy, PLAYER_MASS, PLAYER_FRICTION, 0.7
                    )
                    self.enemy_body = self.physics_engine.get_physics_object(enemy).body
                    break

    def spawn_meteor(self):
        # retrieves player position to be able to spawn meteors
        player_pos = self.player_body._get_position()
        if len(self.scene["rocks"]) < 200:

            while True:
                meteor = Rock("meteor")
                meteor.center_x = random.uniform(
                    player_pos[0] - 4100, player_pos[0] + 4100
                )
                meteor.center_y = random.uniform(
                    player_pos[1] - 4100, player_pos[1] + 4100
                )
                meteor.angle = random.randint(0, 360)
                self.meteor_health = meteor.rock_health

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
                        meteor,
                        mass=meteor.rock_mass,
                        damping=METEOR_FRICTION,
                        elasticity=0.7,
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
        if key == arcade.key.E:
            self.window.show_view(self.window.inventory)
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.pause_view)

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
        if button == arcade.MOUSE_BUTTON_LEFT:
            player_pos = Vec2(self.player_sprite.center_x, self.player_sprite.center_y)
            mouse_pos = Vec2(x, y)
            mouse_pos += self.camera.position
            speed = mouse_pos - player_pos
            scaled_speed = speed.from_magnitude(BULLET_MAX_SPEED)
            bullet = Bullet()
            bullet.center_x = self.player_sprite.center_x
            bullet.center_y = self.player_sprite.center_y
            self.physics_engine.add_sprite(bullet, mass=1000)
            bullet_body = self.physics_engine.get_physics_object(bullet).body
            bullet_body._set_velocity(scaled_speed)
            self.scene["bullets"].append(bullet)
            laser_sound = arcade.load_sound("assets/laserShoot.wav")
            arcade.play_sound(laser_sound, volume=0.5)
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.laser_on = True
            if self.laser_sound == 0:
                laser_sound = arcade.load_sound("assets/laser.wav")
                arcade.play_sound(laser_sound, volume=0.5)
                self.laser_sound = 1

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

        keep_going = True
        for i in range(50):

            if keep_going:
                hypot = i * 16
                laser = arcade.Sprite(image_source1)
                laser.center_x = pos[0] + (hypot * math.cos(angle_radians))
                laser.center_y = pos[1] + (hypot * math.sin(angle_radians))
                laser.angle = angle_degrees
                laser.alpha = 255 - i * (255 / 50)
                self.scene["mining_laser"].append(laser)
                rocklist = arcade.check_for_collision_with_list(
                    laser, self.scene["rocks"]
                )
            if rocklist:

                contact = arcade.Sprite(image_source2)
                contact.center_x = laser.center_x + (5 * math.cos(angle_radians))
                contact.center_y = laser.center_y + (5 * math.sin(angle_radians))
                contact.angle = angle_degrees
                contact.alpha = laser.alpha
                self.scene["mining_laser"].append(contact)
                keep_going = False

            for meteor in rocklist:

                meteor.take_damage()
                if meteor.rock_health <= 0:

                    prize = self.get_drop()
                    if prize:
                        prize.center_x = meteor.center_x + random.randint(-50, 50)
                        prize.center_y = meteor.center_y + random.randint(-50, 50)
                        # prize.change_x = random.randint(-2, 2)
                        # prize.change_y = random.randint(-2, 2)
                        self.scene["scrap"].append(prize)
                    explosion_sound = arcade.load_sound("assets/explosion.wav")
                    arcade.play_sound(explosion_sound, volume=0.3)
                    meteor.kill()

    def on_mouse_release(self, *args, **kwargs):
        self.laser_on = False
        self.laser_sound = 0

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

    def get_drop(self):
        common = [ScrapSteel(), ScrapCopper(), Acid()]
        rare = ["assets/drop_4.png"]
        legendary = ["assets/drop_5.png"]
        drop_choice = random.random()
        if drop_choice < 0.6:
            return
        if 0.6 <= drop_choice > 0.8:
            return random.choice(common)

    def bullet_kill(self):

        enemy_explosion = arcade.load_sound("assets/explosion_enemy.wav")
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
            for zombie in self.scene["zombie"]:
                good_collision = arcade.check_for_collision(bullet, zombie)
                if good_collision:
                    collision = Explosion(
                        (WIDTH, HEIGHT),
                        (
                            bullet.center_x - self.camera.position[0],
                            bullet.center_y - self.camera.position[1],
                        ),
                    )
                    self.explosion.append(collision)
                    arcade.play_sound(enemy_explosion, volume=0.5)
                    bullet.kill()
                    zombie.kill()

    def enemy(self):
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
            collision = arcade.check_for_collision(enemy, self.player_sprite)

            if collision:
                self.player_health -= 5

    def pick_up(self):

        for drop in self.scene["scrap"]:
            if (
                arcade.check_for_collision(self.player_sprite, drop)
                and len(self.window.resources) < 25
            ):
                self.scene["scrap"].remove(drop)
                self.window.resources.append(drop)
