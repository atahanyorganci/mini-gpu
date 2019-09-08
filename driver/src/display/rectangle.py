from resolution import Resolution as res


class Rectangle:
    def __init__(self, hCorner, vCorner, width, height, red, green, blue):
        if hCorner < 0 or hCorner > res.WIDTH or vCorner < 0 or vCorner > res.HEIGHT:
            raise ValueError
        if red < 0 or red > 15 or green < 0 or green > 15 or blue < 0 or blue > 15:
            raise ValueError
        self.width = width
        self.height = height
        self.hCorner = hCorner
        self.vCorner = vCorner
        self.red = red
        self.green = green
        self.blue = blue
    
    def getByteSequence(self):
        sequence = []
        sequence.append(bin(self.red)[2:].rjust(8, "0"))
        sequence.append(bin(self.green)[2:].rjust(8, "0"))
        sequence.append(bin(self.blue)[2:].rjust(8, "0"))
        sequence.append(bin(self.hCorner % 128)[2:].rjust(8, "0"))
        sequence.append(bin(self.hCorner // 128)[2:].rjust(8, "0"))
        sequence.append(bin(self.vCorner % 128)[2:].rjust(8, "0"))
        sequence.append(bin(self.vCorner // 128)[2:].rjust(8, "0"))
        sequence.append(bin(self.width % 128)[2:].rjust(8, "0"))
        sequence.append(bin(self.width // 128)[2:].rjust(8, "0"))
        sequence.append(bin(self.height % 128)[2:].rjust(8, "0"))
        sequence.append(bin(self.height // 128)[2:].rjust(8, "0")) 
        return sequence

test = Rectangle(200, 200, 100, 100, 15, 0, 0)
print(test.getByteSequence())
