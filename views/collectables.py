import arcade


class ScrapSteel(arcade.Sprite):
    def __init__(self):
        main_path = "assets/drop_1.png"
        super().__init__(main_path)

    def __repr__(self):
        return "Steel"


class ScrapCopper(arcade.Sprite):
    def __init__(self):
        main_path = "assets/drop_2.png"
        super().__init__(main_path)

    def __repr__(self):
        return "Copper"

class Acid(arcade.Sprite):
    def __init__(self):
        main_path = "assets/drop_3.png"
        super().__init__(main_path)

    def __repr__(self):
        return "Acid"