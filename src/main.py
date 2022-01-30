import os
from argparse import ArgumentParser
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


from settings import Settings
from command_line_args import parse_command_line_args


def main():
    np.seterr(invalid='ignore')
    args = parse_command_line_args()
    print(vars(args))
    # render settings
    settings = Settings(args.aspect_ratio, args.width, args.samples_per_pixel, args.max_depth)

    g = globals()
    if args.scene not in g:
        raise ValueError(f'Scene {args.scene} not found')
    if args.shader_function not in g:
        raise ValueError(f'render function {args.shader_function} not found')

    scene = g.get(args.scene)
    shader_function = g.get(args.shader_function)
    render(settings, scene, shader_function)

