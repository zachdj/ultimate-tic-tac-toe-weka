import pygame
from .SceneBase import SceneBase
from services import ImageService, SceneManager
from widgets import Button


class MainMenu(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        # get screen dimensions to position buttons
        s_width = 1920
        s_height = 1080
        center_x = s_width*0.5
        center_y = s_height*0.5
        btn_size = s_height*0.2

        single_player_btn = Button(center_x - s_width*0.2, center_y - 1.5*btn_size, s_width*0.4, s_height*0.1,
                                   "Start a Game", lambda: SceneManager.go_to_setup_game(self))

        experiment_btn = Button(center_x - s_width * 0.2, center_y - 0.5*btn_size, s_width * 0.4, s_height * 0.1,
                                "Run Experiment", lambda: SceneManager.go_to_setup_experiment(self))

        # settings_btn = Button(center_x - s_width * 0.2, center_y + .5*btn_size, s_width * 0.4, s_height * 0.1,
        #                         "Settings", lambda: print("Change some settings!"))

        quit_btn = Button(center_x - s_width * 0.2, center_y + .5*btn_size, s_width * 0.4, s_height * 0.1,
                                "Quit", lambda: pygame.event.post(pygame.event.Event(pygame.QUIT, {})) )

        self.widgets.extend([single_player_btn, experiment_btn, quit_btn])

    def process_input(self, events, pressed_keys):
        for widget in self.widgets:
            widget.process_input(events, pressed_keys)

    def update(self):
        pass

    def render(self, screen):
        bg = ImageService.get_main_menu_bg()
        screen.blit(bg, (0, 0))
        for widget in self.widgets:
            widget.render(screen)
