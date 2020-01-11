import arcade

import settings

from menu import MenuView, InstructionsView
from alex_minigame import AlexView

class Director(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.view_index = 0
        self.views = [
            AlexView,
            MenuView,
            InstructionsView,
            MenuView
        ]
        self.next_view()

    def next_view(self):
        next_view = self.views[self.view_index]()
        next_view.director = self
        self.show_view(next_view)
        self.view_index = (self.view_index + 1) % len(self.views)

def main():
    window = Director(settings.WIDTH, settings.HEIGHT, "CPT Structure")
    arcade.run()


if __name__ == "__main__":
    main()
