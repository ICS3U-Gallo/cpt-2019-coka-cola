import arcade
import settings
import random
import os
import math

WIDTH = 800
HEIGHT = 600
GRAVITY = 1
PLAYER_JUMP_SPEED = 15
PLAYER_HEALTH = 2
VIEWPORT_MARGIN = 600
BULLET_SPEED = 11
PLAYER_SPEED = 10

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Load a left facing texture and a right facing texture.
        texture = arcade.load_texture("assets/indiana_jones.png", mirrored=True, scale=0.45)
        self.textures.append(texture)
        texture = arcade.load_texture("assets/indiana_jones.png", scale=0.45)
        self.textures.append(texture)

        # By default, face right.
        self.set_texture(settings.TEXTURE_RIGHT)

    def update(self):
        # Check if player should face left or right
        if self.change_x < 0:
            self.set_texture(settings.TEXTURE_LEFT)
        if self.change_x > 0:
            self.set_texture(settings.TEXTURE_RIGHT)

class KevinMenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Welcome to Kevin's Minigame!", settings.WIDTH/2, settings.HEIGHT//(3/2),
                         arcade.color.BLACK, font_size=40, anchor_x="center")
        arcade.draw_text("Press SPACE to Continue", settings.WIDTH/2, settings.HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            instruction_view = KevinInstructionView()
            self.window.show_view(instruction_view)


class KevinInstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("How to Play:", settings.WIDTH/2, 500,
                         arcade.color.BLACK, font_size=40, anchor_x="center")
        arcade.draw_text("Dodge all the obstacles", settings.WIDTH/2, settings.HEIGHT/2 + 100,
                         arcade.color.BLACK, font_size=18, anchor_x="center")
        arcade.draw_text("Find the key and open the door", settings.WIDTH/2, settings.HEIGHT/2 + 50,
                         arcade.color.BLACK, font_size=18, anchor_x="center")
        arcade.draw_text("there MIGHT be an easter egg", settings.WIDTH/2, settings.HEIGHT/2,
                         arcade.color.BLACK, font_size=18, anchor_x="center")
        arcade.draw_text("Good Luck!", settings.WIDTH/2, settings.HEIGHT/2 - 50,
                         arcade.color.BLACK, font_size=18, anchor_x="center")
        arcade.draw_text("Click SPACE to Start", settings.WIDTH/2, settings.HEIGHT/2-150,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = KevinView()
        self.window.show_view(game_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            game_view = KevinView()
            self.window.show_view(game_view)

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
        self.boss_list = None
        self.BEEMOVE = 7
        self.shipmove = 9
        self.boundary = 200
        self.hasjet = False
        self.key_list = None
        self.bullet_list = None
        self.jetpack_list = None
        self.egg_list = None
        # Separate variable that holds the player sprite
        self.frame_count = 0
        self.haskey = False
        self.keymove = 0
        self.finish_list = None
        self.physics_engine = None
        self.invincible = False
        # self.player = arcade.Sprite(center_x=WIDTH//2, center_y=100)
        
        
        
        

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
        self.boss_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()
        self.jetpack_list = arcade.SpriteList()
        self.egg_list = arcade.SpriteList()

        #add egg
        self.egg = arcade.Sprite("assets/easteregg.png", 0.1)
        self.egg.center_x = -5500
        self.egg.center_y = 140
        self.egg_list.append(self.egg)
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

        

        #boss
        boss = arcade.Sprite("assets/ufoboss.png", 0.5)
        boss.center_x = -700
        boss.center_y = 100
        self.boss_list.append(boss)

        #slime
        self.slime = arcade.Sprite(":resources:images/enemies/slimePurple.png", 1)
        self.slime.center_x = 3500
        self.slime.center_y = 135
        self.obstacles_list.append(self.slime)
        
        #bee
        self.bee = arcade.Sprite(":resources:images/enemies/saw.png", 0.7)
        self.bee.center_x = 4000
        self.bee.center_y = 225
        self.obstacles_list.append(self.bee)
        
        #flag
        self.flag = arcade.Sprite(":resources:images/items/flagGreen1.png", 0.8)
        self.flag.center_x = 400
        self.flag.center_y = 135
        
        # self.player.texture = arcade.make_soft_square_texture(50, arcade.color.BLUE, outer_alpha=255)
        self.player_sprite = Player()
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 135
        self.player_list.append(self.player_sprite)
        #troll
        for x in range(-6000, -5000, 100):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 1)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)
        #troll
        for x in range (-3000, -2000, 100):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 1)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)
        for x in range (-100, 3000, 100):
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

        ycor2 = 150
        for x in range(-2000, -1000, 300):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 0.7)
            wall.center_x = x
            wall.center_y = ycor2
            ycor2 += 50
            self.wall_list.append(wall)
        ycor2 = 250
        for x in range(-900, -100, 300):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 0.7)
            wall.center_x = x
            wall.center_y = ycor2
            ycor2 -= 50
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

        #troll
        self.jetpack = arcade.Sprite("assets/jetpack.png", 0.03)
        self.jetpack.center_x = -2900
        self.jetpack.center_y = 150
        self.jetpack_list.append(self.jetpack)


        self.key = arcade.Sprite(":resources:images/items/keyYellow.png", 0.5)
        self.key.center_x = -2300
        self.key.center_y = 200
        self.key_list.append(self.key)

        
        self.finish_list.append(door_bot)
        self.finish_list.append(door_top)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)

    def on_draw(self):
        arcade.start_render()
        self.egg_list.draw()
        self.boss_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.flag.draw()
        self.finish_list.draw()
        self.obstacles_list.draw()
        self.player_list.draw()
        self.wall_list.draw()
        self.key_list.draw()

        self.jetpack_list.draw()
        # Draw everything below here.
        
    
    def update(self, delta_time):
        self.physics_engine.update()
        self.player_sprite.update()
        if self.haskey == True:
            self.key.center_x = self.player_sprite.center_x
            self.key.center_y = self.player_sprite.center_y + 70
        if self.hasjet == True:
            self.jetpack.center_x = self.player_sprite.center_x
            self.jetpack.center_y = self.player_sprite.center_y
        if self.slime.center_x > 0:
            self.slime.center_x -= 7
        self.bee.center_x -= self.BEEMOVE
        if self.bee.center_x < self.player_sprite.center_x - 150:
            self.BEEMOVE = -15

        for egg in self.egg_list:
            egg_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.egg_list)
            if len(egg_hit_list) > 0:
                self.invincible = True
                
        if self.invincible == True:
            self.egg.center_x = self.player_sprite.center_x
            self.egg.center_y = self.player_sprite.center_y
        #check if invincible
        if self.invincible == False:
            for obstacle in self.obstacles_list:
                obstacle_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.obstacles_list)
                if len(obstacle_hit_list) > 0:
                    self.view_left = 5
                    self.player_sprite.center_x = 50
                    self.slime.center_x = 3500
                    self.bee.center_x = 4000
                    self.BEEMOVE = 7
                    

            for key in self.key_list:
                key_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.key_list)
                if len(key_hit_list) > 0:
                    
                    self.haskey = True
            for jet in self.jetpack_list:
                jet_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.jetpack_list)
                if len(jet_hit_list) > 0:
                    self.hasjet = True
        
            
            self.frame_count += 1
            for enemy in self.enemy_list:

                
                if self.frame_count % 35 == 0:
                    self.shipangle = random.randrange(220, 300)
                    bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")
                    bullet.center_x = enemy.center_x
                    
                    bullet.angle = -90
                    bullet.change_y = -BULLET_SPEED
                    bullet.top = enemy.bottom
                    
                    self.bullet_list.append(bullet)

            
            for boss in self.boss_list:

                start_x = boss.center_x
                start_y = boss.center_y

                dest_x = self.player_sprite.center_x
                dest_y = self.player_sprite.center_y

                x_diff = dest_x - start_x
                y_diff = dest_y - start_y
                angle = math.atan2(y_diff, x_diff)

                
                # Shoot every 60 frames change of shooting each frame
                if self.frame_count % 40 == 0 and self.player_sprite.center_x < 0:
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
                    
            for bullet in self.bullet_list:
                if bullet.center_y < 0:
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
        for finish in self.finish_list:
            finish_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.finish_list)
            if len(finish_hit_list) > 0 and self.haskey == True:
                self.director.next_view()
                
        if self.player_sprite.center_y < 50:
                self.view_left = 5
                self.player_sprite.center_x = 50
                self.player_sprite.center_y = 135
                self.slime.center_x = 3500
                self.bee.center_x = 4000
                self.BEEMOVE = 7
                
        if self.player_sprite.center_x > 50:
            self.boundary = 0
        else:
            self.boundary = 200

         # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN 
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + WIDTH - VIEWPORT_MARGIN + self.boundary
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
        if key == arcade.key.SPACE or key == arcade.key.W or key == arcade.key.UP:
            if self.hasjet == True and self.player_sprite.center_x < 0:
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
            else:
                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
                
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -10
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 10
        elif key == arcade.key.CAPSLOCK and key == arcade.key.RIGHT:
            self.player_sprite.change_x = 20

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
        
        pass
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
    my_view = KevinMenuView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
    # main()


