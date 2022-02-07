from enum import Enum
from color import gradient,                        red_sphere_blue_gradient, \
                  sphere_normal_map_blue_gradient, two_spheres_on_gradient,  \
                  color_depth,                     color_materials

class RayColor(object):
    def __init__(self, function):
        self.function = function

class Colors(Enum):
    gradient = RayColor(gradient)
    red_sphere_blue_gradient = RayColor(red_sphere_blue_gradient)
    sphere_normal_map_blue_gradient = RayColor(sphere_normal_map_blue_gradient)
    two_spheres_on_gradient = RayColor(two_spheres_on_gradient)
    color_depth = RayColor(color_depth)
    color_materials = RayColor(color_materials)

