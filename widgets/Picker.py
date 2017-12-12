import pygame
from .WidgetBase import WidgetBase
from scenes.DrawingUtils import aa_border_rounded_rect
from services import SettingsService as Settings
from services import ImageService
from services import FontService


class Picker(WidgetBase):
    def __init__(self, x, y, width, height, values, callback=None, wrap_values=True, selected_index=0):
        """ Picker widget.  Allows user to make a selection from a discrete set of options

        The textbox will be 80% of the widget width.  The remaining 20% will be split for left/right buttons on each side
        The data for the picker should be a 1D array of objects with the following format:
            [
                { data: first_object, title: "string to display", ...},
                { data: second_object, title: "different string", ...},
                ...
            ]

        :param x: integer left coordinate of the picker
        :param y: integer top coordinate of the picker
        :param width: the maximum width of the picker
        :param height: the height of the picker
        :param values: array of selectable options with the following format:
            [
                { data: first_object, title: "string to display", ...},
                { data: second_object, title: "different string", ...},
                ...
            ]
        :param callback: optional function to call when the selection changes.  The function will be passed the data attribute of the current selection
        :param wrap_values: boolean controlling whether the Picker will "wrap" when the selected index is out of range.
            For example, suppose the options are [R, G, B] and the picker is currently at B.  If wrap_values is enabled,
            then clicking the right button will update the selected value to R.  Otherwise, it will remain at B.
        :param selected_index: the index of the option which will initially be selected.  Defaults to 0 (the first item)
        """
        WidgetBase.__init__(self, x, y)
        self.WIDTH = int(width)
        self.HEIGHT = int(height)
        self.callback = callback
        self.values = values
        self.wrap_values = wrap_values
        if len(self.values) <= 0:
            raise Exception("You must pass at least one selectable value when constructing a Picker widget")
        self.selected_index = selected_index
        # Define constants used to control rendering
        self.BTN_WIDTH = int(0.1*width)  # percentage of width that left/right btn will take up
        self.BORDER_WEIGHT = 3  # thickness of the bordering box around the text
        self.TEXTBOX_WIDTH = int(width - 3*self.BTN_WIDTH)

        self.sprites = ImageService.get_picker_sprites()
        self.left_btn = pygame.transform.scale(self.sprites['left_btn'], (self.BTN_WIDTH, self.HEIGHT))
        self.right_btn = pygame.transform.scale(self.sprites['right_btn'], (self.BTN_WIDTH, self.HEIGHT))

    def process_input(self, events, pressed_keys):
        for event in events:
            # check if user has pressed either left or the right button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos[0], event.pos[1]
                if self.left <= x < self.left + self.BTN_WIDTH and self.top <= y < self.top + self.HEIGHT:
                    # left button clicked
                    self.selected_index -= 1
                    # handle edge case:
                    if self.selected_index < 0 and self.wrap_values:
                        self.selected_index = len(self.values) - 1
                    elif self.selected_index < 0:
                        self.selected_index = 0

                    if self.callback is not None:
                        self.callback(self.values[self.selected_index])

                elif self.left + self.WIDTH - self.BTN_WIDTH <= x < self.left + self.WIDTH and self.top <= y < self.top + self.HEIGHT:
                    # right button clicked
                    self.selected_index += 1
                    # handle edge case:
                    if self.selected_index >= len(self.values) and self.wrap_values:
                        self.selected_index = 0
                    elif self.selected_index >= len(self.values):
                        self.selected_index = len(self.values) - 1

                    if self.callback is not None:
                        self.callback(self.values[self.selected_index])

    def render(self, surface):
        # draw the textbox with the current label:
        textbox_rect = pygame.Rect(self.left + int(1.5*self.BTN_WIDTH), self.top, self.TEXTBOX_WIDTH, self.HEIGHT)
        aa_border_rounded_rect(surface, textbox_rect, Settings.default_theme['widget_background'],
                               Settings.default_theme['widget_highlight'], 0.4, self.BORDER_WEIGHT)

        surface.blit(self.left_btn, (self.left, self.top))
        surface.blit(self.right_btn, (self.left + self.WIDTH - self.BTN_WIDTH, self.top))

        selected_option = self.values[self.selected_index]
        text = selected_option['title']

        font = FontService.get_regular_font(round(self.HEIGHT * 0.30))
        font_color = Settings.theme['font']
        font_surface = font.render(text, False, font_color)
        font_size = font.size(text)
        font_left = self.left + 0.5 * self.WIDTH - 0.5 * font_size[0]
        font_top = self.top + 0.5 * self.HEIGHT - 0.5 * font_size[1]
        surface.blit(font_surface, (font_left, font_top))

    def set_values(self, new_values):
        """
        Sets the array of possible values that can be picked from this picker.  If the current index is valid,
        then it will be preserved.  Otherwise the index will be set to zero.
        In either case, the callback will be executed with the currently selected value

        :param new_values: array of selectable options with the following format:
            [
                { data: first_object, title: "string to display", ...},
                { data: second_object, title: "different string", ...},
                ...
            ]

        :return: None
        """

        if len(new_values) <= 0:
            raise Exception("The Picker widget must have at least one selectable value")

        self.values = new_values
        if len(new_values) <= self.selected_index:
            self.selected_index = 0

        if self.callback is not None:
            self.callback(self.values[self.selected_index])

    def get_selected_value(self):
        return self.values[self.selected_index]
