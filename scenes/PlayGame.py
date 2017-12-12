import pygame, numpy, threading, timeit
from .SceneBase import SceneBase
from .DrawingUtils import *
from models.game import Game, Board, Move, TimeLimitedBot
from services import ImageService, FontService, SceneManager, SettingsService as Settings
import javabridge

class PlayGame(SceneBase):
    """
    This scene shows a graphical representation of a game between two players
    If one or both of the players are human, then it allows that player to make moves with a mouse
    """
    def __init__(self, player1, player2):
        SceneBase.__init__(self)
        # data needed to play the game
        self.game = Game(player1, player2)
        # game object needs to be locked when the board is being rendered or when Bot players are ready to make a move
        self.game_lock = threading.Lock()
        self.bot_is_thinking = False
        self.bot_start_time = timeit.default_timer()
        self.ghost_move = None  # this Move object is used to show human players where their mouse is hovering

        # calculate constants used for rendering
        # (these are all done in the fixed transform space, so we can safely use constants)
        self.MARGIN = 96
        self.CELL_SIZE = 83
        self.CELL_SPACING = 10
        self.LOCAL_BOARD_SPACING = 25
        self.BOARD_AREA_X = 1920 - self.MARGIN - 9*(self.CELL_SIZE + self.CELL_SPACING) - 2*self.LOCAL_BOARD_SPACING
        self.BOARD_AREA_Y = self.MARGIN

        # bounding boxes for player info
        self.P1_BOX = pygame.Rect(self.MARGIN, self.MARGIN, 1920 - 3*self.MARGIN - self.BOARD_AREA_X,
                                  3*(self.CELL_SIZE + self.CELL_SPACING) - self.LOCAL_BOARD_SPACING )
        self.P2_BOX = pygame.Rect(self.MARGIN, self.MARGIN + 6*(self.CELL_SIZE + self.CELL_SPACING) + 2*self.LOCAL_BOARD_SPACING,
                                  1920 - 3*self.MARGIN - self.BOARD_AREA_X, 3*(self.CELL_SIZE + self.CELL_SPACING) - self.LOCAL_BOARD_SPACING )

        # text for player boxes
        self.FONT_SIZE = 48
        font_color = Settings.theme['font']

        self.p1_name = FontService.get_regular_font(self.FONT_SIZE)
        self.p1_name_surface = self.p1_name.render(self.game.player1.name, False, font_color)
        self.p1_name_size = self.p1_name.size(self.game.player1.name)
        self.p1_name_location = (self.P1_BOX.centerx - 0.5 * self.p1_name_size[0], self.P1_BOX.top + 0.5 * self.p1_name_size[1] + 10)

        self.p2_name = FontService.get_regular_font(self.FONT_SIZE)
        self.p2_name_surface = self.p2_name.render(self.game.player2.name, False, font_color)
        self.p2_name_size = self.p2_name.size(self.game.player2.name)
        self.p2_name_location = (self.P2_BOX.centerx - 0.5 * self.p2_name_size[0], self.P2_BOX.top + 0.5 * self.p2_name_size[1] + 10)

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

    def process_input(self, events, pressed_keys):
        for widget in self.widgets:
            widget.process_input(events, pressed_keys)

        # if the current player is a human, then respond to mouse events
        if not self.game.active_player.is_bot():
            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    # highlight the move that's about to be selected if the mouse moves over a cell
                    self.game_lock.acquire()  # acquire a lock while reading the board to get valid moves
                    valid_moves = self.game.get_valid_moves()
                    self.game_lock.release()
                    location = event.pos
                    ghost_move_found = False  # used to clear ghost marker if ghost move is not found
                    for move in valid_moves:
                        cell_location = self.cell_locations[move.metarow][move.metacol][move.row][move.col]
                        # check if mouse motion is within bounding box of cell
                        if cell_location[0] <= location[0] <= cell_location[2] and cell_location[1] <= location[1] <= cell_location[3]:
                            self.ghost_move = move
                            ghost_move_found = True
                    if not ghost_move_found:
                        self.ghost_move = None

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.ghost_move:
                        self.game.make_move(self.ghost_move)

    def update(self):
        if self.game.is_game_over():
            SceneManager.go_to_game_completed(self, self.game)

        self.game_lock.acquire()
        bots_turn = self.game.active_player.is_bot()
        self.game_lock.release()
        if bots_turn and not self.bot_is_thinking and not self.game.is_game_over():
            self.bot_is_thinking = True
            self.bot_start_time = timeit.default_timer()
            move = self.game.active_player.compute_next_move(self.game.board, self.game.get_valid_moves())
            self.game_lock.acquire()
            self.game.make_move(move)
            self.game_lock.release()
            self.bot_is_thinking = False

    def render(self, screen):
        bg = ImageService.get_game_bg()
        screen.blit(bg, (0, 0))

        # render the info box for player1
        border_color = Settings.theme['primary'] if self.game.active_player.number == Board.X else Settings.theme['widget_highlight']
        # draw box
        aa_border_rounded_rect(screen, self.P1_BOX, Settings.theme['widget_background'], border_color)
        screen.blit(self.p1_name_surface, self.p1_name_location)  # player name
        # render the timestamp for player 1
        timestamp = FontService.get_regular_font(self.FONT_SIZE)

        if isinstance(self.game.active_player, TimeLimitedBot) and self.game.active_player.number == Board.X:
            time_left = -1
            if self.game.active_player.is_bot():
                now = timeit.default_timer()
                time_left = self.game.active_player.time_limit - (now - self.bot_start_time)

            time_string = seconds_to_timestamp(time_left)
            p1_time = timestamp.render(time_string, False, Settings.theme['font'])
            p1_time_size = timestamp.size(time_string)
            p1_time_location = (self.P1_BOX.centerx - 0.5 * p1_time_size[0], self.P1_BOX.bottom - p1_time_size[1] - 10)
            screen.blit(p1_time, p1_time_location)

        # render the info box for player2
        border_color = Settings.theme['secondary'] if self.game.active_player.number == Board.O else Settings.theme['widget_highlight']
        # draw box
        aa_border_rounded_rect(screen, self.P2_BOX, Settings.theme['widget_background'], border_color)
        screen.blit(self.p2_name_surface, self.p2_name_location) # player 2's name
        # render the timestamp for player 2
        if isinstance(self.game.active_player, TimeLimitedBot) and self.game.active_player.number == Board.O:
            time_left = -1
            if self.game.active_player.is_bot():
                now = timeit.default_timer()
                time_left = self.game.active_player.time_limit - (now - self.bot_start_time)
            time_string = seconds_to_timestamp(time_left)
            p2_time = timestamp.render(time_string, False, Settings.theme['font'])
            p2_time_size = timestamp.size(time_string)
            p2_time_location = (self.P2_BOX.centerx - 0.5 * p2_time_size[0], self.P2_BOX.bottom - p2_time_size[1] - 10)
            screen.blit(p2_time, p2_time_location)

        # render the board
        self.game_lock.acquire()  # need to read values from the board while rendering
        valid_moves = self.game.get_valid_moves()
        current_player = self.game.active_player
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
                elif move_object in valid_moves:
                    if current_player.number == Board.X:
                        screen.blit(self.cell_sprites['p1_highlight'], (location_x, location_y))
                    if current_player.number == Board.O:
                        screen.blit(self.cell_sprites['p2_highlight'], (location_x, location_y))
                else:
                    screen.blit(self.cell_sprites['blank'], (location_x, location_y))

                # render the cell's owner:
                if cell_owner == Board.X:
                    screen.blit(self.cell_sprites['p1_marker'], (location_x, location_y))
                elif cell_owner == Board.O:
                    screen.blit(self.cell_sprites['p2_marker'], (location_x, location_y))

                # render a ghost move if there is one:
                if self.ghost_move is not None:
                    move_location = self.cell_locations[self.ghost_move.metarow][self.ghost_move.metacol][self.ghost_move.row][self.ghost_move.col]
                    if self.ghost_move.player == Board.X:
                        screen.blit(self.cell_sprites['p1_marker'], (move_location[0], move_location[1]))
                    else:
                        screen.blit(self.cell_sprites['p2_marker'], (move_location[0], move_location[1]))

        self.game_lock.release()  # rendering is done

        for widget in self.widgets:
            widget.render(screen)


def seconds_to_timestamp(seconds):
    if seconds < 0:
        return "Unlimited"

    whole_s = round(seconds)
    s = whole_s % 60
    if s < 10:
        s = "0%s" % s
    m = whole_s // 60
    return "%s:%s" % (m, s)
