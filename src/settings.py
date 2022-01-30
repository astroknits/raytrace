from vec3 import Point3

# Default values
ASPECT_RATIO = 16.0/9.0

# Image default values
WIDTH = 400
SAMPLES_PER_PIXEL = 10
MAX_DEPTH = 50

# Camera Default Values
ORIGIN = Point3(0, 0, 0)
VIEWPORT_HEIGHT = 2.0
FOCAL_LENGTH = 1.0

class Settings(object):
    def __init__(self,
                 aspect_ratio=ASPECT_RATIO,
                 width=WIDTH,
                 samples_per_pixel=SAMPLES_PER_PIXEL,
                 max_depth=MAX_DEPTH,
                 camera_origin=ORIGIN,
                 viewport_height=VIEWPORT_HEIGHT,
                 focal_length=FOCAL_LENGTH):
        # image default values
        self.aspect_ratio = aspect_ratio
        self.width = width
        self.height = self._get_height()
        self.samples_per_pixel = samples_per_pixel
        self.max_depth = max_depth

        # camera default values
        self.camera_origin = camera_origin
        self.viewport_height = viewport_height
        self.focal_length = focal_length

    def _get_height(self):
        return int(self.width / self.aspect_ratio)
