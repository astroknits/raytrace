from vec3 import Vec3, Point3
from ray import Ray

class Camera:
    def __init__(self,
                 aspect_ratio,
                 viewport_height,
                 focal_length,
                 origin):
        aspect_ratio = aspect_ratio
        viewport_height = viewport_height
        viewport_width = aspect_ratio * viewport_height;
        focal_length = focal_length;

        self.origin = origin
        self.horizontal = Vec3(viewport_width, 0.0, 0.0);
        self.vertical = Vec3(0.0, -viewport_height, 0.0);
        self.lower_left_corner = (self.origin
                                  - self.horizontal/2
                                  - self.vertical/2
                                  - Vec3(0, 0, focal_length))

    def get_ray(self, u, v):
        all_origins = self.origin.tile((u.size,))
        return Ray(all_origins, self.lower_left_corner
                                + self.horizontal * u
                                + self.vertical * v
                                - all_origins)

def get_camera(aspect_ratio, viewport_height, focal_length, origin):
    return Camera(aspect_ratio, viewport_height, focal_length, origin)

