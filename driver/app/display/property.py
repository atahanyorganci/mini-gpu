from app.config import Display


class Property:

    def __init__(self, width, height, red, blue, green):
        if width < 0 or width > Display.WIDTH:
            raise ValueError
        if height < 0 or height > Display.HEIGHT:
            raise ValueError
        max_color = 2 ** Display.COLOR - 1
        if red < 0 or red > max_color or green < 0 or green > max_color or blue < 0 or blue > max_color:
            raise ValueError
        self.width = width
        self.height = height
        self.red = red
        self.green = green
        self.blue = blue

    def __bytes__(self):
        return bytes([self.red, self.green, self.blue,
                      self.width % 256, self.width // 256,
                      self.height % 256, self.height // 256])
