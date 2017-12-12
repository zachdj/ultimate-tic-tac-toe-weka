import pygame
import threading
import settings as env_settings

# starting a jvm is required for doing anything with the weka wrappers.
# TODO: Hopefully we can ditch this in the future caz it sucks
import weka.core.jvm as jvm
jvm.start()

from services import SceneManager, ApplicationStatusService as Status

pygame.init()
pygame_display_mode = pygame.RESIZABLE
# Theres a bug in pygame when using MAC OS - resizable move runs incredibly poorly
if env_settings.USING_OSX:
    pygame_display_mode = pygame.FULLSCREEN
screen = pygame.display.set_mode((0, 0), pygame_display_mode)
screen_size = screen.get_size()


# we will draw on a surface of fixed size then transform it to the actual display size
LOGICAL_WIDTH = 1920
LOGICAL_HEIGHT = 1080
display = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT))
clock = pygame.time.Clock()

active_scene = SceneManager.get_main_menu_instance()


def render_scene():
    while active_scene is not None:
        active_scene.render(display)
        # check if screen size has changed
        global screen_size
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                screen_size = event.size
            else:
                pygame.event.post(event)
        scaled_display = pygame.transform.scale(display, screen_size)
        screen.blit(scaled_display, (0, 0))
        pygame.display.flip()

render_thread = threading.Thread(target=render_scene)
render_thread.start()

while active_scene != None:
    pressed_keys = pygame.key.get_pressed()

    # Event filtering
    filtered_events = []
    for event in pygame.event.get():
        quit_attempt = False
        if event.type == pygame.QUIT:
            quit_attempt = True
        elif event.type == pygame.VIDEORESIZE:
            screen_size = event.size
        elif event.type == pygame.KEYDOWN:
            alt_pressed = pressed_keys[pygame.K_LALT] or \
                          pressed_keys[pygame.K_RALT]
            if event.key == pygame.K_ESCAPE:
                quit_attempt = True
            elif event.key == pygame.K_F4 and alt_pressed:
                quit_attempt = True
        elif event.type in [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]:
            # transform from actual screen coordinates to logical coordinates
            scaling_factor_x = LOGICAL_WIDTH / screen_size[0]
            scaling_factor_y = LOGICAL_HEIGHT / screen_size[1]
            event.pos = (event.pos[0]*scaling_factor_x, event.pos[1]*scaling_factor_y)

        if quit_attempt:
            active_scene.terminate()
            Status.terminated = True
            jvm.stop()
        else:
            filtered_events.append(event)

    active_scene.process_input(filtered_events, pressed_keys)
    active_scene.update()
    # active_scene.render(display)

    active_scene = active_scene.next

    # pygame.display.flip()
    clock.tick(60)   # run at a max of 60 fps