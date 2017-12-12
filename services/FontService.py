"""
The FontService singleton handles the loading of font assets
It retrieves fonts using logical names (e.g. get_regular_font() )
The actual font returned from a logical call can vary based on the selected theme

Once a font is loaded from a file, it is kept in memory in case it is requested again
"""

import pygame
import os
import services.SettingsService as Settings


_font_library = {}


def build_font_path(filename):
    return "assets/fonts/%s/%s" % (Settings.theme['path_prefix'], filename)


def get_font(path, size):
    global _font_library
    font_key = "%s,%s" % (path, size)
    font = _font_library.get(font_key)
    if font == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        font = pygame.font.Font(canonicalized_path, size)
        _font_library[font_key] = font
    return font


def get_regular_font(size):
    return get_font(build_font_path("regular.ttf"), size)
