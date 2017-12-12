import pygame, numpy
from .SceneBase import SceneBase
from .DrawingUtils import *
from widgets import Button
from models.game import Board, Move
from services import ImageService, FontService, SceneManager, SettingsService as Settings


class GameCompleted(SceneBase):
    """
    This scene shows the result of a game by displaying the completed board and a message about which player won
    """
    def __init__(self, game):
        SceneBase.__init__(self)
        # data needed to play the game
        self.game = game

        # calculate constants used for rendering
        # (these are all done in the fixed transform space, so we can safely use constants)
        self.MARGIN = 96
        self.CELL_SIZE = 83
        self.CELL_SPACING = 10
        self.LOCAL_BOARD_SPACING = 25
        self.BOARD_AREA_X = 1920 - self.MARGIN - 9*(self.CELL_SIZE + self.CELL_SPACING) - 2*self.LOCAL_BOARD_SPACING
        self.BOARD_AREA_Y = self.MARGIN
        self.FONT_SIZE = 48

        # bounding box for the player who won
        winner_box_width = 1920 - 3*self.MARGIN - self.BOARD_AREA_X
        winner_box_height = self.FONT_SIZE * 3
        self.WINNER_BOX = pygame.Rect(self.MARGIN, 0.5*1080 - self.MARGIN - winner_box_height, winner_box_width, winner_box_height)

        # "Name" of winning player
        winner = self.game.get_winner()
        if winner == Board.X:
            winner_name = "%s (X) wins!" % self.game.player1.name
        elif winner == Board.O:
            winner_name = "%s (O) wins!" % self.game.player2.name
        else:
            winner_name = "The Players Tie! Lame!"
        self.winner_text = FontService.get_regular_font(self.FONT_SIZE)
        self.winner_text_surface = self.winner_text.render(winner_name, False, Settings.theme['font'])
        self.winner_text_size = self.winner_text.size(winner_name)
        self.winner_text_location = (self.WINNER_BOX.centerx - 0.5 * self.winner_text_size[0],
                                     self.WINNER_BOX.top + 0.5 * self.winner_text_size[1] + 10)

        self.cell_sprites = ImageService.get_board_cell_sprites()
        for key in self.cell_sprites.keys():
            self.cell_sprites[key] = pygame.transform.scale(self.cell_sprites[key], (self.CELL_SIZE, self.CELL_SIZE))

        # compute cell bounding boxes - Each element is a 4-tuple (left, top, right, bottom)
        self.cell_locations = numpy.empty((3, 3, 3, 3), object)
        for i in list(range(0, 9)):
            metarow = i // 3
            row = i % 3
            for j in list(range(0, 9)):
                metacol = j // 3
                col = j % 3
                # compute the location of the cell in the grid and shift it into the board area
                location_x = (metacol * 3 + col)*(self.CELL_SIZE + self.CELL_SPACING) \
                    + self.LOCAL_BOARD_SPACING*metacol \
                    + self.BOARD_AREA_X

                location_y = (metarow * 3 + row) * (self.CELL_SIZE + self.CELL_SPACING) \
                     + self.LOCAL_BOARD_SPACING * metarow \
                     + self.BOARD_AREA_Y

                self.cell_locations[metarow][metacol][row][col] = (location_x, location_y, location_x + self.CELL_SIZE, location_y + self.CELL_SIZE)

        exit_btn = Button(self.WINNER_BOX.left, 0.5*1080 + self.MARGIN,
                          self.WINNER_BOX.width, self.WINNER_BOX.height,
                          "Exit", lambda: SceneManager.go_to_main_menu(self))
        self.widgets.append(exit_btn)

    def process_input(self, events, pressed_keys):
        for widget in self.widgets:
            widget.process_input(events, pressed_keys)

    def update(self):
        pass

    def render(self, screen):
        bg = ImageService.get_game_bg()
        screen.blit(bg, (0, 0))

        # render the box for the winner info
        if self.game.get_winner() == Board.X:
            border_color = Settings.theme['primary']
        elif self.game.get_winner() == Board.O:
            border_color = Settings.theme['secondary']
        else:
            border_color = Settings.theme['widget_highlight']

        # draw box
        aa_border_rounded_rect(screen, self.WINNER_BOX, Settings.theme['widget_background'], border_color)
        screen.blit(self.winner_text_surface, self.winner_text_location)  # name of winner

        # render the board
        current_player_symbol = self.game.active_player.number
        for i in list(range(0, 9)):
            metarow = i // 3
            row = i % 3
            for j in list(range(0, 9)):
                metacol = j // 3
                col = j % 3
                board_winner = self.game.board.check_cell(metarow, metacol)
                cell_owner = self.game.board.check_small_cell(metarow, metacol, row, col)
                move_object = Move(current_player_symbol, metarow, metacol, row, col)

                # compute the location of the cell in the grid and shift it into the board area
                location = self.cell_locations[metarow][metacol][row][col]
                location_x, location_y = location[0], location[1]

                # render the correct background for the cell:
                if board_winner == Board.X :
                    screen.blit(self.cell_sprites['p1_won'], (location_x, location_y))
                elif board_winner == Board.O:
                    screen.blit(self.cell_sprites['p2_won'], (location_x, location_y))
                else:
                    screen.blit(self.cell_sprites['blank'], (location_x, location_y))

                # render the cell's owner:
                if cell_owner == Board.X:
                    screen.blit(self.cell_sprites['p1_marker'], (location_x, location_y))
                elif cell_owner == Board.O:
                    screen.blit(self.cell_sprites['p2_marker'], (location_x, location_y))

        for widget in self.widgets:
            widget.render(screen)
