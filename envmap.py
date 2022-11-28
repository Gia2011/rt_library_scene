# Universidad del Valle de Guatemala
# Christopher García 20541 
# Gráficas por computadora (10)
# #Raytracing environment

from Lib import *
from math import *
import struct

class Envmap(object):
    def __init__(self, path):
        self.path = path
        self.read()
        
    def read(self):
        with open(self.path, "rb") as image:
            image.seek(2 + 4 + 2 + 2)
            header_size = struct.unpack("=l", image.read(4))[0]    
            image.seek(2 + 4 + 2 + 2 + 4 + 4)
            self.width = struct.unpack("=l", image.read(4))[0]    
            self.height = struct.unpack("=l", image.read(4))[0]    
            
            image.seek(header_size)
            
            self.pixels = []
            for y in range(self.height):
                self.pixels.append([])
                for x in range(self.width):
                    b = ord(image.read(1))
                    g = ord(image.read(1))
                    r = ord(image.read(1))
                    self.pixels[y].append(
                        color(r, g, b)
                    )
    
    def get_color(self, dir):
        normalized_direction = dir.norm()
        x = round(((atan2(normalized_direction.z, normalized_direction.x) / (2 * pi)) + 0.5) * self.width)
        y = (-1 * round((acos((-1 * normalized_direction.y)) / pi) * self.height))

        x -= 1 if (x > 0) else 0
        y -= 1 if (y > 0) else 0

        return self.pixels[y][x]
            
        