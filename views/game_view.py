import random

import arcade

from .entity import BasicEnemy

WIDTH = 1600
HEIGHT = 800
TITLE = "test"

CHARACTER_SCAILING = 2

PLAYER_ACCELERATION = 0.05
PLAYER_DEACCELERATION = 0.02
PLAYER_CHANGE_ANGLE_SPEED = 3
PLAYER_ANGLE_DECCELERATION = 0.03

METEOR_MOVEMENT_CONSTANT = 7


class TestGame(arcade.View):
    def __init__(self):
        super().__init__()

        self.player_sprite = None

        self.scene = None

        self.player_speed = None

        self.accelerating_up = None
        self.accelerating_down = None
        self.accelerating_left = None
        self.accelerating_right = None
        self.moving = None
        self.moving_angle = None

        self.physics_engine = None

        self.camera = None

        arcade.set_background_color(arcade.color.BLACK)

        self.setup()

    def setup(self):

        self.scene = arcade.Scene()
        self.scene.add_sprite_list("player")
        self.scene.add_sprite_list("rocks")
        self.scene.add_sprite_list("zombie")

        self.player_bullet_list = arcade.SpriteList()

        self.camera = arcade.Camera(WIDTH, HEIGHT)

        image_source = "assets/player_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCAILING)
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 400
        self.scene.add_sprite("player", self.player_sprite)

        self.player_speed = 0
        self.accelerating_up = False
        self.accelerating_down = False
        self.accelerating_left = False
        self.accelerating_right = False
        self.moving = False
        self.moving_angle = False
        rock_choices = [
            "meteorGrey_big4.png",
            "meteorGrey_big1.png",
            "meteorGrey_big2.png",
            "meteorGrey_big3.png",
            "meteorGrey_small1.png",
            "meteorGrey_small2.png",
            "meteorGrey_tiny1.png",
            "meteorGrey_tiny2.png",
            "meteorGrey_med1.png",
            "meteorGrey_med2.png",
        ]
        for i in range(10):
            rock = arcade.Sprite(
                f":resources:images/space_shooter/{random.choice(rock_choices)}",
                0.5 + random.random() * 2,
                center_x=random.randint(0, WIDTH),
                center_y=random.randint(0, HEIGHT),
            )
            rock.change_x = (
                random.random() * METEOR_MOVEMENT_CONSTANT
                - METEOR_MOVEMENT_CONSTANT / 2
            )
            rock.change_y = (
                random.random() * METEOR_MOVEMENT_CONSTANT
                - METEOR_MOVEMENT_CONSTANT / 2
            )
            self.scene["rocks"].append(rock)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.scene["player"], self.scene["rocks"]
        )

        enemy = BasicEnemy("enemy")
        enemy.center_x = self.player_sprite.center_x + 50
        enemy.center_y = self.player_sprite.center_y + 50
        self.scene["zombie"].append(enemy)
        
        for i in range(50):
            enemy = BasicEnemy("enemy")
            enemy.center_x = random.randint(-5000,5000)
            enemy.center_y = random.randint(-5000,5000)
            self.scene["zombie"].append(enemy)

    def on_draw(self):
        self.clear()

        self.camera.use()

        self.scene.draw()

    def on_update(self, delta_time):
        self.scene.update()

        self.center_camera()

        if self.accelerating_right:
            self.player_sprite.change_x += PLAYER_ACCELERATION
        if self.accelerating_left:
            self.player_sprite.change_x -= PLAYER_ACCELERATION
        if self.accelerating_up:
            self.player_sprite.change_y += PLAYER_ACCELERATION
        if self.accelerating_down:
            self.player_sprite.change_y -= PLAYER_ACCELERATION
        if not self.moving:
            if self.player_sprite.change_x > 0:
                self.player_sprite.change_x -= PLAYER_DEACCELERATION
            elif self.player_sprite.change_x < 0:
                self.player_sprite.change_x += PLAYER_DEACCELERATION
            if self.player_sprite.change_y > 0:
                self.player_sprite.change_y -= PLAYER_DEACCELERATION
            elif self.player_sprite.change_y < 0:
                self.player_sprite.change_y += PLAYER_DEACCELERATION
        if not self.moving_angle:
            if self.player_sprite.change_angle < 0:
                self.player_sprite.change_angle += PLAYER_ANGLE_DECCELERATION
            if self.player_sprite.change_angle > 0:
                self.player_sprite.change_angle -= PLAYER_ANGLE_DECCELERATION

        for rock in self.scene["rocks"]:
            if rock.center_x < 0:
                rock.center_x = WIDTH
            if rock.center_x > WIDTH:
                rock.center_x = 0
            if rock.center_y < 0:
                rock.center_y = HEIGHT
            if rock.center_y > HEIGHT:
                rock.center_y = 0

        # for rock in self.scene["rocks"]:
        # touching = arcade.check_for_collision_with_list(rock, self.scene["rocks"])

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.accelerating_up = True
            self.moving = True
        if key == arcade.key.S:
            self.accelerating_down = True
            self.moving = True
        if key == arcade.key.D:
            self.accelerating_right = True
            self.moving = True
        if key == arcade.key.A:
            self.accelerating_left = True
            self.moving = True
        if key == arcade.key.LEFT:
            self.player_sprite.change_angle = PLAYER_CHANGE_ANGLE_SPEED
            self.moving_angle = True
        if key == arcade.key.RIGHT:
            self.player_sprite.change_angle = -PLAYER_CHANGE_ANGLE_SPEED
            self.moving_angle = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.accelerating_up = False
            self.moving = False
        if key == arcade.key.S:
            self.accelerating_down = False
            self.moving = False
        if key == arcade.key.D:
            self.accelerating_right = False
            self.moving = False
        if key == arcade.key.A:
            self.accelerating_left = False
            self.moving = False
        if key == arcade.key.LEFT:
            self.moving_angle = False
        if key == arcade.key.RIGHT:
            self.moving_angle = False

    def center_camera(self):
        screen_center_x = self.player_sprite.center_x - WIDTH / 2
        screen_center_y = self.player_sprite.center_y - HEIGHT / 2

        # if screen_center_x < 0:
        # screen_center_x = 0
        # if screen_center_y < 0:
        # screen_center_y = 0

        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)
