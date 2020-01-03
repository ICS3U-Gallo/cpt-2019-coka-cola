import arcade

import settings


class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.CADMIUM_ORANGE)

    def on_draw(self):
        arcade.start_render()
        title = arcade.Sprite("assets/title_indiana_jones.png", center_x=400, center_y=500)
        title.draw()
        chest = arcade.Sprite("assets/treasure_chest.png", center_x=400, center_y=300)
        chest.draw()
        arcade.draw_text("Press SPACE to start.", settings.WIDTH/2, 100,
                         arcade.color.BLACK, font_size=15, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.director.next_view()

class InstructionsView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.CADMIUM_ORANGE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("This is the instructions page, press space to advance.", settings.WIDTH/2, settings.HEIGHT/2,
                         arcade.color.BLACK, font_size=15, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.director.next_view()


if __name__ == "__main__":
    """This section of code will allow you to run your View
    independently from the main.py file and its Director.

    You can ignore this whole section. Keep it at the bottom
    of your code.

    It is advised you do not modify it unless you really know
    what you are doing.
    """
    from utils import FakeDirector
    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    my_view = MenuView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
