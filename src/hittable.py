import numpy as np
from collections import namedtuple
from abc import abstractmethod
from vec3 import Vec3, Point3, Color, unit_vector, dot, cross, length, length_squared
from ray import Ray

class HitRecord:
    def __init__(self, n, empty=False):
        self.p           = empty or Vec3.empty(n)
        self.normal      = empty or Vec3.empty(n)
        self.t           = empty or np.full(n, np.inf, dtype=np.float32)
        self.front_face  = empty or np.zeros(n, dtype=np.float32)
        self.index       = empty or np.arange(n, dtype=np.int32)
        self.material_id = empty or np.zeros(n, dtype=np.int64)

    def __getitem__(self, idx):
        other = HitRecord(len(idx), empty=True)
        other.p          = self.p[idx]
        other.normal     = self.normal[idx]
        other.t          = self.t[idx]
        other.front_face = self.front_face[idx]
        other.index      = self.index[idx]
        other.material_id = self.material_id[idx]
        return other

class Hittable:
    @abstractmethod
    def update_hit_record(rays, t_min, t_max, hit_record: HitRecord):
        pass
    
class Sphere(Hittable):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def update_hit_record(self, rays, t_min, t_max, hit_record):
        oc = rays.origin - self.center
        a = length_squared(rays.direction)
        half_b = dot(oc, rays.direction)
        c = length_squared(oc) - self.radius*self.radius
        discriminant = half_b*half_b - a*c

        root = np.sqrt(discriminant)
        # calculate both roots of the quadratic
        t1 = (-half_b - root) / a
        t2 = (-half_b + root) / a
        # Check whether the roots are between the min/max values for t
        hit1 = np.logical_and(t1 < t_max, t1 > t_min)
        hit2 = np.logical_and(t2 < t_max, t2 > t_min)

        # Combine the two hits, precedence to t1 (closest)
        t = np.where(hit2, t2, np.inf)
        t = np.where(hit1, t1, t)

        # Detect where in the rays list we are the closest hit
        closest = np.where(t < hit_record.t)
        
        # Calculate normal
        hit_rays = rays[closest]
        
        p = hit_rays.at(t[closest])
        outward_normal = (p - self.center) / self.radius 
        front_face = dot(hit_rays.direction, outward_normal) < 0 
        normal = Vec3.where(front_face, outward_normal, -outward_normal)
        
        # Update hit records
        hit_record.p[closest] = p
        hit_record.normal[closest] = normal
        hit_record.t[closest] = t[closest]
        hit_record.front_face[closest] = front_face
        hit_record.material_id[closest] = id(self.material)
