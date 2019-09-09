from app.config import Display


class Rectangle:
    def __init__(self, hcorner, vcorner, width, height, red, green, blue):
        if hcorner < 0 or hcorner > Display.WIDTH or vcorner < 0 or vcorner > Display.HEIGHT:
            raise ValueError
        if red < 0 or red > 15 or green < 0 or green > 15 or blue < 0 or blue > 15:
            raise ValueError
        self.width = width
        self.height = height
        self.hCorner = hcorner
        self.vCorner = vcorner
        self.red = red
        self.green = green
        self.blue = blue

    def get_byte_sequence(self):
        sequence = [bin(self.red)[2:].rjust(8, "0"), bin(self.green)[2:].rjust(8, "0"),
                    bin(self.blue)[2:].rjust(8, "0"), bin(self.hCorner % 128)[2:].rjust(8, "0"),
                    bin(self.hCorner // 128)[2:].rjust(8, "0"), bin(self.vCorner % 128)[2:].rjust(8, "0"),
                    bin(self.vCorner // 128)[2:].rjust(8, "0"), bin(self.width % 128)[2:].rjust(8, "0"),
                    bin(self.width // 128)[2:].rjust(8, "0"), bin(self.height % 128)[2:].rjust(8, "0"),
                    bin(self.height // 128)[2:].rjust(8, "0")]
        return sequence
