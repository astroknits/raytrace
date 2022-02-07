import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm

from settings import Settings
from camera import Camera
from helpers import random_uniform
from vec3 import Vec3


class Renderer(object):
    def __init__(self, settings=None):
        self.settings = settings if settings else Settings()
        self.camera = Camera(settings.aspect_ratio,
                             settings.viewport_height,
                             settings.focal_length,
                             settings.camera_origin)
        self.image = None

    def render(self, scene, ray_color, apply_gamma=True):
        colors = self._compute_image(scene, ray_color, apply_gamma=apply_gamma)
        self.image = self._convert_to_pil(colors)
        return self.image
    
    def display(self):
        try:
            display(self.image)
            return
        except NameError:
            if isinstance(self.image, Image.Image):
                self.image.show()
                return
            else:
                print(f'cannot display image {image}')
        return

    def save(self, image_name='img.bmp', subdir=None):
        image_dir = 'images'
        if subdir:
            image_dir = os.path.join(image_dir, subdir)
        if not os.path.isdir(image_dir):
            os.makedirs(image_dir)
        self.image.save(os.path.join(image_dir, image_name))

    def _convert_to_pil(self, v, scale = 255.999):
        # quick function that can take a Vec3 object and return an Image object.
        # Our arrays are 3xN, while the Image.fromarray() method expects Nx3,
        # so we need to swap the axes. The function is able to take 1d or 2d arrays
        # as an input. It will assume that 1d arrays are grayscale images, and 2d
        # arrays are composition of 3 grayscale images in RGB order.
        img = (v.join() * scale).astype(np.uint8)

        if len(img.shape) == 2:
            img_rgb = img.swapaxes(0,1).reshape(self.settings.height, self.settings.width, 3)
        else:
            img_rgb = img.reshape(self.settings.height, self.settings.width)

        return Image.fromarray(img_rgb)
    
    def _compute_image(self, scene, ray_color, apply_gamma=True):
        ii, jj = np.mgrid[:float(self.settings.height), :float(self.settings.width)]

        u = (jj/(self.settings.width-1)).flatten().astype(np.float32)
        v = (ii/(self.settings.height-1)).flatten().astype(np.float32)

        img = Vec3.zeros(self.settings.width * self.settings.height)
        for s in tqdm(range(self.settings.samples_per_pixel)):
            uu = u + random_uniform(0.0, 1.0, u.size) / (self.settings.width - 1)
            vv = v + random_uniform(0.0, 1.0, v.size) / (self.settings.height - 1)

            r = self.camera.get_ray(uu,vv)

            img += ray_color(r, scene, self.settings)

        img *= 1.0 / self.settings.samples_per_pixel
        if apply_gamma:
            img.x = np.sqrt(img.x)
            img.y = np.sqrt(img.y)
            img.z = np.sqrt(img.z)
        return img.clip(0.0, 0.999)

    
