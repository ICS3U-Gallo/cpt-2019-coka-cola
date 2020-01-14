import arcade
import settings
import random
import os
import math

WIDTH = 800
HEIGHT = 600
GRAVITY = 1
PLAYER_JUMP_SPEED = 17
PLAYER_HEALTH = 2
VIEWPORT_MARGIN = 600
BULLET_SPEED = 4.5

class KevinView(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.CADMIUM_ORANGE)
        # Set up the player
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.enemy_list = None
        self.wall_list = None
        self.player_list = None
        self.obstacles_list = None
        self.background = None
        self.BEEMOVE = 7
        self.bullet_list = None
        # Separate variable that holds the player sprite
        self.frame_count = 0

        self.finish_list = None
        self.physics_engine = None

        # self.player = arcade.Sprite(center_x=WIDTH//2, center_y=100)
        
        
        self.bullets_texture = arcade.make_soft_circle_texture(15, 
                         arcade.color.BLACK, outer_alpha=255)
        

        self.view_bottom = 0
        self.view_left = 0
        
        

        # If you have sprite lists, you should create them here,
        # and set them to None

    def on_show(self):
        # Create your sprites and sprite lists here
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.obstacles_list = arcade.SpriteList()
        self.finish_list = arcade.SpriteList()
        self.player_sprite = arcade.Sprite("assets/indiana_jones.png", 0.5)
        # Add top-left enemy ship
        enemy = arcade.Sprite(":resources:images/space_shooter/playerShip1_green.png", 0.5)
        enemy.center_x = 3000
        enemy.center_y = HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)

        # Add top-right enemy ship
        enemy = arcade.Sprite(":resources:images/space_shooter/playerShip1_green.png", 0.5)
        enemy.center_x = 3500
        enemy.center_y = HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)

        #another one
        enemy = arcade.Sprite(":resources:images/space_shooter/playerShip1_green.png", 0.5)
        enemy.center_x = 4000
        enemy.center_y = HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)

        #slime
        self.slime = arcade.Sprite(":resources:images/enemies/slimePurple.png", 1)
        self.slime.center_x = 3500
        self.slime.center_y = 135
        self.obstacles_list.append(self.slime)
        
        #bee
        self.bee = arcade.Sprite(":resources:images/enemies/bee.png", 0.7)
        self.bee.center_x = 4000
        self.bee.center_y = 225
        self.obstacles_list.append(self.bee)
        
        #flag
        self.flag = arcade.Sprite(":resources:images/items/flagGreen1.png", 0.8)
        self.flag.center_x = 400
        self.flag.center_y = 135
        
        # self.player.texture = arcade.make_soft_square_texture(50, arcade.color.BLUE, outer_alpha=255)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 135
        self.player_list.append(self.player_sprite)
        
        for x in range(0, 3000, 100):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 1)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)
        
        for x in range(4200, 7000, 100):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 1)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        ycor = 75
        for x in range(3200, 4000, 300):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 0.7)
            wall.center_x = x
            wall.center_y = ycor
            ycor += 50
            self.wall_list.append(wall)
        
        for x in range(800, 1800, 400):
            spike = arcade.Sprite(":resources:images/tiles/spikes.png", 1)
            spike.center_x = x
            spike.center_y = 135
            self.obstacles_list.append(spike)

        door_bot = arcade.Sprite(":resources:images/tiles/doorClosed_mid.png", 1)
        door_bot.center_x = 6000
        door_bot.center_y = 135
        door_top = arcade.Sprite(":resources:images/tiles/doorClosed_top.png", 1)
        door_top.center_x = 6000
        door_top.center_y = 230
        
        self.finish_list.append(door_bot)
        self.finish_list.append(door_top)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)

    def on_draw(self):
        arcade.start_render()

        self.enemy_list.draw()
        self.bullet_list.draw()
        self.flag.draw()
        self.finish_list.draw()
        self.obstacles_list.draw()
        self.player_list.draw()
        self.wall_list.draw()
        
        # Draw everything below here.
        
    
    def update(self, delta_time):
        

        self.physics_engine.update()
        self.slime.center_x -= 7
        self.bee.center_x -= self.BEEMOVE
        if self.bee.center_x < self.player_sprite.center_x - 150:
            self.BEEMOVE = -15
        for obstacle in self.obstacles_list:
            obstacle_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.obstacles_list)
            if len(obstacle_hit_list) > 0:
                self.view_left = 5
                self.player_sprite.center_x = 50
                self.slime.center_x = 3500
                self.bee.center_x = 4000
                self.BEEMOVE = 7

        for finish in self.finish_list:
            finish_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.finish_list)
            if len(finish_hit_list) > 0:
                self.view_left = 5
                self.player_sprite.center_x = 50
                self.slime.center_x = 3500
                self.bee.center_x = 4000
                self.BEEMOVE = 7
        if self.player_sprite.center_y < 60:
            self.view_left = 5
            self.player_sprite.center_x = 50
            self.player_sprite.center_y = 135
            self.slime.center_x = 3500
            self.bee.center_x = 4000
            self.BEEMOVE = 7

        self.frame_count += 1
        for enemy in self.enemy_list:

            # First, calculate the angle to the player. We could do this
            # only when the bullet fires, but in this case we will rotate
            # the enemy to face the player each frame, so we'll do this
            # each frame.

            # Position the start at the enemy's current location
            start_x = enemy.center_x
            start_y = enemy.center_y

            # Get the destination location for the bullet
            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the enemy to face the player.
            enemy.angle = math.degrees(angle)-90

            # Shoot every 60 frames change of shooting each frame
            if(self.player_sprite.center_x > 2000):
                if self.frame_count % 60 == 0:
                    bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")
                    bullet.center_x = start_x
                    bullet.center_y = start_y

                    # Angle the bullet sprite
                    bullet.angle = math.degrees(angle)

                    # Taking into account the angle, calculate our change_x
                    # and change_y. Velocity is how fast the bullet travels.
                    bullet.change_x = math.cos(angle) * BULLET_SPEED
                    bullet.change_y = math.sin(angle) * BULLET_SPEED

                    self.bullet_list.append(bullet)

            # Get rid of the bullet when it flies off-screen
            for bullet in self.bullet_list:
                if bullet.top < 0:
                    bullet.remove_from_sprite_lists()

            self.bullet_list.update()

            #bullet collision
            for bullet in self.bullet_list:
                bullet_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.bullet_list)
                if len(bullet_hit_list) > 0:
                    self.view_left = 5
                    self.player_sprite.center_x = 50
                    self.slime.center_x = 3500
                    self.bee.center_x = 4000
                    self.BEEMOVE = 7
                


         # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        

        # Make sure our boundaries are integer values. While the view port does
        # support floating point numbers, for this application we want every pixel
        # in the view port to map directly onto a pixel on the screen. We don't want
        # any rounding errors.
        self.view_left = int(self.view_left)
        

        # If we changed the boundary values, update the view port to match
        if changed:
            arcade.set_viewport(self.view_left, WIDTH + self.view_left - 1, 0, HEIGHT  - 1)


    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -10
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 10

        """
        Called whenever a key on the keyboard is pressed.
        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        bullet = arcade.Sprite()
        bullet.center_x = self.player.center_x
        bullet.center_y = self.player.center_y
        bullet.change_y = 5 
        bullet.texture = self.bullets_texture
        bullet.width = 5

        self.bullets_list.append(bullet)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


# def main():
#     game = MyGame(WIDTH, HEIGHT, "My Game")
#     game.setup()
#     arcade.run()


if __name__ == "__main__":
    from utils import FakeDirector
    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    my_view = KevinView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
    # main()
    
