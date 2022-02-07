from enum import Enum
from vec3 import Vec3, Point3, Color, unit_vector, dot, cross, length, length_squared
from hittable import HitRecord, Sphere
from material import Lambertian, Metal
from color import img_centre

####
# Set up scene
####
diffuse_mat = Lambertian(Color(0, 0, .3))
metal_mat = Metal(Color(.3, .1, .1))
world1 = [Sphere(img_centre, 0.5, diffuse_mat), Sphere(Point3(0, -100.5, -1), 100, diffuse_mat), Sphere(Point3(0.5, 0.25, -1), 0.25, metal_mat)]

material_ground = Lambertian(Color(0.8, 0.8, 0.0))
material_center = Lambertian(Color(0.7, 0.3, 0.3))
material_left   = Metal(Color(0.8, 0.8, 0.8))
material_right  = Metal(Color(0.8, 0.6, 0.2))

world2 = [
    Sphere(Point3( 0.0, -100.5, -1.0), 100.0, material_ground),
    Sphere(Point3( 0.0,    0.0, -1.0),   0.5, material_center),
    Sphere(Point3(-1.0,    0.0, -1.0),   0.5, material_left),
    Sphere(Point3( 1.0,    0.0, -1.0),   0.5, material_right),
]

material_left   = Metal(Color(0.8, 0.8, 0.8), 0.3)
material_right  = Metal(Color(0.8, 0.6, 0.2), 1.0)

world3 = [
    Sphere(Point3( 0.0, -100.5, -1.0), 100.0, material_ground),
    Sphere(Point3( 0.0,    0.0, -1.0),   0.5, material_center),
    Sphere(Point3(-1.0,    0.0, -1.0),   0.5, material_left),
    Sphere(Point3( 1.0,    0.0, -1.0),   0.5, material_right),
]


class Scenes(Enum):
    world1 = world1
    world2 = world2
    world3 = world3
