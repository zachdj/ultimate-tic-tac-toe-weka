from pygame import *
"""
This module contains utility functions for drawing certain shapes that are difficult to achieve with the regular pygame
drawing API.
"""


def aa_filled_rounded_rect(surface,rect,color,radius=0.4):

    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)
    http://pygame.org/project-AAfilledRoundedRect-2349-.html

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = Rect(rect)
    color        = Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = Surface(rect.size,SRCALPHA)

    circle       = Surface([min(rect.size)*3]*2,SRCALPHA)
    draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)


def aa_border_rounded_rect(surface, rect, fill_color, border_color, radius=0.4, border_weight=4):
    border_rect = rect
    fill_rect = Rect(rect.left + border_weight, rect.top + border_weight, rect.width - border_weight*2, rect.height - border_weight*2)
    aa_filled_rounded_rect(surface, border_rect, border_color, radius)
    aa_filled_rounded_rect(surface, fill_rect, fill_color, radius)