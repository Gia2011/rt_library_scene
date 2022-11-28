# Universidad del Valle de Guatemala
# Christopher García 20541 
# Gráficas por computadora (10)
# #Raytracing environment

class Light:
    def __init__(self, position, intensity, colorx):
        self.position = position
        self.intensity = intensity
        self.col = colorx
        