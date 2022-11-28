# Universidad del Valle de Guatemala
# Christopher García 20541 
# Gráficas por computadora (10)
# #Raytracing environment

from Lib import *
from intersect import *
from plane import *

class Cube(object):
    def __init__(self, position, size, materials):
        self.position = position
        self.size = size
        self.material = materials
        self.bsMin = -999999
        self.bsMax = 999999
        
    def ray_intersect(self, origin, direction):
        
        x, y, z = self.position.x, self.position.y, self.position.z
        size = self.size
        bsMin = self.bsMin
        bsMax = self.bsMax
        
        txmin = ((x - (size*0.5)) - origin.x) / direction.x 
        txmax = ((x + (size*0.5)) - origin.x) / direction.x 
        
        if txmin > txmax: txmin, txmax = txmax, txmin
        if txmin > bsMin: bsMin = txmin
        if txmax < bsMax: bsMax = txmax
        if bsMin > bsMax: return None
        
        tymin = ((y - (size*0.5)) - origin.y) / direction.y 
        tymax = ((y + (size*0.5)) + origin.y) / direction.y 
        
        if (tymin > tymax): tymin, tymax = tymax, tymin
        if tymin > bsMin: bsMin = tymin
        if tymax < bsMax: bsMax = tymax
        if bsMin > bsMax: return None
        
        tzmin = ((z - (size*0.5)) - origin.z) / direction.z 
        tzmax = ((z + (size*0.5)) + origin.z) / direction.z 
    
        if (tzmin > tzmax): tzmin, tzmax = tzmax, tzmin        
        if tzmin > bsMin: bsMin = tzmin
        if tzmax < bsMax: bsMax = tzmax
        if bsMin > bsMax: return None
        
        if bsMin < 0: 
            bsMin = bsMax
            if bsMin < 0: return None
            
        impact = (direction * bsMin) - origin
        normal = (impact - self.position).norm()
        
        face = 0
        
        if normal.x < 0 and normal.y < 0:
            face = 1
        elif normal.x < 0 and normal.y > 0:
            face = 2
        elif normal.x > 0 and normal.y < 0:
            face = 3  
        elif normal.x > 0 and normal.y > 0:
            face = 4
        else:
            face = 5

        # print("\n",normal)
        # print("x neg" if normal.x < 0 else "x pos")
        # print("y neg" if normal.y < 0 else "y pos")
        # print("z neg" if normal.z < 0 else "z pos")
        # print("\n")
         
        return Intersect(
            distance = bsMin,
            point = impact,
            normal = normal,
            face = face
        )
        
        
        
        