import arcade
import settings
import random
import os

VIEWPORT_MARGIN = 40

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Load a left facing texture and a right facing texture.
        # mirrored=True will mirror the image we load.
        texture = arcade.load_texture("assets/indiana_jones.png", mirrored=True, scale=0.3)
        self.textures.append(texture)
        texture = arcade.load_texture("assets/indiana_jones.png", scale=0.3)
        self.textures.append(texture)

        # By default, face right.
        self.set_texture(settings.TEXTURE_RIGHT)

    def update(self):
        # Figure out if we should face left or right
        if self.change_x < 0:
            self.set_texture(settings.TEXTURE_LEFT)
        if self.change_x > 0:
            self.set_texture(settings.TEXTURE_RIGHT)


class AlexGame(arcade.Window):
    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Set the working directory
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None
        self.wall_list = None


        # Set up the player info
        self.player_sprite = None
        self.physics_engine = None
        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
    
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player()
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 270 
        self.player_list.append(self.player_sprite)

        # Setting the bottom boundaries
        for x in range(32, 1824, 64):
            self.add_boundary(x, -64)
            self.add_boundary(x, 1024)

        # Setting the left boundary
        for y in range(-64, 1064, 64):
            self.add_boundary(-32, y)
            self.add_boundary(1824, y)


        for x in range(200, 1650, 210):
            for y in range(0, 1000, 64):
                # Randomly skip a box so the player can find a way through
                if random.randrange(5) > 0:
                    wall = arcade.Sprite("assets/sandblock.png", 0.64)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)
        
        
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.wall_list)

        arcade.set_background_color(arcade.color.CADMIUM_ORANGE)

        # Set up the viewport boundaries
        self.view_left = 0
        self.view_bottom = 0

    def add_boundary(self, x, y):
        wall = arcade.Sprite("assets/sandblock.png", 0.64)
        wall.center_x = x
        wall.center_y = y
        self.wall_list.append(wall)


    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.wall_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call an update on all sprites
        self.physics_engine.update()
        self.player_sprite.update()

        # --- Manage Scrolling ---

        # Keep track of if we changed the boundary. We don't want to call the
        # set_viewport command if we didn't change the view port.
        changed = False

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + settings.WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + settings.HEIGHT - VIEWPORT_MARGIN
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
                                settings.WIDTH + self.view_left - 1,
                                self.view_bottom,
                                settings.HEIGHT + self.view_bottom - 1)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = settings.MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -settings.MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -settings.MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = settings.MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN or key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT or key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0


def main():
    """ Main method """
    window = AlexGame(settings.WIDTH, settings.HEIGHT, settings.SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    # """This section of code will allow you to run your View
    # independently from the main.py file and its Director.

    # You can ignore this whole section. Keep it at the bottom
    # of your code.
    # It is advised you do not modify it unless you really know
    # what you are doing.
    # """
    # from utils import FakeDirector
    # window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    # my_view = AlexView()
    # my_view.director = FakeDirector(close_on_next_view=True)
    # window.show_view(my_view)
    # arcade.run()
    main()
