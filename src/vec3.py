import numpy as np

class Vec3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = np.array(x, dtype=np.float32)
        self.y = np.array(y, dtype=np.float32)
        self.z = np.array(z, dtype=np.float32)

    @staticmethod
    def empty(size):
        x = np.empty(size, dtype=np.float32)
        y = np.empty(size, dtype=np.float32)
        z = np.empty(size, dtype=np.float32)
        return Vec3(x,y,z)

    @staticmethod
    def zeros(size):
        x = np.zeros(size, dtype=np.float32)
        y = np.zeros(size, dtype=np.float32)
        z = np.zeros(size, dtype=np.float32)
        return Vec3(x,y,z)

    @staticmethod
    def ones(size):
        x = np.ones(size, dtype=np.float32)
        y = np.ones(size, dtype=np.float32)
        z = np.ones(size, dtype=np.float32)
        return Vec3(x,y,z)
    
    @staticmethod
    def where(condition, v1, v2):
        x = np.where(condition, v1.x, v2.x)
        y = np.where(condition, v1.y, v2.y)
        z = np.where(condition, v1.z, v2.z)
        return Vec3(x,y,z)
    
    def clip(self, vmin, vmax):
        x = np.clip(self.x, vmin, vmax)
        y = np.clip(self.y, vmin, vmax)
        z = np.clip(self.z, vmin, vmax)
        return Vec3(x,y,z)

    def fill(self, value):
        self.x.fill(value)
        self.y.fill(value)
        self.z.fill(value)

    def repeat(self, n):
        x = np.repeat(self.x, n)
        y = np.repeat(self.y, n)
        z = np.repeat(self.z, n)
        return Vec3(x,y,z)
    
    def __str__(self):
        return 'vec3: x:%s y:%s z:%s' % (str(self.x), str(self.y), str(self.z))
    
    def __len__(self):
        return self.x.size

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __mul__(self, scalar):
        return Vec3(self.x*scalar, self.y*scalar, self.z*scalar)

    def multiply(self, other):
        return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __truediv__(self, scalar):
        return Vec3(self.x/scalar, self.y/scalar, self.z/scalar)
    
    def tile(self, shape):
        '''Replicate np.tile on each component'''
        return Vec3(np.tile(self.x, shape), np.tile(self.y, shape), np.tile(self.z, shape))

    def __getitem__(self, idx):
        '''Extract a vector subset'''
        return Vec3(self.x[idx], self.y[idx], self.z[idx])
    
    def __setitem__(self, idx, other):
        '''Set a vector subset from another vector'''
        self.x[idx] = other.x
        self.y[idx] = other.y
        self.z[idx] = other.z

    def join(self):
        '''Join the three components into a single 3xN array'''
        return np.vstack((self.x, self.y, self.z))
    
    def append(self, other):
        '''Append another vector to this one.
        Use concatenate() because cupy has no append function.
        '''
        self.x = np.concatenate((self.x, other.x))
        self.y = np.concatenate((self.y, other.y))
        self.z = np.concatenate((self.z, other.z))
        

## Aliases
Point3 = Vec3
Color = Vec3

## Utility functions
def unit_vector(v):
    return v / length(v)

def dot(a, b):
    return a.x*b.x + a.y*b.y + a.z*b.z

def length(v):
    return length_squared(v)**0.5

def length_squared(v):
    return v.x*v.x + v.y*v.y + v.z*v.z

def cross(a, b):
    return Vec3(a.y*b.z - a.z*b.y,
                -(a.x*b.z - a.z*b.x),
                a.x*b.y - a.y*b.x)
