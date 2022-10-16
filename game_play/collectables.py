import arcade


class ScrapSteel(arcade.Sprite):
    """class for steel"""

    def __init__(self):
        """initializer"""
        # sets image
        self.main_path = "assets/drop_1.png"
        super().__init__(self.main_path)

    def __repr__(self):
        """sets name to 'Steel'"""
        return "Steel"


class ScrapCopper(arcade.Sprite):
    """class for copper"""

    def __init__(self):
        """initializer"""
        # sets image
        self.main_path = "assets/drop_2.png"
        super().__init__(self.main_path)

    def __repr__(self):
        """sets name to 'Copper'"""
        return "Copper"


class Acid(arcade.Sprite):
    """class for acid"""

    def __init__(self):
        """initializer"""
        # sets image
        self.main_path = "assets/drop_3.png"
        super().__init__(self.main_path)

    def __repr__(self):
        """sets name to 'Acid'"""
        return "Acid"
