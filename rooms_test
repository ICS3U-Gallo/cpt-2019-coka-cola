import arcade
import settings
import os

WALL_SPRITE_NATIVE_SIZE = 100
WALL_SPRITE_SCALING = 0.64
WALL_SPRITE_SIZE = int(WALL_SPRITE_NATIVE_SIZE * WALL_SPRITE_SCALING)


class Room:

    def __init__(self):
        # Variables to hold sprite lists
        self.wall_list = None
        self.gem_list = None
        self.bullet_list = None
        self.enemy_list = None
        self.boss_list = None

        # Background images
        self.background = None


def setup_lobby():
    room = Room()

    room.player_list = arcade.SpriteList()
    room.wall_list = arcade.SpriteList()
    room.gem_list = arcade.SpriteList()
    room.bullet_list = arcade.SpriteList()
    room.enemy_list = arcade.SpriteList()
    room.enemy_1_list = arcade.SpriteList()
    room.enemy_2_list = arcade.SpriteList()
    room.boss_list = arcade.SpriteList()

    for y in (0, settings.HEIGHT - WALL_SPRITE_SIZE):
        for x in range(-32, settings.WIDTH + 32, WALL_SPRITE_SIZE):
            wall = arcade.Sprite("assets/sandblock.png", WALL_SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    for x in (0, settings.WIDTH - WALL_SPRITE_SIZE):
        for y in range(WALL_SPRITE_SIZE, settings.HEIGHT - WALL_SPRITE_SIZE, WALL_SPRITE_SIZE):
            if (y != WALL_SPRITE_SIZE * 4 and y != WALL_SPRITE_SIZE * 5):
                wall = arcade.Sprite("assets/sandblock.png", WALL_SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    wall = arcade.Sprite("assets/sandblock.png", WALL_SPRITE_SCALING)
    wall.left = 5 * WALL_SPRITE_SIZE
    wall.bottom = 6 * WALL_SPRITE_SIZE
    room.wall_list.append(wall)

    room.background = arcade.load_texture("assets/sand_bkgd.jpg")

    return room


def setup_room_right():
    room = Room()

    room.player_list = arcade.SpriteList()
    room.wall_list = arcade.SpriteList()
    room.gem_list = arcade.SpriteList()
    room.bullet_list = arcade.SpriteList()
    room.enemy_list = arcade.SpriteList()
    room.enemy_1_list = arcade.SpriteList()
    room.enemy_2_list = arcade.SpriteList()
    room.boss_list = arcade.SpriteList()

    for y in (0, settings.HEIGHT - WALL_SPRITE_SIZE):
        for x in range(0, settings.WIDTH, WALL_SPRITE_SIZE):
            wall = arcade.Sprite("assets/sandblock.png", WALL_SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)
    
    for x in (0, settings.WIDTH - WALL_SPRITE_SIZE):
        for y in range(WALL_SPRITE_SIZE, settings.HEIGHT - WALL_SPRITE_SIZE, WALL_SPRITE_SIZE):
            if (y != WALL_SPRITE_SIZE * 4 and y != WALL_SPRITE_SIZE * 5) or x != 0:
                wall = arcade.Sprite("assets/sandblock.png", WALL_SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    wall = arcade.Sprite("assets/sandblock.png", WALL_SPRITE_SCALING)
    wall.left = 5 * WALL_SPRITE_SIZE
    wall.bottom = 6 * WALL_SPRITE_SIZE
    room.wall_list.append(wall)

    room.background = arcade.load_texture("assets/sand_bkgd.jpg")

    return room


def setup_room_left():
    room = Room()

    room.player_list = arcade.SpriteList()
    room.wall_list = arcade.SpriteList()
    room.gem_list = arcade.SpriteList()
    room.bullet_list = arcade.SpriteList()
    room.enemy_list = arcade.SpriteList()
    room.enemy_1_list = arcade.SpriteList()
    room.enemy_2_list = arcade.SpriteList()
    room.boss_list = arcade.SpriteList()

    for y in (0, settings.HEIGHT - WALL_SPRITE_SIZE):
        for x in range(0, settings.WIDTH, WALL_SPRITE_SIZE):
            wall = arcade.Sprite("assets/sandblock.png", WALL_SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)
    
    for x in (0, settings.WIDTH - WALL_SPRITE_SIZE):
        for y in range(WALL_SPRITE_SIZE, settings.HEIGHT - WALL_SPRITE_SIZE, WALL_SPRITE_SIZE):
            if (y != WALL_SPRITE_SIZE * 4 and y != WALL_SPRITE_SIZE * 5) or x == 0:
                wall = arcade.Sprite("assets/sandblock.png", WALL_SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    wall = arcade.Sprite("assets/sandblock.png", WALL_SPRITE_SCALING)
    wall.left = 5 * WALL_SPRITE_SIZE
    wall.bottom = 6 * WALL_SPRITE_SIZE
    room.wall_list.append(wall)

    room.background = arcade.load_texture("assets/sand_bkgd.jpg")

    return room


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.current_room = 0

        self.rooms = None
        self.player_sprite = None
        self.player_list = None
        self.physics_engine = None
    
    def setup(self):
        self.player_sprite = arcade.Sprite("assets/indiana_jones.png", 0.35)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.rooms = []

        room = setup_lobby()
        self.rooms.append(room)

        room = setup_room_right()
        self.rooms.append(room)

        room = setup_room_left()
        self.rooms.append(room)

        self.current_room = 0
        
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(settings.WIDTH // 2, settings.HEIGHT //2, 
                                      settings.WIDTH, settings.HEIGHT, self.rooms[self.current_room].background)

        self.rooms[self.current_room].wall_list.draw()

        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = settings.MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -settings.MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -settings.MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = settings.MOVEMENT_SPEED
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN or key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT or key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0
    
    def on_update(self, delta_time):
        self.physics_engine.update()

        if self.player_sprite.center_x > settings.WIDTH and self.current_room == 0:
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_x < 0 and self.current_room == 0:
            self.current_room = 2
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = settings.WIDTH

        elif self.player_sprite.center_x < settings.WIDTH and self.current_room == 2:
            self.current_room = 0
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = settings.WIDTH

        elif self.player_sprite.center_x < 0 and self.current_room == 1:
            self.current_room = 0
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = settings.WIDTH
    
def main():
    window = MyGame(settings.WIDTH, settings.HEIGHT, settings.SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
