import arcade
import settings
import random
import os
import math
import time
from caleb_minigame import CalebMenuView

# Constant variables
VIEWPORT_MARGIN = 250
BULLET_SPEED = 20

# Sizes and scaling of sprites
WALL_SPRITE_NATIVE_SIZE = 100
WALL_SPRITE_SCALING = 0.64
WALL_SPRITE_SIZE = WALL_SPRITE_NATIVE_SIZE * WALL_SPRITE_SCALING

# Variables to hold images for sprites
PLAYER_IMAGE = "assets/indiana_jones.png"
ENEMY_IMAGE = "assets/sand_devil.png"
BOSS_IMAGE = "assets/sand_boss.png"
GEM_BLUE_IMAGE = "assets/gem_blue.png"
GEM_GREEN_IMAGE = "assets/gem_green.png"
GEM_RED_IMAGE = "assets/gem_red.png"
BULLET_IMAGE = "assets/bullet.png"
WALL_IMAGE = "assets/sandblock.png"
KEY_IMAGE = "assets/key.png"
ARCADE_FONT = "assets/arcade_font/PressStart2P-vaV7.ttf"


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Load a left facing player and a right facing player.
        texture = arcade.load_texture(PLAYER_IMAGE, mirrored=True, scale=0.35)
        self.textures.append(texture)
        texture = arcade.load_texture(PLAYER_IMAGE, scale=0.35)
        self.textures.append(texture)

        # By default, face right.
        self.set_texture(settings.TEXTURE_RIGHT)

    def update(self):
        # Check if player should face left or right
        if self.change_x < 0:
            self.set_texture(settings.TEXTURE_LEFT)
        if self.change_x > 0:
            self.set_texture(settings.TEXTURE_RIGHT)


class Enemy(arcade.Sprite):
    def __init__(self, x, y, health):
        super().__init__()

        # Dictionary to store health bar textures.
        self.health_bar_textures = {
            'full': arcade.make_soft_square_texture(5, arcade.color.GREEN, outer_alpha=255),
            'damaged': arcade.make_soft_square_texture(5, arcade.color.YELLOW, outer_alpha=255),
            'critical': arcade.make_soft_square_texture(5, arcade.color.RED, outer_alpha=255),
            'background': arcade.make_soft_square_texture(5, arcade.color.WHITE, outer_alpha=255),
            'outline': arcade.make_soft_square_texture(7, arcade.color.BLACK, outer_alpha=255)
        }
        
        # Load a right facing enemy, and a left facing enemy.
        texture = arcade.load_texture(ENEMY_IMAGE, scale=0.3)
        self.textures.append(texture)
        texture = arcade.load_texture(ENEMY_IMAGE, mirrored=True, scale=0.3)
        self.textures.append(texture)

        # By defalt, the enemy faces right.
        self.set_texture(settings.TEXTURE_RIGHT)

        self.health_texture = self.health_bar_textures.get("full")
        self.health_max_x = 0
        self.max_health = -1
        self.health_bar_width = 76

        self.center_x = x
        self.center_y = y
        self.health = health

        if self.max_health == -1:
            self.max_health = health

        # Initialize variables to use when drawing the health bar sprites.
        self.health_x = self.center_x - 40 + (self.health/2)
        self.health_max_x = self.center_x - 40 + (75/2)
        self.health_y = self.center_y + 47

        # Health bar that changes colour.
        self.health_sprite = arcade.Sprite()
        self.health_sprite.append_texture(self.health_bar_textures.get("full"))
        self.health_sprite.append_texture(self.health_bar_textures.get("damaged"))
        self.health_sprite.append_texture(self.health_bar_textures.get("critical"))
        self.health_sprite.set_texture(0)
        self.health_sprite.center_x = self.health_x
        self.health_sprite.center_y = self.health_y

        # Outline of health bar.
        self.health_outline_sprite = arcade.Sprite()
        self.health_outline_sprite.append_texture(self.health_bar_textures.get("outline"))
        self.health_outline_sprite.set_texture(0)
        self.health_outline_sprite.center_x = self.health_max_x
        self.health_outline_sprite.center_y = self.health_y
        self.health_outline_sprite.width = self.health_bar_width
        
        # Background of health bar.
        self.health_background_sprite = arcade.Sprite()
        self.health_background_sprite.append_texture(self.health_bar_textures.get("background"))
        self.health_background_sprite.set_texture(0)
        self.health_background_sprite.center_x = self.health_max_x
        self.health_background_sprite.center_y = self.health_y
        self.health_background_sprite.width = self.health_bar_width - 2

    def update(self):
        self.health_x = self.center_x - 40 + (self.health/2)
        self.health_max_x = self.center_x - 40 + (75/2)
        self.health_y = self.center_y + 47

        # Check to see what colour the health bar should be based on
        # how much health the enemy has.
        if self.health > self.max_health * 2/3:
            self.health_sprite.set_texture(0)
        elif self.health > self.max_health * 1/3:
            self.health_sprite.set_texture(1)
        else:
            self.health_sprite.set_texture(2)

        # Update the position of the health bars
        self.health_sprite.center_x = self.health_x
        self.health_sprite.center_y = self.health_y
        self.health_outline_sprite.center_x = self.health_max_x
        self.health_outline_sprite.center_y = self.health_y
        self.health_background_sprite.center_x = self.health_max_x
        self.health_background_sprite.center_y = self.health_y

        self.health_sprite.width = self.health

        if self.change_x < 0:
            self.set_texture(settings.TEXTURE_LEFT)
        if self.change_x > 0:
            self.set_texture(settings.TEXTURE_RIGHT)

    def follow_player(self, player_sprite):
        
        # print(self.center_x, self.change_x, self.center_y , self.change_y)
        new_center_x = self.center_x + self.change_x
        new_center_y = self.center_y + self.change_y

        if self.check_x(new_center_x) and self.check_y(new_center_y):
            # print("here", new_center_x, -new_center_y)
            self.center_x = new_center_x
            self.center_y = new_center_y
        else:
            # print("here1", new_center_x, -new_center_y)
            new_center_x = self.center_x - self.change_x + 2
            new_center_y = self.center_y - self.change_y + 2
            if self.check_x(new_center_x) and self.check_y(new_center_y):
                # print("here2", new_center_x, -new_center_y)
                self.center_x = new_center_x
                self.center_y = new_center_y
            # else:
            #     # print("here3", new_center_x, -new_center_y)

        # Random 1 in 20 chance that we'll change from our old direction and
        # then re-aim toward the player
        if random.randrange(20) == 0:
            start_x = self.center_x
            start_y = self.center_y

            # Get the destination location for the bullet
            dest_x = player_sprite.center_x
            dest_y = player_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            self.change_x = math.cos(angle) * 5
            self.change_y = math.sin(angle) * 5
            # time.sleep(1)

    def check_x(self, value):
        if 565 <= value <= 1285:
            return True
        return False

    def check_y(self, value):
        if -604 <= value <= -84:
            return True
        return False
    

class Boss(arcade.Sprite):
    def __init__(self, x, y, health):
        super().__init__()

        # Dictionary to store health bar textures.
        self.health_bar_textures = {
            'full': arcade.make_soft_square_texture(5, arcade.color.GREEN, outer_alpha=255),
            'damaged': arcade.make_soft_square_texture(5, arcade.color.YELLOW, outer_alpha=255),
            'critical': arcade.make_soft_square_texture(5, arcade.color.RED, outer_alpha=255),
            'background': arcade.make_soft_square_texture(5, arcade.color.WHITE, outer_alpha=255),
            'outline': arcade.make_soft_square_texture(7, arcade.color.BLACK, outer_alpha=255)
            }
            
        # Load a right facing enemy, and a left facing enemy.
        texture = arcade.load_texture(BOSS_IMAGE, scale=0.3)
        self.textures.append(texture)
        texture = arcade.load_texture(BOSS_IMAGE, mirrored=True, scale=0.3)
        self.textures.append(texture)

        # By defalt, the enemy faces right.
        self.set_texture(settings.TEXTURE_RIGHT)
        
        self.health_max_x = 0
        self.max_health = -1
        self.health_bar_width = 200

        self.center_x = x
        self.center_y = y
        self.health = health

        if self.max_health == -1:
            self.max_health = health

        # Initialize variables to use when drawing the health bar sprites.
        self.health_x = self.center_x - 98 + (self.health/2)
        self.health_max_x = self.center_x - 98 + (200/2)
        self.health_y = self.center_y + 90

        # Health bar that changes colour.
        self.health_sprite = arcade.Sprite()
        self.health_sprite.append_texture(self.health_bar_textures.get("full"))
        self.health_sprite.append_texture(self.health_bar_textures.get("damaged"))
        self.health_sprite.append_texture(self.health_bar_textures.get("critical"))
        self.health_sprite.set_texture(0)
        self.health_sprite.center_x = self.health_x
        self.health_sprite.center_y = self.health_y

        # Outline of health bar.
        self.health_outline_sprite = arcade.Sprite()
        self.health_outline_sprite.append_texture(self.health_bar_textures.get("outline"))
        self.health_outline_sprite.set_texture(0)
        self.health_outline_sprite.center_x = self.health_max_x
        self.health_outline_sprite.center_y = self.health_y
        self.health_outline_sprite.width = self.health_bar_width
        
        # Background of health bar.
        self.health_background_sprite = arcade.Sprite()
        self.health_background_sprite.append_texture(self.health_bar_textures.get("background"))
        self.health_background_sprite.set_texture(0)
        self.health_background_sprite.center_x = self.health_max_x
        self.health_background_sprite.center_y = self.health_y
        self.health_background_sprite.width = self.health_bar_width - 2

    def update(self):
        self.health_x = self.center_x - 98 + (self.health/2)
        self.health_max_x = self.center_x - 98 + (200/2)
        self.health_y = self.center_y + 90

        # Check to see what colour the health bar should be based on
        # how much health the enemy has.
        if self.health > self.max_health * 2/3:
            self.health_sprite.set_texture(0)
        elif self.health > self.max_health * 1/3:
            self.health_sprite.set_texture(1)
        else:
            self.health_sprite.set_texture(2)

        # Update the position of the health bars
        self.health_sprite.center_x = self.health_x
        self.health_sprite.center_y = self.health_y
        self.health_outline_sprite.center_x = self.health_max_x
        self.health_outline_sprite.center_y = self.health_y
        self.health_background_sprite.center_x = self.health_max_x
        self.health_background_sprite.center_y = self.health_y

        self.health_sprite.width = self.health

        if self.change_x < 0:
            self.set_texture(settings.TEXTURE_LEFT)
        if self.change_x > 0:
            self.set_texture(settings.TEXTURE_RIGHT)

        def disappear(self):
            pass



class AlexMenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.SAND_DUNE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("The Sand Temple", settings.WIDTH/2, settings.HEIGHT/2 + 150,
                         arcade.color.DARK_GRAY, font_size=40, anchor_x="center", font_name=ARCADE_FONT)
        arcade.draw_text("Press P to play.", settings.WIDTH/2, settings.HEIGHT/2 + 25,
                         arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Press I for instructions.", settings.WIDTH/2, settings.HEIGHT/2 - 50,
                         arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Press N for the next game.", settings.WIDTH/2, settings.HEIGHT/2 - 125,
                         arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Main Menu", settings.WIDTH/2, settings.HEIGHT/2 - 250,
                         arcade.color.BLACK, font_size=10, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.P:
            game_view = AlexGameView()
            game_view.director = self.director
            self.window.show_view(game_view)
        elif key == arcade.key.I:
            instructions_view = AlexInstructionView()
            instructions_view.director = self.director
            self.window.show_view(instructions_view)
        elif key == arcade.key.N:
            self.director.next_view()


class AlexInstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.SAND)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("How to Play?", settings.WIDTH/2, settings.HEIGHT/2 + 150,
                         arcade.color.BLACK, font_size=35, anchor_x="center", font_name=ARCADE_FONT)
        arcade.draw_text("Gameplay: Use AWSD or the arrow keys to move around and click to shoot.",
                         settings.WIDTH/2, settings.HEIGHT/2 + 75, arcade.color.BLACK, font_size=18,
                         anchor_x="center")
        arcade.draw_text("Goal: Find your way through the maze. Collect the gems along the way.",
                         settings.WIDTH/2, settings.HEIGHT/2 + 25, arcade.color.BLACK, font_size=18,
                         anchor_x="center")
        arcade.draw_text("Once you reach the end of the maze, fight the sand enemies and the sand boss.",
                         settings.WIDTH/2, settings.HEIGHT/2 - 25, arcade.color.BLACK, font_size=18,
                         anchor_x="center")
        arcade.draw_text("Kill the sand boss to obtain a key and progress to the next adventure!",
                         settings.WIDTH/2, settings.HEIGHT/2 - 75, arcade.color.BLACK, font_size=18,
                         anchor_x="center")
        arcade.draw_text("Press ESCAPE to go back to menu.", settings.WIDTH/2, settings.HEIGHT/2 - 175,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Instructions", settings.WIDTH/2, settings.HEIGHT/2 - 250,
                         arcade.color.BLACK, font_size=10, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = AlexMenuView()
            menu_view.director = self.director
            self.window.show_view(menu_view)


class AlexGameView(arcade.View):
    def __init__(self):
        """ Set up of the game and initialization of the variables. """

        super().__init__()

        # Set the working directory
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Set up the player info
        self.player_sprite = None
        self.player_health = 60

        # Initialize the viewport bottom and left variables
        self.view_bottom = 0
        self.view_left = 0

        # Set up collected gems info
        self.collected = 0
        self.collected_text = None
        self.green_gem_collected = False
        self.blue_gem_collected = False
        self.red_gem_collected = False

        # Set up frame count and game logic variables
        self.frame_count = 0
        self.last_hit = 0
        self.player_entered_boss_room = False
        self.door = True
        self.open_door = False
        self.door_closed = True
        self.is_in = False

        # Variables to hold sprite lists
        self.player_list = None
        self.wall_list = None
        self.gem_list = None
        self.bullet_list = None
        self.boss_bullets_list = None
        self.enemy_list = None
        self.boss_list = None
        self.key_list = None
        self.health_bar_list = None
        self.gem_display_list = None

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(is_static=False)
        self.gem_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.boss_bullets_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.boss_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()
        self.health_bar_list = arcade.SpriteList()
        self.gem_display_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player()
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 40
        self.player_list.append(self.player_sprite)

    def on_show(self):
        global completed

        completed = False

        # Add the enemies
        self.add_enemy(800, -400)

        # Add the boss
        self.add_boss(1000, -500)

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
                    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

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
        list_of_gem_types = [GEM_GREEN_IMAGE, GEM_BLUE_IMAGE, GEM_RED_IMAGE]
        list_of_gem_coordinates = [(195, 490), (255, 812), (450, 490), (894, 683),
                                   (835, 363), (1220, 938), (1345, 612), (1608, 235),
                                   (1276, 363), (1665, 683)]

        self.add_gem(GEM_GREEN_IMAGE, 200, 40)

        # for gem_type in list_of_gem_types:
        #     coordinates = list_of_gem_coordinates[random.randrange(len(list_of_gem_coordinates))]
        #     x = coordinates[0]
        #     y = coordinates[1]
        #     self.add_gem(gem_type, x, y)
        #     list_of_gem_coordinates.remove((x, y))

        # Creating boss bullet texture
        self.boss_bullets_texture = arcade.make_soft_circle_texture(10, 
                         arcade.color.RED, outer_alpha=255)

        # Physics engine so player can't go through walls
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        # Setting the background
        arcade.set_background_color(arcade.color.CADMIUM_ORANGE)

    def on_draw(self):
        arcade.start_render()
        # Draw all the sprites.
        self.wall_list.draw()
        self.player_list.draw()
        self.gem_list.draw()
        self.bullet_list.draw()
        self.boss_bullets_list.draw()
        self.enemy_list.draw()
        self.boss_list.draw()
        self.key_list.draw()

        # Draw the health bars
        self.health_bars(self.player_health, self.enemy_list, self.boss_sprite.health)

        # Drawing the collected gems text in bottom left corner
        output = f"Gems collected: {self.collected}/3"
        arcade.draw_text(output, 10 + self.view_left, 20 + self.view_bottom, arcade.color.BLACK, 14)

    def on_update(self, delta_time):
        global completed

        """ Movement and game logic """

        # Increase frame count when player enters room
        # Used to keep track of time for timed events
        if self.player_entered_boss_room == True:
            self.frame_count += 1

        if self.door:
            self.block = self.add_boundary(576, -24)
            self.door = False

        if self.collected == 1 and self.door_closed:
            self.open_door = True
            self.door_closed = False

        if self.open_door:
            self.wall_list.remove(self.block)
            self.open_door = False

        # To determine if player entered boss room
        if self.player_sprite.center_y < -90  and not self.is_in:
            self.player_entered_boss_room = True
            self.door = True
            self.is_in = True

        # Call an update on all sprites
        self.physics_engine.update()
        self.player_sprite.update()
        self.bullet_list.update()
        self.boss_bullets_list.update()
        self.wall_list.update()
        self.gem_list.update()
        self.enemy_list.update()
        self.boss_list.update()
        self.health_bar_list.update()

        # Check if player collects a gem
        gem_collected = arcade.check_for_collision_with_list(self.player_sprite, self.gem_list)
        for gem in gem_collected:
            gem.remove_from_sprite_lists()
            self.collected += 1

        # Check if bullets hit something
        for bullet in self.bullet_list:
            # Check this bullet to see if it hit a wall
            disappear_list = arcade.check_for_collision_with_list(bullet, self.wall_list)
            # If it did, get rid of the bullet
            if len(disappear_list) > 0:
                bullet.remove_from_sprite_lists()

            # Check this bullet to see if it hit an enemy
            enemy_hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            # If it did, get rid of bullet
            if len(enemy_hit_list) > 0:
                bullet.remove_from_sprite_lists()
            
            # If hit, the enemy loses health
            for enemy in enemy_hit_list:
                enemy.health -= 25
                if enemy.health <= 0:
                    enemy.remove_from_sprite_lists()
                    enemy.health_outline_sprite.remove_from_sprite_lists()
                    enemy.health_background_sprite.remove_from_sprite_lists()
                    enemy.health_sprite.remove_from_sprite_lists()

            # Check this bullet to see if it hit the boss
            boss_hit_list = arcade.check_for_collision_with_list(bullet, self.boss_list)
            # If it did, get rid of bullet
            if len(boss_hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # If hit, the boss loses health
            for boss in boss_hit_list:
                boss.health -= 25
                if boss.health <= 0:
                    boss.remove_from_sprite_lists()
                    boss.health_outline_sprite.remove_from_sprite_lists()
                    boss.health_background_sprite.remove_from_sprite_lists()
                    boss.health_sprite.remove_from_sprite_lists()

                    # Once boss is dead, key appears
                    key_sprite = arcade.Sprite(KEY_IMAGE)
                    key_sprite.center_x = self.boss_sprite.center_x
                    key_sprite.center_y = self.boss_sprite.center_y
                    self.key_list.append(key_sprite)

        # If the player entered boss room:
        # The enemies start to move
        # The boss starts to shoot
        if self.player_entered_boss_room:
           
            for enemy in self.enemy_list:
                # Called so enemy follows the player
                enemy.follow_player(self.player_sprite)

                # Check this enemy to see if it hit the player
                player_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
                
                # If it did, player loses health
                # Enemy dies and dissapears
                if len(player_hit_list) > 0:
                    self.player_health -= 10
                    enemy.remove_from_sprite_lists()
                    enemy.health_outline_sprite.remove_from_sprite_lists()
                    enemy.health_background_sprite.remove_from_sprite_lists()
                    enemy.health_sprite.remove_from_sprite_lists()

            # Boss aims and shoots at player
            for boss in self.boss_list:               

                # A 1 in 50 chance that the boss shoots
                if random.randrange(50) == 0:
                    # Position the bullet at the player's current location
                    start_x = boss.center_x
                    start_y = boss.center_y

                    # Get from the player the destination location for the bullet
                    final_x = self.player_sprite.center_x
                    final_y = self.player_sprite.center_y

                    # Get from the mouse the destination location for the bullet
                    dist_x = final_x - start_x
                    dist_y = final_y - start_y
                    angle = math.atan2(dist_y, dist_x)

                    # Creating the bullet
                    boss_bullets = arcade.Sprite()
                    boss_bullets.texture = self.boss_bullets_texture
                    boss_bullets_speed = 5
                    boss_bullets.width = 30
                    boss_bullets.center_x = start_x
                    boss_bullets.center_y = start_y

                    # Tilting the bullet based on angle
                    boss_bullets.angle = math.degrees(angle)

                    # Math for the trajectory of the bullet
                    boss_bullets.change_x = math.cos(angle) * boss_bullets_speed
                    boss_bullets.change_y = math.sin(angle) * boss_bullets_speed
                    self.boss_bullets_list.append(boss_bullets)

                # Check to see if player hit the boss
                boss_hit_player = boss.collides_with_sprite(self.player_sprite)

                # Every 30 frames, player loses health if it hit boss
                if self.frame_count >= self.last_hit + 30:
                    if boss_hit_player:
                        self.player_health -= 10
                        self.last_hit = self.frame_count

            # Check if boss bullets hit something
            for bullet in self.boss_bullets_list:
                # Check this bullet to see if it hit a wall
                disappear_list = arcade.check_for_collision_with_list(bullet, self.wall_list)
                # If it did, get rid of the bullet
                if len(disappear_list) > 0:
                    bullet.remove_from_sprite_lists()

                # Check this bullet to see if it hit the player
                player_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.boss_bullets_list)

                # If it did, get rid of bullet
                # Player loses health
                if len(player_hit_list) > 0:
                    self.player_health -= 10
                    bullet.remove_from_sprite_lists()
        
        # Check if player is dead
        if self.player_health <= 0:
            # If player is dead, remove player
            self.player_sprite.remove_from_sprite_lists()

            # Show game over view
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)

        # Check if player collected the key
        key_collected = arcade.check_for_collision_with_list(self.player_sprite, self.key_list)

        # If player did, game is completed
        for key in key_collected:
            key.remove_from_sprite_lists()
            completed = True

        # Check if the game is completed
        if completed:
            # Show game completed view
            game_completed_view = GameCompletedView()
            game_completed_view.director = self.director
            self.window.show_view(game_completed_view)

        # Called to manage screen scrolling
        self.manage_scrolling()

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
        
        elif key == arcade.key.ESCAPE:
            # Pass self, the current view, to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)

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
        bullet = arcade.Sprite(BULLET_IMAGE, 0.15)

        # Position the bullet at the player's current location
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        # Get from the mouse the destination location for the bullet
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

        # calculate our change_x and change_y
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)

    def health_bars(self, player_health, enemy_list, boss_health):

        player_x = self.player_sprite.center_x - 30 + (player_health/2)
        player_constant_x = self.player_sprite.center_x - 30 + (60/2)
        player_y = self.player_sprite.center_y + 40

        if player_health > 45:
            player_health_colour = arcade.color.GREEN
        elif player_health > 30:
            player_health_colour = arcade.color.YELLOW
        else:
            player_health_colour = arcade.color.RED

        # Player Health Bar
        self.draw_player_health_bar(player_constant_x, player_y, player_x, player_health, player_health_colour)
        
        self.health_bar_list.draw()

    def draw_player_health_bar(self, player_constant_x, player_y, player_x, player_health, player_health_colour):
        arcade.draw_rectangle_filled(player_constant_x, player_y, 60, 5, arcade.color.WHITE)
        arcade.draw_rectangle_filled(player_x, player_y, player_health, 5, player_health_colour)
        arcade.draw_rectangle_outline(player_constant_x, player_y, 61, 6, arcade.color.BLACK)

    def add_gem(self, gem_type, x, y):
        gem = arcade.Sprite(gem_type, 0.75)
        gem.center_x = x
        gem.center_y = y
        self.gem_list.append(gem)

    def add_enemy(self, x, y):
        self.enemy_sprite = Enemy(x, y, 75)
        self.enemy_list.append(self.enemy_sprite)
        self.health_bar_list.append(self.enemy_sprite.health_outline_sprite)
        self.health_bar_list.append(self.enemy_sprite.health_background_sprite)
        self.health_bar_list.append(self.enemy_sprite.health_sprite)

    def add_boss(self, x, y):
        self.boss_sprite = Boss(x, y, 200)
        self.boss_list.append(self.boss_sprite)
        self.health_bar_list.append(self.boss_sprite.health_outline_sprite)
        self.health_bar_list.append(self.boss_sprite.health_background_sprite)
        self.health_bar_list.append(self.boss_sprite.health_sprite)

    def add_boundary(self, x, y) -> arcade.Sprite:
        wall = arcade.Sprite(WALL_IMAGE, WALL_SPRITE_SCALING)
        wall.center_x = x
        wall.center_y = y
        self.wall_list.append(wall)
        return wall
    
    def manage_scrolling(self):
        global completed

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
            if completed is True:
                self.view_bottom = 0
                self.view_left = 0
            
            arcade.set_viewport(self.view_left,
                                settings.WIDTH + self.view_left - 1,
                                self.view_bottom,
                                settings.HEIGHT + self.view_bottom - 1)


class PauseView(arcade.View):
    def __init__(self, alex_game_view):
        super().__init__()
        self.alex_game_view = alex_game_view

    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE)

    def on_draw(self):
        arcade.start_render()

        # Draw player, for effect, on pause screen.
        # The previous View (GameView) was passed in
        # and saved in self.game_view.
        player_sprite = self.alex_game_view.player_sprite
        player_sprite.draw()

        # draw an orange filter over him
        arcade.draw_lrtb_rectangle_filled(left=player_sprite.left,
                                          right=player_sprite.right,
                                          top=player_sprite.top,
                                          bottom=player_sprite.bottom,
                                          color=arcade.color.ORANGE + (200,))

        arcade.draw_text("PAUSED", settings.WIDTH/2, settings.HEIGHT/2+50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Press Esc. to return",
                         settings.WIDTH/2,
                         settings.HEIGHT/2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Press Enter to reset",
                         settings.WIDTH/2,
                         settings.HEIGHT/2-30,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.alex_game_view)
        elif key == arcade.key.ENTER:  # reset game
            game_view = AlexGameView()
            self.window.show_view(game_view)


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.view_left = 0
        self.view_bottom = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        """
        Draw "Game over" across the screen.
        """
        arcade.draw_text("Game Over", 240, 400, arcade.color.WHITE, 54)
        arcade.draw_text("Press R to restart", 310, 300, arcade.color.WHITE, 24)
        arcade.set_viewport(self.view_left,
            settings.WIDTH + self.view_left - 1,
            self.view_bottom,
            settings.HEIGHT + self.view_bottom - 1)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            game_view = AlexGameView()
            self.window.show_view(game_view)


class GameCompletedView(arcade.View):
    def __init__(self):
        super().__init__()
        self.view_left = 0
        self.view_right = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.YELLOW)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("YOU WIN!", 240, 400, arcade.color.WHITE, 54)
        arcade.draw_text("Press ENTER to go back to main menu.", 310, 300, arcade.color.WHITE, 24)
        arcade.set_viewport(self.view_left,
            settings.WIDTH + self.view_left - 1,
            self.view_bottom,
            settings.HEIGHT + self.view_bottom - 1)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.director.next_view()


if __name__ == "__main__":
    # """This section of code will allow you to run your View
    # independently from the main.py file and its Director.

    # You can ignore this whole section. Keep it at the bottom
    # of your code.
    # It is advised you do not modify it unless you really know
    # what you are doing.
    # """
    from utils import FakeDirector
    window = arcade.Window(settings.WIDTH, settings.HEIGHT, title=settings.TITLE)
    my_view = AlexMenuView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
