# Universidad del Valle de Guatemala
# Christopher García 20541 
# Gráficas por computadora (10)
# #Raytracing environment

class Intersect:
    def __init__(self, distance, point, normal, face = None):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.face = face
        