from app.config import Display


class Rectangle:
    def __init__(self, hcorner, vcorner, width, height, red, green, blue):
        if hcorner < 0 or hcorner > Display.WIDTH or vcorner < 0 or vcorner > Display.HEIGHT:
            raise ValueError
        if red < 0 or red > 15 or green < 0 or green > 15 or blue < 0 or blue > 15:
            raise ValueError
        self.width = width
        self.height = height
        self.hcorner = hcorner
        self.vcorner = vcorner
        self.red = red
        self.green = green
        self.blue = blue

    def __bytes__(self):
        return bytes([1, self.red, self.green, self.blue,
                      self.hcorner % 256, self.hcorner // 256, self.vcorner % 256, self.vcorner // 256,
                      self.width % 256, self.width // 256, self.height % 256, self.height // 256])
