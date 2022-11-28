# Universidad del Valle de Guatemala
# Christopher García 20541 
# Gráficas por computadora (10)
# #Raytracing environment

import struct

def char(c):
    # 1 bytes
    return struct.pack('=c', c.encode('ascii'))
    
def word(w):
    # 2 bytes
    return struct.pack('=h', w)
    
def dword(d):
    # 4 bytes
    return struct.pack('=l', d)

class color(object):
    def __init__(self, r, g, b):
        self.r = min(255, max(r, 0))
        self.g = min(255, max(g, 0))
        self.b = min(255, max(b, 0))
        
    def __mul__(self, other):
        
        r = self.r
        g = self.g
        b = self.b
        
        if(type(other) == int or type(other) == float):
            r *= other
            g *= other
            b *= other
        else:
            r *= other.r
            g *= other.g
            b *= other.b
        
        r = min(255, max(r, 0))
        g = min(255, max(g, 0))
        b = min(255, max(b, 0))
        
        return color(r,g,b)
    
    def __add__(self, other):
        
        r = self.r
        g = self.g
        b = self.b
        
        if(type(other) == int or type(other) == float):
            r += other
            g += other
            b += other
        else:
            r += other.r
            g += other.g
            b += other.b
        
        r = min(255, max(r, 0))
        g = min(255, max(g, 0))
        b = min(255, max(b, 0))
        
        return color(r,g,b)
    
    def toBytes(self): 
        return bytes([int(self.b), int(self.g), int(self.r)])
    
    def __repr__(self):
        return "color(%s, %s, %s)" % (self.r, self.g, self.b)

def writebmp(filename, width, height, framebuffer):
        f = open(filename, 'bw')
    
        #pixel header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword((14 + 40) + width * height * 3))
        f.write(word(0))
        f.write(word(0))
        f.write(dword(14 + 40))
        
        #info header
        f.write(dword(40))
        f.write(dword(width))
        f.write(dword(height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(width * height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        
        #pixel data
        for x in range(width):
            for y in range(height):
                f.write(framebuffer[y][x].toBytes())
                
        f.close()

class V3(object):
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
        
    def round(self):
        self.x = round(self.x)
        self.y = round(self.y)
        self.z = round(self.z)
        
    def __add__(self, other):
        return V3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )
    
    def __sub__(self, other):
        return V3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )
        
    def __mul__(self, other):
        if(type(other) == int or type(other) == float):
            return V3(
                self.x * other,
                self.y * other,
                self.z * other
            )
        
        return V3(
            (self.y * other.z) - (self.z * other.y),
            (self.z * other.x) - (self.x * other.z),
            (self.x * other.y) - (self.y * other.x)
        )
        
    def __matmul__(self, other):
        if (type(other) == V3):
            return ((self.x * other.x) + (self.y * other.y) + (self.z * other.z))    
        
    def length(self):
        return ((self.x**2) + (self.y**2) + (self.z**2))**0.5    
    
    def norm(self):
        return self * (1/self.length())
            
    def __repr__(self):
        return "V3(%s, %s, %s)" % (self.x, self.y, self.z)
    
def cross(v1,v2):
    return (
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x
    )

def reflect(I, N): 
    return (I - N * 2 * (N @ I)).norm()

def barycentric(A, B, C, P):
    cx, cy, cz = cross(
        V3(B.x - A.x, C.x - A.x, A.x - P.x),
        V3(B.y - A.y, C.y - A.y, A.y - P.y)
    )
    if (abs(cz) <= 0):
        return (-1, -1, -1)
    
    u = cx/cz
    v = cy/cz
    w = 1 - (u + v)
    
    return (w, v, u)

def refract(I, N, roi):
    etai = 1
    etat = roi
    
    cosi = (I @ N) * -1
    
    if (cosi < 0):
        cosi *= -1
        etai *= -1
        etat *= -1
        N *= -1

    eta = etai/etat
    k = (1 - ((eta ** 2) * (1 - (cosi ** 2))))
    
    if k < 0:
        return V3(0, 0, 0)
    
    cost = k ** 0.5
    
    return ((I * eta) + (N * ((eta * cosi) - cost))).norm()
    