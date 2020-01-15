import arcade
import settings

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.total_time = 0
        self.score = 0 

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK) 
        
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over", 240, 400, arcade.color.WHITE, 54)
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = CalebView()
        self.window.show_view(game_view) 

if __name__ == "__main__":
    from utils import FakeDirector
    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    my_view = GameOverView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    # main()
    arcade.run()