import os
import numpy as np
from PIL import Image
from vec3 import Vec3, length_squared

def random_uniform(low, high, size):
    return np.random.uniform(low, high, size).astype(np.float32)

def random_in_unit_sphere(n):
    '''Generate random Vec3 arrays in batches and keep the ones inside the unit sphere'''

    values = Vec3.zeros(0)

    while len(values) < n:
        random_values = Vec3(random_uniform(-1.0, 1.0, n), random_uniform(-1.0, 1.0, n), random_uniform(-1.0, 1.0, n))
        good_ones = length_squared(random_values) < 1
        values.append(random_values[good_ones])

    return values[np.arange(n)]

def random_unit_vectors(n):
    a = random_uniform(0.0, 2.0*np.pi, n)
    z = random_uniform(-1.0, 1.0, n)
    r = np.sqrt(1 - z*z)
    return Vec3(r*np.cos(a), r*np.sin(a), z)


