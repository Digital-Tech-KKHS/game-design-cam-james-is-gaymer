import arcade


class ScrapSteel(arcade.Sprite):
    def __init__(self):
        main_path = "assets/drop_1.png"
        super().__init__(main_path)


    

class ScrapCopper(arcade.Sprite):
    def __init__(self):
        main_path = "assets/drop_2.png"
        super().__init__(main_path)


class Acid(arcade.Sprite):
    def __init__(self):
        main_path = "assets/drop_3.png"
        super().__init__(main_path)
