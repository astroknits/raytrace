import numpy as np
from vec3 import Vec3, Point3, Color, unit_vector, dot, cross, length, length_squared
from hittable import HitRecord, Sphere
from helpers import random_in_unit_sphere, random_unit_vectors
from ray import Ray
from tqdm import tqdm

img_centre = Point3(0, 0, -1)

red = Color(1, 0, 0)
blue = Color(0.5, 0.7, 1.0)
white = Color(1, 1, 1)

def gradient(rays, settings):
    '''
    The gradient(ray) function linearly blends white and blue depending
    on the height of the 𝑦 coordinate after scaling the ray direction to unit
    length (so −1.0<𝑦<1.0). Because we're looking at the 𝑦 height after
    normalizing the vector, you'll notice a horizontal gradient to the color
    in addition to the vertical gradient.

    I then did a standard graphics trick of scaling that to 0.0≤𝑡≤1.0. When
    𝑡=1.0 I want blue. When 𝑡=0.0 I want white. In between, I want a blend.
    This forms a “linear blend”, or “linear interpolation”, or “lerp” for
    short, between two things. A lerp is always of the form

    blendedValue=(1−𝑡)⋅startValue+𝑡⋅endValue,
    with 𝑡 going from zero to one. In our case this produces the image that results.

    '''
    unit_direction = unit_vector(rays.direction)
    # unit_direction.y runs from -1 to 1
    # Therefore, unit_direction.y + 1.0 runs from 0 to 2.0
    # and t runs from 0 to 1.0
    t = 0.5 * (unit_direction.y + 1.0)
    return white*(1-t) + blue*t

def hit_sphere_orig(centre, radius, rays):
    '''
    Point3 centre: centre of sphere
    float radius: radius of sphere
    Ray rays: ray for which to calculate whether or not hits sphere
    '''
    # Need to calculate the roots of equation:
    # t^2 b.b + 2tb.(A-C) + (A-C).(A-C) - r^2 = 0
    # a = b.b
    # b = 2b.(A-C)
    # c = (A-C).(A-C) - r^2
    # where:
    #    P(t) = A + tb is equation of the ray, with
    #        A - ray origin
    #        b - ray direction
    #    C is the centre of the sphere

    # ray origin to centre of sphere
    np.seterr(invalid='ignore')   # Returns the old settings
    oc = rays.origin - centre

    a = dot(rays.direction, rays.direction)
    b = 2*dot(rays.direction, oc)
    c = dot(oc, oc) - radius*radius

    discriminant = b*b - 4*a*c
    root = (-1.0*b - np.sqrt(discriminant))/(2.0 * a)
    return np.where(discriminant > 0, root, -1.0)

def hit_sphere(centre, radius, rays):
    '''
    Point3 centre: centre of sphere
    float radius: radius of sphere
    Ray rays: ray for which to calculate whether or not hits sphere
    '''
    np.seterr(invalid='ignore')   # Returns the old settings
    # Need to calculate the roots of equation:
    # t^2 b.b + 2tb.(A-C) + (A-C).(A-C) - r^2 = 0
    # a = b.b
    # b = 2b.(A-C)
    # c = (A-C).(A-C) - r^2
    # where:
    #    P(t) = A + tb is equation of the ray, with
    #        A - ray origin
    #        b - ray direction
    #    C is the centre of the sphere
    #
    # define h such that b = 2h, and half_b = h
    # roots become: (-h +/- sqrt(h*h - ac))a

    # ray origin to centre of sphere
    oc = rays.origin - centre

    a = dot(rays.direction, rays.direction)
    half_b = dot(rays.direction, oc)
    c = dot(oc, oc) - radius*radius

    discriminant = half_b*half_b - a*c
    root = (-1.0*half_b - np.sqrt(discriminant))/a
    return np.where(discriminant > 0, root, -1.0)

def red_sphere_blue_gradient(rays, settings, radius=0.5):
    grad = gradient(rays, settings)
    sphere = hit_sphere(img_centre, radius, rays)
    grad[np.where(sphere >= 0)] = red
    return grad

def sphere_normal_map_blue_gradient(rays, settings, radius=0.5):
    grad = gradient(rays, settings)
    t = hit_sphere(img_centre, radius, rays)
    N = unit_vector(rays.at(t) - img_centre)
    # normal components run from -1 to 1
    # Therefore, normal component + 1 runs from 0 to 2
    # and c components run from 0 to 1.0
    c = Color(N.x + 1, N.y + 1, N.z + 1) * 0.5
    grad[np.where(t >= 0)] = c[np.where(t >= 0)]
    return grad

def two_spheres_on_gradient(rays, world, settings):
    grad = gradient(rays, settings)

    hit_record = HitRecord(len(rays))
    for hittable in world:
        hittable.update_hit_record(rays, 0, np.inf, hit_record)

    hits = np.where(hit_record.t != np.inf)
    hit_color = (hit_record.normal[hits] + Vec3(1,1,1)) * 0.5
    grad[hits] = hit_color
    return grad

def color_depth(rays, world, settings):
    grad = gradient(rays, settings)
    frame_intensity = np.full(len(rays), 1.0, dtype=np.float32)
    frame_rays = rays
    hit_record = HitRecord(len(rays))

    for d in range(settings.max_depth):

        # Initialize all distances to infinite
        hit_record.t.fill(np.inf)
        for hittable in world:
            hittable.update_hit_record(rays, 0.001, np.inf, hit_record)

        # Rays that have hit something will be used in the next iteration
        hit_idx = np.where(hit_record.t != np.inf)[0]

        if len(hit_idx) > 0:

            # Narrow down the hit record and calculate new rays
            hit_record = hit_record[hit_idx]
            
            in_unit_sphere = random_in_unit_sphere(len(hit_idx))
            # in_unit_sphere = unit_vector(in_unit_sphere)
            neg_hemisphere = np.where(dot(in_unit_sphere, hit_record.normal) < 0)
            in_unit_sphere[neg_hemisphere] = in_unit_sphere[neg_hemisphere] * -1.0

            target = (hit_record.p
                      + hit_record.normal
                      + in_unit_sphere)

            rays = Ray(hit_record.p, target - hit_record.p)

            # Update global arrays
            frame_rays.direction[hit_record.index] = rays.direction
            frame_intensity[hit_record.index] *= 0.5 

        else:
            break
    
    return grad * frame_intensity

def color_materials(rays, world, settings):
    frame_intensity = Vec3.ones(len(rays))
    frame_rays = rays
    hit_record = HitRecord(len(rays))

    materials = set([x.material for x in world])

    for d in range(settings.max_depth):

        # Initialize all distances to infinite and propagate all rays
        hit_record.t.fill(np.inf)
        hit_record.material_id.fill(0)
        for hittable in world:
            hittable.update_hit_record(rays, 0.001, np.inf, hit_record)

        for material in materials:
            material_hits = np.where(hit_record.material_id == id(material))[0]
            if len(material_hits) == 0:
                continue

            my_rays = rays[material_hits]
            my_rec = hit_record[material_hits]
            result = material.scatter(my_rays, my_rec)

            # All rays have done something
            rays[material_hits] = result.rays
            frame_rays.direction[my_rec.index] = result.rays.direction

            intensity = result.attenuation.multiply(frame_intensity[my_rec.index])
            intensity[np.where(~result.is_scattered)] = Vec3(0,0,0)

            frame_intensity[my_rec.index] = intensity

            # Those that have been scattered stop here
            not_scattered_material_idx = material_hits[~result.is_scattered]
            hit_record.t[not_scattered_material_idx] = np.inf

        # Iterate with those rays that have been scattered by something
        scattered_rays = np.where(hit_record.t != np.inf)[0]
        rays = rays[scattered_rays]
        hit_record = hit_record[scattered_rays]

        if len(rays) == 0:
            break

    return gradient(frame_rays, settings).multiply(frame_intensity)

