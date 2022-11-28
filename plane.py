# Universidad del Valle de Guatemala
# Christopher García 20541 
# Gráficas por computadora (10)
# #Raytracing environment

from intersect import *
from Lib import *

class Plane(object):
    def __init__(self, center, w, l, material):
        self.center = center
        self.w = w
        self.l = l
        self.material = material
        
    def ray_intersect(self, origin, direction):
        d = (origin.y + self.center.y) / direction.y
        impact = origin + (direction * d)
        normal = V3(0, 1, 0)
        
        if (d <= 0) or \
            impact.x > (self.center.x + self.w/2) or impact.x < (self.center.x - self.w/2) or \
            impact.z > (self.center.z + self.l/2) or impact.z < (self.center.z - self.l/2): 
            return None

        return Intersect(
            distance=d,
            point=impact,
            normal=normal
        )
    
    # def __init__(self, position, normal, material):
    #     self.position = position
    #     self.normal = normal
    #     self.material = material
        
    # def ray_intersect(self, origin, direction):
    #     d = direction @ self.normal
    #     impact = 0
    #     normal = self.normal
        
    #     if abs(d) > 0.0001:
    #         t1 = (self.position - origin) @ normal
    #         t2 = t1 / d
    #         if t2 > 0:
    #             impact = origin + (t2 * [direction.x, direction.y, direction.z])

    #         return Intersect(
    #             distance=t1,
    #             point=impact,
    #             normal=normal,
    #             texCoords = None,
    #             sO = self
    #         )

    #     return None
