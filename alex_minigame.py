import arcade
import settings
import random
import os
import math

VIEWPORT_MARGIN = 40
GEM_COUNT = 10
BULLET_SPEED = 5
WALL_SPRITE_NATIVE_SIZE = 100
WALL_SPRITE_SCALING = 0.64
WALL_SPRITE_SIZE = 64


window = None


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Load a left facing texture and a right facing texture.
        texture = arcade.load_texture("assets/indiana_jones.png", mirrored=True, scale=0.35)
        self.textures.append(texture)
        texture = arcade.load_texture("assets/indiana_jones.png", scale=0.35)
        self.textures.append(texture)

        # By default, face right.
        self.set_texture(settings.TEXTURE_RIGHT)

    def update(self):
        # Check if player should face left or right
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

        # Variables to sprite lists
        self.player_list = None
        self.wall_list = None
        self.gem_list = None
        self.bullet_list = None
        self.enemy_list = None

        # Set up the player info
        self.player_sprite = None
        self.player_health = 60
        self.view_bottom = 0
        self.view_left = 0
        self.collected = 0
        self.collected_text = None
        self.physics_engine = None

        # Set up the enemy info
        self.enemy_sprite = None
        self.enemy_health = 150

    def setup(self):
    
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.gem_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player()
        self.player_sprite.center_x = 0
        self.player_sprite.center_y = 40
        self.player_list.append(self.player_sprite)

        self.add_enemy(583, 46)
        self.add_enemy(1278, 46)

        # Map of the maze
        maze_map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
                    [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1],
                    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1],
                    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
                    [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
                    [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
                    [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],
                    [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
                    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


        # Drawing the maze
        maze_y = 1000

        for row in maze_map:
            maze_x = 0
            for block in row:
                if block == 1:
                    self.add_boundary(maze_x, maze_y)
                maze_x += WALL_SPRITE_SIZE
            maze_y -= WALL_SPRITE_SIZE
        
        # Creating the gems
        for _ in range(GEM_COUNT):
            self.add_gem()
                
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.wall_list)

        arcade.set_background_color(arcade.color.CADMIUM_ORANGE)

        # Set up the viewport boundaries
        self.view_left = 0
        self.view_bottom = 0

    def add_gem(self):
        gem = arcade.Sprite("assets/gem.png", 0.1)
        gem.center_x = random.randrange(0, 1800, 64)
        gem.center_y = random.randrange(0, 1000, 64)
        self.gem_list.append(gem)

    def add_enemy(self, x, y):
        self.enemy_sprite = arcade.Sprite("assets/test_enemy.png", 0.4)
        self.enemy_sprite.center_x = x
        self.enemy_sprite.center_y = y
        self.enemy_list.append(self.enemy_sprite)

    def add_boundary(self, x, y):
        wall = arcade.Sprite("assets/sandblock.png", WALL_SPRITE_SCALING)
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
        self.gem_list.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()

        self.health_bars(self.player_health, self.enemy_health)

        output = f"Gems collected: {self.collected}/10"
        arcade.draw_text(output, 10 + self.view_left, 20 + self.view_bottom, arcade.color.BLACK, 14)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call an update on all sprites
        self.physics_engine.update()
        self.player_sprite.update()
        self.bullet_list.update()
        self.gem_list.update()

        print(self.player_sprite.center_x, self.player_sprite.center_y)

        gem_collected = arcade.check_for_collision_with_list(self.player_sprite, self.gem_list)
        for gem in gem_collected:
            gem.remove_from_sprite_lists()
            self.collected += 1

        for bullet in self.bullet_list:
            # Check this bullet to see if it hit a coin
            disappear_list = arcade.check_for_collision_with_list(bullet, self.wall_list)
            # If it did, get rid of the bullet
            if len(disappear_list) > 0:
                bullet.remove_from_sprite_lists()

            # Check if bullet hit enemys
            enemy_hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            # If it did, enemy health goes down, bullet dissapears
            if len(enemy_hit_list) > 0:
                self.enemy_health -= 30
                bullet.remove_from_sprite_lists()
            
            if self.enemy_health <= 0:
                self.enemy_sprite.remove_from_sprite_lists()

        self.manage_scrolling()

    def manage_scrolling(self):
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

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse moves.
        """
        # Create a bullet
        bullet = arcade.Sprite("assets/bullet.png", 0.15)

        # Position the bullet at the player's current location
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        # Get from the mouse the destination location for the bullet
        # IMPORTANT! If you have a scrolling screen, you will also need
        # to add in self.view_bottom and self.view_left.
        dest_x = x + self.view_left
        dest_y = y + self.view_bottom

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Angle the bullet sprite
        bullet.angle = math.degrees(angle)
        print(f"Bullet angle: {bullet.angle:.2f}")

        # calculate our change_x and change_y
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)
    
    def health_bars(self, player_health, enemy_health):

        player_x = self.player_sprite.center_x - 30 + (player_health/2)
        player_constant_x = self.player_sprite.center_x - 30 + (60/2)
        player_y = self.player_sprite.center_y + 40
        enemy_x = self.enemy_sprite.center_x - 78 + (enemy_health/2)
        enemy_constant_x = self.enemy_sprite.center_x - 78 + (150/2)
        enemy_y = self.enemy_sprite.center_y + 65


        if player_health > 45:
            player_health_colour = arcade.color.GREEN
        elif player_health > 30:
            player_health_colour = arcade.color.YELLOW
        else:
            player_health_colour = arcade.color.RED
        
        if enemy_health > 75:
            enemy_health_colour = arcade.color.GREEN
        elif enemy_health > 50:
            enemy_health_colour = arcade.color.YELLOW
        else:
            enemy_health_colour = arcade.color.RED
        
        # Player Health Bar
        self.draw_player_health_bar(player_constant_x, player_y, player_x, player_health, player_health_colour)
        
        # Enemy 1 Health Bar
        self.draw_enemy_health_bar(enemy_constant_x, enemy_y, enemy_x, enemy_health, enemy_health_colour)

    def draw_player_health_bar(self, player_constant_x, player_y, player_x, player_health, player_health_colour):
        arcade.draw_rectangle_filled(player_constant_x, player_y, 60, 5, arcade.color.WHITE)
        arcade.draw_rectangle_filled(player_x, player_y, player_health, 5, player_health_colour)
        arcade.draw_rectangle_outline(player_constant_x, player_y, 61, 6, arcade.color.BLACK)

    def draw_enemy_health_bar(self, enemy_constant_x, enemy_y, enemy_x, enemy_health, enemy_health_colour):
        arcade.draw_rectangle_filled(enemy_constant_x, enemy_y, 150, 5, arcade.color.WHITE)
        arcade.draw_rectangle_filled(enemy_x, enemy_y, enemy_health, 5, enemy_health_colour)
        arcade.draw_rectangle_outline(enemy_constant_x, enemy_y, 152, 6, arcade.color.BLACK)


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
