import numpy as np
from command_line_args import parse_args
from renderer import Renderer


def render(settings, scene, shader_function, display=True, save=True):
    renderer = Renderer(settings)
    renderer.render(scene, shader_function)
    if save:
        renderer.save()
    if display:
        renderer.display()

def main():
    np.seterr(invalid='ignore')
    args = parse_args()

    # render the actual image
    render(args["settings"], args["scene"], args["shader_function"])

if __name__ == '__main__':
    main()
