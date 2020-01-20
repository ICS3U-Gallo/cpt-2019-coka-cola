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
BULLET_SPEED = 50

class OwenMenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("WELCOME TO FLAPPY JONES!", settings.WIDTH/2, 
                         settings.HEIGHT//(3/2),
                         arcade.color.BLACK, font_size=40, anchor_x="center")

        arcade.draw_text("Press SPACE to Continue", settings.WIDTH/2, 
                         settings.HEIGHT/2-75, arcade.color.YANKEES_BLUE, 
                         font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            instruction_view = OwenInstructionView()
            self.window.show_view(instruction_view)

class OwenInstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("How to Play?", settings.WIDTH/2, 500,
                         arcade.color.BLACK, font_size=40, anchor_x="center")
        arcade.draw_text("Gameplay: Use the mouse to move around and click to shoot.", settings.WIDTH/2, 450,
                         arcade.color.BLACK, font_size=18, anchor_x="center")
        arcade.draw_text("Goal: You have 3 lives. Shoot to destroy all the rocks, monkeys and kill", settings.WIDTH/2, settings.HEIGHT/2 + 50,
                         arcade.color.BLACK, font_size=18, anchor_x="center")
        arcade.draw_text("the jungle monster to obtain a key to advance to the next level.", settings.WIDTH/2, settings.HEIGHT/2,
                         arcade.color.BLACK, font_size=18, anchor_x="center")
        arcade.draw_text("Be Careful! If any of them touch you or leave the screen, you will lose a life.", settings.WIDTH/2, settings.HEIGHT/2 - 50,
                         arcade.color.BLACK, font_size=18, anchor_x="center")
        arcade.draw_text("Good Luck!", settings.WIDTH/2, settings.HEIGHT/2 - 100,
                         arcade.color.BLACK, font_size=18, anchor_x="center")
        arcade.draw_text("Click SPACE to Start", settings.WIDTH/2, settings.HEIGHT/2-200,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = OwenGameView()
        self.window.show_view(game_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            game_view = OwenGameView()
            self.window.show_view(game_view)

class OwenGameView(arcade.View):

    def __init__(self):
        super().__init__()
    
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.player_list = None
        self.coin_list = None
        self.wall_list = None
        self.background = None
        self.view_bottom = 0
        self.view_left = 0
        self.frame_count = 0


    def on_show(self):
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        arcade.set_background_color(arcade.color.CADMIUM_ORANGE)

        self.player_sprite = arcade.Sprite("assets/indiana_jones.png", 0.3)
        self.player_sprite.center_x = 64 
        self.player_sprite.center_y = 500
        self.player_list.append(self.player_sprite) 

        for x in range(0, 1850, 64):
            wall = arcade.Sprite("assets/rock.png", 0.1)
            wall.center_x = x
            wall.center_y = 0
            self.wall_list.append(wall)
        
        for x in range(0, 1850, 64): 
            wall = arcade.Sprite("assets/rock.png", 0.1)
            wall.center_x = x
            wall.center_y = 1035
            self.wall_list.append(wall)

        for y in range(0, 1035, 64):
            wall = arcade.Sprite("assets/rock.png", 0.1)
            wall.center_x = 1863
            wall.center_y = y
            self.wall_list.append(wall)

        for y in range(0, 1035, 64):
            wall = arcade.Sprite("assets/rock.png", 0.1)
            wall.center_x = -70
            wall.center_y = y
            self.wall_list.append(wall)

        for x in range(200, 1650, 400):
            for y in range(69, 1000, 64):
                if random.randrange(5) > 0:
                    wall = arcade.Sprite("assets/rock.png", 0.1)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        arcade.set_background_color(arcade.color.YELLOW_ORANGE)

        self.view_left = 0
        self.view_bottom = 0

        self.enemy1 = arcade.Sprite("assets/sand_worm.png", 0.3)
        self.enemy1.center_x = 390
        self.enemy1.center_y = 967
        self.enemy1.angle = 180
        self.enemy_list.append(self.enemy1)

        self.enemy2 = arcade.Sprite("assets/sand_worm.png", 0.3)
        self.enemy2.center_x = 780
        self.enemy2.center_y = 70
        self.enemy2.angle = 0
        self.enemy_list.append(self.enemy2)

        self.enemy3 = arcade.Sprite("assets/sand_worm.png", 0.3)
        self.enemy3.center_x = 1190
        self.enemy3.center_y = 967
        self.enemy3.angle = 180
        self.enemy_list.append(self.enemy3)

    def on_draw(self):
        arcade.start_render()

        self.player_sprite.draw()
        self.wall_list.draw()
        self.key_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw() 



    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):

        self.physics_engine.update()

        changed = False

        self.frame_count += 1
        
        key_sprite = arcade.Sprite("assets/key.png")
        key_sprite.center_x = 1650
        key_sprite.center_y = 500
        self.key_list.append(key_sprite)

        for enemy in self.enemy_list:
            if self.frame_count % 100 == 0:
                if enemy == self.enemy1:
                    bullet = arcade.Sprite("assets/bullet.png", 0.3)
                    bullet.center_x = enemy.center_x
                    bullet.angle = -90
                    bullet.top = enemy.bottom
                    bullet.change_y = -2
                    self.bullet_list.append(bullet)
                if enemy == self.enemy2:
                    bullet = arcade.Sprite("assets/bullet.png", 0.3)
                    bullet.center_x = enemy.center_x
                    bullet.angle = 450
                    bullet.top = enemy.bottom
                    bullet.change_y = 2
                    self.bullet_list.append(bullet)
                if enemy == self.enemy3:
                    bullet = arcade.Sprite("assets/bullet.png", 0.3)
                    bullet.center_x = enemy.center_x
                    bullet.angle = -90
                    bullet.top = enemy.bottom
                    bullet.change_y = -2
                    self.bullet_list.append(bullet)
        
        for bullet in self.bullet_list:
            if bullet.top < 30:
                bullet.remove_from_sprite_lists()
            if bullet.top > 990:
                bullet.remove_from_sprite_lists()
        
        self.bullet_list.update()

        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left - 1,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom - 1)        

        key_collected = arcade.check_for_collision_with_list(self.player, self.key_list)
        for key in key_collected: 
            key.remove_from_sprite_lists()
            completed = True

        if completed:
            game_completed_view = GameCompletedView()
            game_completed_view.director = self.director
            self.window.show_view(game_completed_view)

        for bullet in self.bullet_list:
            bullet_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.bullet_list)
            if len(bullet_hit_list) > 0:
                self.view_left = 5
                self.player_sprite.center_x = 50


class OwenInstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.YALE_BLUE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("How to Play?", settings.WIDTH/2, settings.HEIGHT/2 + 150,
                         arcade.color.BLACK, font_size=35, anchor_x="center")
        arcade.draw_text("Use the arrow keys to move around and dodge the bullets",
                         settings.WIDTH/2, settings.HEIGHT/2 + 75, arcade.color.BLACK, font_size=18,
                         anchor_x="center")
        arcade.draw_text("Get through all the enemies and walls to find your exit to the key.",
                         settings.WIDTH/2, settings.HEIGHT/2 + 25, arcade.color.BLACK, font_size=18,
                         anchor_x="center")
        arcade.draw_text("Beware! The bullets are dangerous and will send you back to spawn",
                         settings.WIDTH/2, settings.HEIGHT/2 - 25, arcade.color.BLACK, font_size=18,
                         anchor_x="center")
        arcade.draw_text("Get the key and move on to the next game! GOOD LUCK!!!",
                         settings.WIDTH/2, settings.HEIGHT/2 - 75, arcade.color.BLACK, font_size=18,
                         anchor_x="center")
        arcade.draw_text("Press ESCAPE to go back to menu.", settings.WIDTH/2, settings.HEIGHT/2 - 175,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Instructions", settings.WIDTH/2, settings.HEIGHT/2 - 250,
                         arcade.color.BLACK, font_size=10, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = OwenGameView()
        self.window.show_view(game_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            game_view = OwenGameView()
            self.window.show_view(game_view)

class GameCompletedView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.GOLDEN_POPPY)

        self.view_left = 0
        self.view_bottom = 0

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text("YOU WIN!", settings.WIDTH/2, 400, arcade.color.BLACK,
                         54, anchor_x="center")
        arcade.draw_text("Press ENTER to go to the next adventure.",
                         settings.WIDTH/2, settings.HEIGHT/2,
                         arcade.color.BLACK, 24, anchor_x="center")

        arcade.draw_text("Game Completed", settings.WIDTH/2,
                         settings.HEIGHT/2 - 250, arcade.color.BLACK,
                         font_size=10, anchor_x="center")

        arcade.set_viewport(self.view_left,
                            settings.WIDTH + self.view_left - 1,
                            self.view_bottom,
                            settings.HEIGHT + self.view_bottom - 1)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.director.next_view()


if __name__ == "__main__":
    from utils import FakeDirector
    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    my_view = OwenMenuView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
