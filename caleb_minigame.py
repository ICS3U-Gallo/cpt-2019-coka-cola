import arcade
import math
import random
import settings
import os


class CalebMenuView(arcade.View):
    # Set the background color
    def on_show(self):
        arcade.set_background_color(arcade.color.JUNGLE_GREEN)

    # Display text
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Welcome to Caleb's Minigame!", settings.WIDTH/2,
                         settings.HEIGHT//(3/2), arcade.color.BLACK,
                         font_size=42, anchor_x="center")

        arcade.draw_text("Press SPACE to Continue", settings.WIDTH/2,
                         settings.HEIGHT/2-125, arcade.color.WHITE_SMOKE,
                         font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        pass

    # If user presses space, go to instruction screen
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            instructions_view = CalebInstructionView()
            instructions_view.director = self.director
            self.window.show_view(instructions_view)


class CalebInstructionView(arcade.View):
    # Set background color
    def on_show(self):
        arcade.set_background_color(arcade.color.JUNGLE_GREEN)

    # Explain the rules and how to play
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("How to Play?", settings.WIDTH/2, 500,
                         arcade.color.BLACK, font_size=40, anchor_x="center")
        arcade.draw_text("Gameplay: Use the mouse to move around and click to\
 shoot.", settings.WIDTH/2, 425, arcade.color.BLACK, font_size=18,
                         anchor_x="center")
        arcade.draw_text("Goal: You have 3 lives. Shoot to destroy all the\
 rocks, monkeys and kill", settings.WIDTH/2, settings.HEIGHT/2 + 50,
                         arcade.color.BLACK, font_size=18, anchor_x="center")
        arcade.draw_text("the jungle monster to obtain a key to advance to the\
 next level.", settings.WIDTH/2, settings.HEIGHT/2, arcade.color.BLACK,
                         font_size=18, anchor_x="center")
        arcade.draw_text("Be Careful! If any of them touch you or leave the\
 screen, you will lose a life.", settings.WIDTH/2, settings.HEIGHT/2 - 50,
                         arcade.color.BLACK, font_size=18, anchor_x="center")
        arcade.draw_text("Good Luck!", settings.WIDTH/2,
                         settings.HEIGHT/2 - 100, arcade.color.BLACK,
                         font_size=18, anchor_x="center")
        arcade.draw_text("Press SPACE to Start", settings.WIDTH/2,
                         settings.HEIGHT/2-200, arcade.color.WHITE_SMOKE,
                         font_size=20, anchor_x="center")

    # If user presses space. go to the game
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            game_view = CalebGameView()
            game_view.director = self.director
            self.window.show_view(game_view)


class CalebGameView(arcade.View):
    def __init__(self):
        super().__init__()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Initialize the sprite lists
        self.player_list = None
        self.rocks_list = None
        self.monkeys_list = None
        self.banana_list = None
        self.bullets_list = None
        self.hearts_list = None
        self.jungle_monster_list = None
        self.jungle_bullets_list = None
        self.count = 0
        self.key_list = None

        self.player = None
        self.background = None

    def on_show(self):

        # Sprite Lists
        self.player_list = arcade.SpriteList()
        self.rocks_list = arcade.SpriteList()
        self.monkeys_list = arcade.SpriteList()
        self.banana_list = arcade.SpriteList()
        self.bullets_list = arcade.SpriteList()
        self.hearts_list = arcade.SpriteList()
        self.jungle_monster_list = arcade.SpriteList()
        self.jungle_bullets_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()

        # Set up the player
        self.player = arcade.Sprite("assets/indiana_jones.png", 0.5)
        self.player.center_x = 50
        self.player.center_y = 50
        self.player_list.append(self.player)

        # Set up Rocks
        self.rock_texture = arcade.make_soft_circle_texture(40,
                                                            arcade.color.
                                                            GRAY_BLUE,
                                                            outer_alpha=255)

        # Set up Bullets
        self.bullets_texture = arcade.make_soft_circle_texture(15,
                                                               arcade.color.
                                                               BLACK,
                                                               outer_alpha=255)

        # Put 3 hearts in the top left corner
        for x in range(50, 190, 60):
            heart = arcade.Sprite("assets/heart.png", 0.1)
            heart.center_y = 500
            heart.center_x = x
            self.hearts_list.append(heart)

        # Set up Time and Score
        self.total_time = 0.0
        self.score = 0

        # Setup the falling rocks
        for _ in range(30):
            rock = arcade.Sprite()
            rock.center_x = random.randrange(0, settings.WIDTH)
            rock.center_y = settings.HEIGHT + 200
            rock.texture = self.rock_texture
            rock.speed = random.randrange(30, 60)
            rock.angle = random.uniform(math.pi, math.pi * 2)
            self.rocks_list.append(rock)

        # Setup the falling monkeys
        for _ in range(18):
            monkey = arcade.Sprite("assets/monkey.png", 0.20)
            monkey.center_x = random.randrange(100, settings.WIDTH)
            monkey.center_y = settings.HEIGHT + 425
            monkey.speed_x = 50
            monkey.speed_y = random.randrange(20, 30)
            self.monkeys_list.append(monkey)

        # Setup the jungle boss
        for _ in range(1):
            jungle_monster = arcade.Sprite("assets/junglemonster.PNG")
            jungle_monster.center_x = 400
            jungle_monster.center_y = settings.HEIGHT + 480
            jungle_monster.speed_x = 0
            jungle_monster.speed_y = 12
            self.jungle_monster_list.append(jungle_monster)

        # Set up Jungle bullets
        self.jungle_bullets_texture = arcade.make_soft_circle_texture(
                                        10,
                                        arcade.color.GREEN,
                                        outer_alpha=255)

        # Import the jungle background
        self.background = arcade.load_texture("assets/jungle.PNG")

    def on_draw(self):
        # keep as first line
        arcade.start_render()

        arcade.draw_texture_rectangle(settings.WIDTH // 2,
                                      settings.HEIGHT // 2, settings.WIDTH,
                                      settings.HEIGHT, self.background)

        # Draw the sprites
        self.player.draw()
        self.rocks_list.draw()
        self.monkeys_list.draw()
        self.banana_list.draw()
        self.bullets_list.draw()
        self.hearts_list.draw()
        self.jungle_monster_list.draw()
        self.jungle_bullets_list.draw()
        self.key_list.draw()

        # Draw time
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        output = f"Time: {minutes:02d}:{seconds:02d}"
        arcade.draw_text(output, settings.WIDTH - 200, 50, arcade.color.WHITE,
                         30)

        # Draw score
        arcade.draw_text(f"Score: {self.score}", settings.WIDTH - 200,
                         settings.HEIGHT - 490, arcade.color.BLUE, 36)
        arcade.draw_text(f"Score: {self.score}", settings.WIDTH - 198,
                         settings.HEIGHT - 490, arcade.color.BABY_BLUE, 36)

    def update(self, delta_time):
        # Update the sprites
        self.rocks_list.update()
        self.bullets_list.update()
        self.banana_list.update()
        self.jungle_bullets_list.update()
        self.total_time += delta_time

        for rock in self.rocks_list:
            # Make rocks move
            rock.center_y -= rock.speed * delta_time
            bullets_hit_rock = rock.collides_with_list(self.bullets_list)
            rock_hit_player = rock.collides_with_sprite(self.player)

            # Get rid of rock and bullets when they collide
            if bullets_hit_rock:
                rock.kill()
                # Add 1 to score if rock is destroyed
                self.score += 1
                for bullet in bullets_hit_rock:
                    bullet.kill()

            # Get rid of a heart when rock collides with player, leaves screen
            if rock_hit_player or rock.center_y < 0:
                if len(self.hearts_list) is not 0:
                    heart = self.hearts_list[0]
                    self.hearts_list.remove(heart)
                    rock.kill()

        for monkey in self.monkeys_list:
            # Make monkeys move side to side
            monkey.center_x += monkey.speed_x * delta_time

            if monkey.center_x < 0:
                monkey.speed_x = 50
            elif monkey.center_x > 800:
                monkey.speed_x = -50

            # Make monkeys move down
            monkey.center_y -= monkey.speed_y * delta_time

            bullets_hit_monkey = monkey.collides_with_list(self.bullets_list)
            monkey_hit_player = monkey.collides_with_sprite(self.player)

            # Get rid of monkey and bullet when they collide
            if bullets_hit_monkey and monkey.center_y <= 600:
                monkey.kill()
                # Add 1 to score is monkey is killed
                self.score += 1
                for bullet in bullets_hit_monkey:
                    bullet.kill()

            # Get monkeys to shoot bananas
            if monkey.center_y < 600 and random.randrange(200) == 0:
                banana = arcade.Sprite("assets/banana.gif", 0.15)
                banana.center_x = monkey.center_x
                banana.angle = -90
                banana.top = monkey.bottom
                banana.change_y = -5
                self.banana_list.append(banana)

            # Get rid of a heart when a monkey collides with the player
            if monkey_hit_player or monkey.center_y < 0:
                if len(self.hearts_list) is not 0:
                    heart = self.hearts_list[0]
                    self.hearts_list.remove(heart)
                    monkey.kill()

        for banana in self.banana_list:
            banana_hit_player = banana.collides_with_sprite(self.player)

            # If the banana hits the player, the banana is removed
            if banana_hit_player:
                banana.kill()
                # Get rid of heart
                if len(self.hearts_list) is not 0:
                    heart = self.hearts_list[0]
                    self.hearts_list.remove(heart)

        # Get jungle monster to shoot at player
        for jungle_monster in self.jungle_monster_list:
            jungle_monster.center_y -= jungle_monster.speed_y * delta_time
            if jungle_monster.center_y < 700 and random.randrange(25) == 0:

                # Have the bullets start at the jungle monster
                start_x = jungle_monster.center_x
                start_y = jungle_monster.center_y

                # Have the bullets aim at the player
                final_x = self.player.center_x
                final_y = self.player.center_y

                # Calculate the distance to the player
                dist_x = final_x - start_x
                dist_y = final_y - start_y
                angle = math.atan2(dist_y, dist_x)

                # Set up the Jungle Bullets
                jungle_bullets = arcade.Sprite()
                jungle_bullets.texture = self.jungle_bullets_texture
                jungle_bullets_speed = 8
                jungle_bullets.width = 50
                jungle_bullets.center_x = start_x
                jungle_bullets.center_y = start_y

                jungle_bullets.angle = math.degrees(angle)

                # Set up the jungle bullets's speed
                jungle_bullets.change_x = math.cos(angle)*jungle_bullets_speed
                jungle_bullets.change_y = math.sin(angle)*jungle_bullets_speed
                self.jungle_bullets_list.append(jungle_bullets)

            # Player must hit the jungle monster 100 times to kill him
            bullets_hit_jungle_monster = jungle_monster.collides_with_list(
                                        self.bullets_list)

            if bullets_hit_jungle_monster and jungle_monster.center_y < 700:
                self.count += 1
                for bullet in bullets_hit_jungle_monster:
                    bullet.kill()
                    if self.count == 100:
                        jungle_monster.kill()
                        # When jungle monster is killed, show key
                        key_sprite = arcade.Sprite("assets/key.png")
                        key_sprite.center_x = jungle_monster.center_x
                        key_sprite.center_y = jungle_monster.center_y
                        self.key_list.append(key_sprite)

            # If player hits jungle monster, player loses lives
            jungle_monster_hit_player = jungle_monster.collides_with_sprite(
                                        self.player)

            if jungle_monster_hit_player or jungle_monster.center_y < 0:
                if len(self.hearts_list) is not 0:
                    heart = self.hearts_list[0]
                    self.hearts_list.remove(heart)

        # See if player got the key
        key_collected = arcade.check_for_collision_with_list(self.player,
                                                             self.key_list)
        for key in key_collected:
            key.remove_from_sprite_lists()
            completed = True

            # If player got the key, go to the game completed view
            if completed is True:
                game_completed_view = GameCompleteView()
                game_completed_view.director = self.director
                self.window.show_view(game_completed_view)

        # If jungle bullets hit player, remove a heart
        for jungle_bullets in self.jungle_bullets_list:
            jungle_bullets_hit_player = jungle_bullets.collides_with_sprite(
                                        self.player)

            if jungle_bullets_hit_player:
                if len(self.hearts_list) is not 0:
                    heart = self.hearts_list[0]
                    self.hearts_list.remove(heart)
                    jungle_bullets.kill()

        # If the player doesn't have any hearts left, they lose
        if len(self.hearts_list) == 0:
            game_over_view = GameOverView()
            game_over_view.director = self.director
            self.window.show_view(game_over_view)

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        # Restricts where the player can go
        self.player.center_x = x
        if y > 100:
            self.player.center_y = y
        else:
            self.player.center_y = 100

    def on_mouse_press(self, x, y, button, key_modifiers):
        # Setup the bullets and their properties
        bullet = arcade.Sprite()
        bullet.center_x = self.player.center_x
        bullet.center_y = self.player.center_y
        bullet.change_y = 5
        bullet.texture = self.bullets_texture
        bullet.width = 5

        self.bullets_list.append(bullet)


class GameOverView(arcade.View):
    # Set the background color

    def on_show(self):
        arcade.set_background_color(arcade.color.RED_DEVIL)

    def on_draw(self):
        arcade.start_render()

        # Draw Text
        arcade.draw_text("Game Over", 250, 400, arcade.color.WHITE, 54,)
        arcade.draw_text("Press R to Restart", 300, 200,
                         arcade.color.WHITE, 24)

    # If player presses R, the game restarts
    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            game_view = CalebGameView()
            game_view.director = self.director
            self.window.show_view(game_view)


class GameCompleteView(arcade.View):
    # Setup the background color

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        # Draw the text
        arcade.draw_text("Congratulations! Game Complete", 120, 400,
                         arcade.color.WHITE, font_size=35)
        arcade.draw_text("Press Space to Advance", 255, 200,
                         arcade.color.WHITE, font_size=24)

    # If player presses Space go to the next minigame
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.director.next_view()

if __name__ == "__main__":
    from utils import FakeDirector
    window = arcade.Window(settings.WIDTH, settings.HEIGHT,
                           title=settings.TITLE)
    my_view = CalebMenuView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
