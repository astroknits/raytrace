from collections import namedtuple
import numpy as np
from vec3 import Vec3, Point3, Color, unit_vector, dot, cross, length, length_squared
from ray import Ray
from hittable import HitRecord
from helpers import random_unit_vectors, random_in_unit_sphere

ScatterResult = namedtuple('ScatterResult', 'attenuation rays is_scattered')

class Material:
    def scatter(r_in: Ray, ray_idx, rec: HitRecord) -> ScatterResult:
        pass

class Lambertian(Material):
    # scatters rays and attenuates by the albedo
    def __init__(self, albedo: Color):
        # albedo is a property of the material
        self.albedo = albedo

    def scatter(self, r_in: Ray, rec: HitRecord) -> ScatterResult:

        scatter_direction = rec.normal + random_unit_vectors(len(r_in))
        scattered = Ray(rec.p, scatter_direction)

        return ScatterResult(attenuation = self.albedo,
                             rays = scattered,
                             is_scattered = np.full(len(r_in), True, dtype=np.bool))

def reflect(v, n):
    return v - n*2*dot(v, n)

class Metal(Material):

    def __init__(self, albedo: Color, f=1):
        self.albedo = albedo
        self.fuzz = f if f < 1 else 1

    def scatter(self, r_in: Ray, rec: HitRecord) -> ScatterResult:

        reflected = reflect(unit_vector(r_in.direction), rec.normal)
        scatter_direction = reflected + random_in_unit_sphere(len(r_in))*self.fuzz
        scattered = Ray(rec.p, scatter_direction);

        return ScatterResult(attenuation = self.albedo,
                             rays = scattered,
                             is_scattered = dot(scattered.direction, rec.normal) > 0)
