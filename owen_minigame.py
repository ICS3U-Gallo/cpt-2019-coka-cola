import random
import arcade
import os
import settings

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Flappy Jones"
VIEWPORT_MARGIN = 300
MOVEMENT_SPEED = 5
BULLET_SPEED = 2


class OwenMenuView(arcade.View):
    """ Main application class. """

    def __init__(self):
        """
        Initializer 
        """
        super().__init__()
    
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Sprite lists
        self.player_list = None
        self.coin_list = None

        # Set up the player
        self.player_sprite = None
        self.wall_list = None
        self.view_bottom = 0
        self.view_left = 0

        self.frame_count = 0
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

    def on_show(self):

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite("assets/indiana_jones.png", 0.3)
        self.player_sprite.center_x = 64 
        self.player_sprite.center_y = 270
        self.player_list.append(self.player_sprite) 

        for x in range(200, 1650, 64):
            wall = arcade.Sprite("assets/rock.png", 0.1)
            wall.center_x = x
            wall.center_y = 0
            self.wall_list.append(wall)
        
        for x in range(200, 1650, 64): 
            wall = arcade.Sprite("assets/rock.png", 0.1)
            wall.center_x = x
            wall.center_y = 1035
            self.wall_list.append(wall)

        for y in range(0, 1035, 64):
            wall = arcade.Sprite("assets/rock.png", 0.1)
            wall.center_x = 1680
            wall.center_y = y
            self.wall_list.append(wall)

        # -- Set up several columns of walls
        for x in range(200, 1650, 400):
            for y in range(69, 1000, 64):
                # Randomly skip a box so the player can find a way through
                if random.randrange(5) > 0:
                    wall = arcade.Sprite("assets/rock.png", 0.1)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        # Set the background color
        arcade.set_background_color(arcade.color.YELLOW_ORANGE)

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

        enemy = arcade.Sprite("assets/rock.png", 0.1)
        enemy.center_x = 390
        enemy.center_y = 967
        enemy.angle = 180
        self.enemy_list.append(enemy)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.player_sprite.draw()
        self.wall_list.draw()
        

        self.enemy_list.draw()
        self.bullet_list.draw() 



    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.physics_engine.update()

        changed = False

        self.frame_count += 1

        for enemy in self.enemy_list:
            if self.frame_count % 120 == 0:
                bullet = arcade.Sprite("assets/bullet.png", 0.3)
                bullet.center_x = enemy.center_x
                bullet.angle = -90
                bullet.top = enemy.bottom
                bullet.change_y = -2
                self.bullet_list.append(bullet)
        
        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()
        
        self.bullet_list.update()

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        # Make sure our boundaries are integer values. While the view port does
        # support floating point numbers, for this application we want every pixel
        # in the view port to map directly onto a pixel on the screen. We don't want
        # any rounding errors.
        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        # If we changed the boundary values, update the view port to match
        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left - 1,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom - 1)
        
        #self.player_sprite.change_x = 1

if __name__ == "__main__":
    from utils import FakeDirector
    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    my_view = OwenMenuView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
