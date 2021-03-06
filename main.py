import arcade

import settings

from menu import MenuView
from alex_minigame import AlexMenuView
from caleb_minigame import CalebMenuView
from kevin_minigame import KevinView
from owen_minigame import OwenMenuView


class Director(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.view_index = 0
        self.views = [
            MenuView,
            AlexMenuView,
            CalebMenuView,
            KevinView,
            OwenMenuView
        ]
        self.next_view()

    def next_view(self):
        next_view = self.views[self.view_index]()
        next_view.director = self
        self.show_view(next_view)
        self.view_index = (self.view_index + 1) % len(self.views)

    def previous_view(self):
        prev_view = self.views[self.view_index-1]()
        prev_view.director = self
        self.show_view(prev_view)
        self.view_index = (self.view_index - 1) % len(self.views)


def main():
    window = Director(settings.WIDTH, settings.HEIGHT, "CPT Structure")
    arcade.run()


if __name__ == "__main__":
    main() 
