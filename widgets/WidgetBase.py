class WidgetBase(object):
    """ Abstract base class for all widgets
    """

    def __init__(self, x, y):
        self.left = int(x)
        self.top = int(y)

    def process_input(self, events, pressed_keys):
        # This method will receive all the events that happened since the last frame
        print("uh-oh, you didn't override this in the child class")

    def render(self, surface):
        # Instructions to render the widget
        print("uh-oh, you didn't override this in the child class")

    def global_to_local(self, global_x, global_y):
        """ Converts global screen coordinates to widget-localized coordinates
        (such that x=0 corresponds to the left edge of the widget and y=0 corresponds to the top"""
        return global_x - self.left, global_y - self.top
