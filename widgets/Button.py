import pygame
from .WidgetBase import WidgetBase
from services import SettingsService as Settings
from services import FontService
from scenes import DrawingUtils

class Button(WidgetBase):
    """ Widget for a clickable button with text

        x : integer : the left coordinate of the button
        y : integer: the top coordinate of the button
        width: integer : the width of the button
        height : integer : the height of the button
        callback: function : function to execute when the button is pressed
    """
    def __init__(self, x, y, width, height, text, callback):
        WidgetBase.__init__(self, x, y)
        self.width = int(width)
        self.height = int(height)
        self.callback = callback
        self.text = text

        self.depressed = False  # is the button pushed down?
        self.hover = False  # is the mouse hovering over the button?

    def process_input(self, events, pressed_keys):
        for event in events:
            # check if mouse is hovering over button
            if event.type == pygame.MOUSEMOTION:
                local_x, local_y = self.global_to_local(event.pos[0], event.pos[1])
                if 0 <= local_x <= self.width and 0 <= local_y <= self.height:
                    self.hover = True
                else:
                    self.hover = False
                    self.depressed = False
            # check if user has pushed the mouse button down on top of the button
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                local_x, local_y = self.global_to_local(event.pos[0], event.pos[1])
                if 0 <= local_x <= self.width and 0 <= local_y <= self.height:
                    self.depressed = True
            # check if mouse has been clicked on the button
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                local_x, local_y = self.global_to_local(event.pos[0], event.pos[1])
                if 0 <= local_x <= self.width and 0 <= local_y <= self.height:
                    # if the button was previously in the down state and is now up, then a button press has occurred
                    if self.depressed:
                        if self.callback: self.callback()

                self.depressed = False

    def render(self, surface):
        border_color = Settings.theme['widget_highlight']
        if self.hover: border_color = Settings.theme['tertiary']
        if self.depressed: border_color = Settings.theme['widget_background']

        DrawingUtils.aa_border_rounded_rect(surface, pygame.Rect(self.left, self.top, self.width, self.height),
                                            Settings.theme['widget_background'], border_color)

        font = FontService.get_regular_font(round(self.height * 0.40))
        font_color = Settings.theme['font']
        font_surface = font.render(self.text, False, font_color)
        font_size = font.size(self.text)
        font_left = self.left + 0.5*self.width - 0.5*font_size[0]
        font_top = self.top + 0.5*self.height - 0.5*font_size[1]
        surface.blit(font_surface, (font_left, font_top))

        

