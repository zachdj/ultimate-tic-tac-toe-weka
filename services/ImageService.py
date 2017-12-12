"""
The ImageService singleton handles the loading of image assets for scenes
It will retrieve images using logical names (e.g. get_main_menu_bg() )
The actual image returned from a logical call can vary based on the selected theme

Once an image is loaded from a file, it is kept in memory in case it is requested again
"""

import pygame
import os
import services.SettingsService as Settings


_image_library = {}


def build_image_path(filename):
    return "assets/img/%s/%s" % (Settings.theme['path_prefix'], filename)


def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path).convert_alpha()
        _image_library[path] = image
    return image


def get_main_menu_bg():
    return get_image(build_image_path("mm_bg.png"))


def get_game_bg():
    return get_image(build_image_path("game_bg.png"))


def get_picker_sprites():
    return {
        'left_btn': get_image(build_image_path("widgets/left_btn.png")),
        'right_btn': get_image(build_image_path("widgets/right_btn.png"))
    }


def get_board_cell_sprites():
    return {
        'blank': get_image(build_image_path("cell.png")),
        'p1_won': get_image(build_image_path("p1_captured.png")),
        'p1_highlight': get_image(build_image_path("p1_highlighted.png")),
        'p1_marker': get_image(build_image_path("p1_marker.png")),
        'p2_won': get_image(build_image_path("p2_captured.png")),
        'p2_highlight': get_image(build_image_path("p2_highlighted.png")),
        'p2_marker': get_image(build_image_path("p2_marker.png"))
    }

