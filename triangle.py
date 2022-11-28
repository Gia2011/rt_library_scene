# Universidad del Valle de Guatemala
# Christopher García 20541 
# Gráficas por computadora (10)
# #Raytracing environment

from Lib import *
from intersect import *
from plane import *

# Referencia Ray interesect: https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/ray-triangle-intersection-geometric-solution
class Triangles(object):
    def __init__(self, vectors, material):
        self.v0, self.v1, self.v2, self.v3 = vectors[0], vectors[1], vectors[2], vectors[3]
        self.material = material
        
    def triangle_Unit(self, vecs, origin, direction):        
        V0V1 = vecs[1] - vecs[0]
        V0V2 = vecs[2] - vecs[0]

        N = V0V1 * V0V2

        N_RayDir = N @ direction
        
        if N_RayDir < 0.000000001:
            return None
        
        d = N @ vecs[0]
        t = (d + (N @ origin)) / N_RayDir

        if t <= 0:
            return None
        
        p = origin + (direction * t)

        w, v, u = barycentric(vecs[0], vecs[1], vecs[2], p)

        if w < 0 or v < 0 or u < 0:
            return None

        return Intersect(
            distance=t,
            point=p,
            normal=N.norm()
        )

    def ray_intersect(self, origin, direction):
        
        triangles = [
            self.triangle_Unit([self.v0, self.v2, self.v1], origin, direction),
            self.triangle_Unit([self.v0, self.v2, self.v3], origin, direction),
            self.triangle_Unit([self.v0, self.v3, self.v1], origin, direction),
            self.triangle_Unit([self.v1, self.v2, self.v3], origin, direction)
        ]
        
        t = 999_999
        intersect = None
        
        for tr in triangles:
            if tr:
                if tr.distance < t:
                    t = tr.distance
                    intersect = tr
                    
        if intersect is None:
            return None

        return Intersect(
            distance=intersect.distance,
            point=intersect.point,
            normal=intersect.normal
        )
        