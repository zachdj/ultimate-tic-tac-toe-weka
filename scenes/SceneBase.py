# Credit for scene management code: http://www.nerdparadise.com/programming/pygame/part7

class SceneBase(object):
    """ Abstract base class for all scenes

    Scenes are the View and Controller layers of the MVC architecture wrapped into a single class
    """

    def __init__(self):
        self.next = self
        self.widgets = []

    def add_widget(self, widget):
        self.widgets.append(widget)

    def process_input(self, events, pressed_keys):
        # This method will receive all the events that happened since the last frame
        print("uh-oh, you didn't override this in the child class")

    def update(self):
        # Game logic goes here.  What needs to change since last frame?
        print("uh-oh, you didn't override this in the child class")

    def render(self, screen):
        # Instructions for rendering this scene onto the main display surface
        print("uh-oh, you didn't override this in the child class")

    def switch_to_scene(self, next_scene):
        # Switches to the given scene
        self.next = next_scene

    def terminate(self):
        # called from the main game loop when the pygame.QUIT event is fired
        self.switch_to_scene(None)