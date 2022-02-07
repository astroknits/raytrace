from argparse import ArgumentParser
from settings import Settings
from color_types import Colors
from scenes import Scenes

def get_command_line_args():
    parser = ArgumentParser()
    parser.add_argument('-s', '--scene', type=str, choices=[s.name for s in Scenes], help='scene name (default world3)', default='world3')
    parser.add_argument('-w', '--width', type=int, help='image width (default 400)', default=400)
    parser.add_argument('-a', '--aspect', dest='aspect_ratio', type=float, help='image aspect ratio (default=16/9)', default=16.0/9.0)
    parser.add_argument('-p', '--samples', dest='samples_per_pixel', type=int, help='samples per pixel (default 10)', default=10)
    parser.add_argument('-d', '--max-depth', type=int, help='max depth (default 50)', default=50)
    parser.add_argument('-f', '--shader', dest='shader_function',
                                          type=str,
                                          choices=[s.name for s  in Colors],
                                          help='name of function to use (default color_materials)',
                                          default='color_materials')
    return parser.parse_args()
    
def parse_args():
    args = vars(get_command_line_args())

    arguments = {}
    # render settings
    arguments["settings"] = Settings(args["aspect_ratio"], args["width"], args["samples_per_pixel"], args["max_depth"])
    arguments["scene"] = Scenes[args["scene"]].value
    arguments["shader_function"] = Colors[args["shader_function"]].value.function

    return arguments
