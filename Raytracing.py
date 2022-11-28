# Universidad del Valle de Guatemala
# Christopher García 20541 
# Gráficas por computadora (10)
# #Raytracing environment

from math import pi, tan
from Lib import *
import math
from light import Light
from material import Material
from sphere import *
from cube import *
from plane import *
from triangle import *
from envmap import *

MAX_RECURSION_DEPTH = 3

class RayTracer(object):
    def __init__(self, width, height):
        self.width = width 
        self.height = height
        self.background_color = color(0, 0, 100)
        self.current_color = color(255, 255, 255)
        self.ray_prob = 1
        self.scene = []
        self.envmap = None
        self.light = Light(V3(-20, 20, 20), 2, color(255,255,255))
        self.lightF = Light(V3(20, 20, 20), 2, color(255,255,255))
        self.clear()

    def clear(self):
        self.framebuffer = [
            [self.background_color for x in range(self.width)]
            for y in range(self.height)
        ]
        
    def point(self, x, y, color=None):
        if y >= 0 and y <= self.height and x >= 0 and x <= self.width:
            self.framebuffer[y][x] = color or self.current_color
        
    def write(self, filename):
        writebmp(filename, self.width, self.height, self.framebuffer)
        
    def render(self):
        fov = int(pi/2)
        ar = self.width/self.height
        tana = tan(fov/2)
        
        for y in range (self.height):
            for x in range (self.width):
                i = (((2 * (x + 0.5)) / self.width) - 1) * (ar * tana)
                j = (1 - ((2 * (y + 0.5)) / self.height)) * tana
                
                direction = V3(i, j, -1).norm()
                origin = V3(0, 0, 0)
                c = self.cast_ray(origin, direction)
                self.point(y, x, c)
    
    '''   
    #Ejercicio#1         
    def cast_ray(self, origin, direction):
        for s,c in self.scene:
            if s.ray_intersect(origin, direction):
                return c
        return self.background_color
    '''
    
    def envmap_background(self, direction):
        return self.envmap.get_color(direction) if (self.envmap is not None) else self.background_color
    
    def cast_ray(self, origin, direction, recursion = 0):
        
        if recursion >= MAX_RECURSION_DEPTH:
            return self.envmap_background(direction)
        
        material, intersect = self.scene_intersect(origin, direction)
        
        if material is None:
            return self.envmap_background(direction)
        
        light_dir = (self.light.position - intersect.point).norm()
        light_dirF = (self.lightF.position - intersect.point).norm()
        
        # Shadow
        shadow_bias = 1.1
        # print("2",intersect.point, intersect.normal)
        shadow_orig = intersect.point + (intersect.normal * shadow_bias)
        shadow_material = self.scene_intersect(shadow_orig, light_dir)
        shadow_materialF = self.scene_intersect(shadow_orig, light_dirF)
        shadow_intensity = 0
        shadow_intensityF = 0
        
        
        if shadow_material:
            # Está en la sombra
            shadow_intensity = 0.75
            
        if shadow_materialF:
            # Está en la sombra
            shadow_intensityF = 0.75
        
        # Diffuse component
        diffuse_intensity = self.light.intensity * (light_dir @ intersect.normal)
        diffuse = material.diffuse * diffuse_intensity * material.albedo[0] * (1 - shadow_intensity)
        diffuse_intensityF = self.lightF.intensity * (light_dir @ intersect.normal)
        diffuseF = material.diffuse * diffuse_intensityF * material.albedo[0] * (1 - shadow_intensityF)
       
        # Specular component
        light_reflection = reflect(light_dir, intersect.normal)
        reflection_intensity = max(0, (light_reflection @ direction))
        specular_intensity = self.light.intensity * (reflection_intensity ** material.spec)
        specular = self.light.col * specular_intensity * material.albedo[1]
        
        light_reflectionF = reflect(light_dirF, intersect.normal)
        reflection_intensityF = max(0, (light_reflectionF @ direction))
        specular_intensityF = self.lightF.intensity * (reflection_intensityF ** material.spec)
        specularF = self.lightF.col * specular_intensityF * material.albedo[1]
        
        # Reflection
        if material.albedo[2] > 0:
            reflect_direction = reflect(direction, intersect.normal)
            reflect_bias = -0.5 if (reflect_direction @ intersect.normal < 0) else 0.5
            reflect_origin = intersect.point + (intersect.normal * reflect_bias) 
            reflect_color = self.cast_ray(reflect_origin, reflect_direction, (recursion + 1))
            reflect_directionF = reflect(direction, intersect.normal)
            reflect_biasF = -0.5 if (reflect_directionF @ intersect.normal < 0) else 0.5
            reflect_originF = intersect.point + (intersect.normal * reflect_biasF) 
            reflect_colorF = self.cast_ray(reflect_originF, reflect_directionF, (recursion + 1))
        else:
            reflect_color = color(0, 0, 0)
            reflect_colorF = color(0, 0, 0)
            
        # Refraction
        if material.albedo[3] > 0:
            refract_direction = refract(direction, intersect.normal, material.refractive_index)
            refract_bias = -0.5 if ((refract_direction @ intersect.normal) < 0) else 0.5
            refract_origin = intersect.point + (intersect.normal * refract_bias) 
            refract_color = self.cast_ray(refract_origin, refract_direction, (recursion + 1))
            refract_directionF = refract(direction, intersect.normal, material.refractive_index)
            refract_biasF = -0.5 if ((refract_directionF @ intersect.normal) < 0) else 0.5
            refract_originF = intersect.point + (intersect.normal * refract_biasF) 
            refract_colorF = self.cast_ray(refract_originF, refract_directionF, (recursion + 1))
        else:
            refract_color = color(0, 0, 0)
            refract_colorF = color(0, 0, 0)
            
        reflection = reflect_color * material.albedo[2]
        refraction = refract_color * material.albedo[3]
        reflectionF = reflect_colorF * material.albedo[2]
        refractionF = refract_colorF * material.albedo[3]
        
        return diffuse + specular + reflection + refraction 
                
    def scene_intersect(self, origin, direction):
        
        zbuffer = 999999
        material = None
        intersect = None
        
        for s in self.scene:
            object_intersect = s.ray_intersect(origin, direction)
            if object_intersect:
                if object_intersect.distance < zbuffer:
                    zbuffer = object_intersect.distance
                    if not isinstance(s.material, list):
                        #print(s.material)
                        material = s.material
                    else:
                        #print(object_intersect.face)
                        material = s.material[object_intersect.face]
                    intersect = object_intersect
        
                    #print(material)
        return material, intersect
    
'''
#Ejercicio#1: Snowman
           
WHITE = color(255,255,255)
BLACK = color(0,0,0)
ORANGE = color(255,140,0)

r = RayTracer(600, 600)
r.scene = [
    (Sphere(V3(2.9, 0, -16), 0.25), ORANGE),
    (Sphere(V3(3.5, 0.6, -16), 0.285), BLACK),
    (Sphere(V3(3.5, -0.6, -16), 0.285), BLACK),
    (Sphere(V3(2.6, 0.85, -16), 0.2), BLACK),
    (Sphere(V3(2.6, -0.85, -16), 0.195), BLACK),
    (Sphere(V3(2.35, 0.5, -16), 0.195), BLACK),
    (Sphere(V3(2.35, -0.5, -16), 0.195), BLACK),
    (Sphere(V3(2.15, 0, -16), 0.195), BLACK),
    (Sphere(V3(-0.8, 0, -16), 0.27), BLACK),
    (Sphere(V3(0.1, 0, -16), 0.27), BLACK),
    (Sphere(V3(1, 0, -16), 0.27), BLACK),
    (Sphere(V3(-3.5, 0, -16), 2.8), WHITE),
    (Sphere(V3(0, 0, -16), 2.1), WHITE),
    (Sphere(V3(2.8, 0, -16), 1.47), WHITE),
]
r.render()
r.write('snowman.bmp')
'''

'''
#Ejercicio#2: Osos

rubber = Material(diffuse=color(80,0,0), albedo=[0.9, 0.1], spec=10)
ivory = Material(diffuse=color(100,100,80), albedo=[0.6, 0.3], spec=50)
brown = Material(diffuse=color(135, 70, 20), albedo=[0.8, 0.2], spec=30)
silver = Material(diffuse=color(163, 163, 162), albedo=[0.7, 0.2], spec=75)
gray = Material(diffuse=color(80, 80, 80), albedo=[0.9, 0.1], spec=25)
lightBrown = Material(diffuse=color(199, 144, 90), albedo=[0.6, 0.4], spec=35)
blue = Material(diffuse=color(51, 70, 145), albedo=[0.8,0.2], spec=20)
black = Material(diffuse=color(0,0,0), albedo=[0.8,0.2], spec=20)

r = RayTracer(800, 800)
r.background_color = color(100, 100, 100)
r.light = Light(V3(-4, -4, 0), 1, color(255,255,255))

r.scene = [
    Sphere(V3(-3, -1.65, -13.8), 1.65, silver),
    Sphere(V3(3, -1.65, -13.8), 1.65, brown),
    Sphere(V3(-4.7, 0.7, -12.2), 0.9, silver),
    Sphere(V3(-0.8, 0.7, -12.6), 0.9, silver),
    Sphere(V3(-3.6, -3, -12.7), 0.7, silver),
    Sphere(V3(-1.85, -3, -13), 0.7, silver),
    Sphere(V3(-2.5, -1.5, -10), 0.17, black),
    Sphere(V3(-1.9, -1.5, -10), 0.17, black),
    Sphere(V3(2.5, -1.5, -10), 0.17, black),
    Sphere(V3(1.9, -1.5, -10), 0.17, black),
    Sphere(V3(-2.2, -0.78, -10), 0.2, black),
    Sphere(V3(2.2, -0.78, -10), 0.2, black),
    Sphere(V3(-3.6, 3.3, -12.1), 0.95, silver),
    Sphere(V3(-1.7, 3.3, -12.4), 0.95, silver),
    Sphere(V3(4.2, 0.7, -12.2), 0.9, brown),
    Sphere(V3(0.8, 0.7, -12.6), 0.9, brown),
    Sphere(V3(3.6, -3, -12.7), 0.7, lightBrown),
    Sphere(V3(1.85, -3, -13), 0.7, lightBrown),
    Sphere(V3(1.6, 3.15, -12.1), 0.95, brown),
    Sphere(V3(3.6, 3.1, -12), 0.95, brown),
    Sphere(V3(-2.9, -0.82, -13), 0.8, gray),
    Sphere(V3(2.9, -0.82, -13), 0.8, lightBrown),
    Sphere(V3(-3, 2, -14), 2.35, blue),
    Sphere(V3(3, 2, -14), 2.35, rubber),
]
r.point(100, 100)
r.render()
r.write('ositos.bmp')
'''

ivory  = Material(diffuse = color(200, 200, 180), albedo = [0.6, 0.3, 0, 0],   spec = 10)
rubber = Material(diffuse = color(180, 0, 0),     albedo = [0.9, 0.1, 0.1, 0], spec = 50)
mirror = Material(diffuse = color(255, 255, 255), albedo = [0, 1, 0.8, 0],     spec = 1425)
glass  = Material(diffuse = color(150, 180, 200), albedo = [0, 0.5, 0, 0.8],   spec = 125, refractive_index=1.5)
darkness = Material(diffuse = color(0, 0, 0),     albedo = [0.7, 0.3, 0.1, 0], spec = 1005)
gold = Material(diffuse= color(212, 175, 55), albedo= [0.6, 0.3, 0, 0], spec = 620)

materials = [darkness if i < 5 else gold for i in range(6)]
materials2 = [darkness if i > 4 else ivory for i in range(6)]
materials3 = [darkness if i > 5 else rubber for i in range(6)]
materials4 = [darkness if i < 5 else darkness for i in range(6)]

r = RayTracer(1000, 1000)
r.envmap = Envmap('./Space.bmp')
r.light = Light(V3(0, -15, -16), 2, color(255,255,255))
# r.lightF = Light(V3(0, -15, -20), 2, color(255,255,255))

r.scene = [
    Sphere(V3(7, -7, -25), 2, ivory),
    Sphere(V3(6.3, -7, -20), 2, rubber),
    Sphere(V3(9, -7, -22.5), 2, darkness),
    Sphere(V3(0, 0, -6), 0.1, darkness),
    Plane(V3(0, 2, -5), 6, 5, mirror),
    Cube(V3(-3.5, -5, -15), 2, materials),
    Cube(V3(-5.5, -5, -16), 2, materials2),
    Cube(V3(-4, -3.5, -16), 2, materials3),
    Cube(V3(-5, -3, -16), 2, materials4),
    Cube(V3(0, 0, -6.5), 2, glass),
    Cube(V3(0, 0, -6), 1, mirror),
    Triangles([V3(-3.5, 2, -10), V3(0, -3, -10), V3(3.5, 2, -10), V3(0, 2, -10)], gold)
]

r.render()
r.write('Pruebas.bmp')