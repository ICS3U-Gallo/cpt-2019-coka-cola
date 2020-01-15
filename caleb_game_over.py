import arcade
import settings
import sys

from caleb_minigame import CalebView

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
        arcade.draw_text("Press Space Twice to Restart", 255, 300, arcade.color.WHITE, 18)
        arcade.draw_text("Press Q to Quit", 310, 200, arcade.color.WHITE, 18)
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        pass
    
    def on_key_press(self, key, key_modifiers):
        # If A is pressed, switch to the next view
        if key == arcade.key.SPACE:
            self.director.previous_view() 

        if key == arcade.key.Q:
            sys.exit(0);  
            

if __name__ == "__main__":
    from utils import FakeDirector
    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    my_view = GameOverView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    # main()
    arcade.run()