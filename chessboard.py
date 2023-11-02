import pygame

pygame.init()
font = pygame.font.Font(None, 36)


class Square:
    def __init__(self, grid_size, coord, piece):
        x, y = coord[0] * grid_size, coord[1] * grid_size
        self.rect = pygame.Rect(x, y, grid_size, grid_size)
        self.piece = piece
        self.playable = False
        if (coord[0] + coord[1]) % 2 == 0:
            print("yellow")
            self.colour = (255, 255, 0)  # yellow
        else:
            print("orange")
            self.colour = (255, 165, 0)  # orange


class ChessBoard:
    def __init__(self, grid_size):
        self.data = None
        self.selected = None
        initial_board = {}
        pieces_main = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        pieces_pawn = 'p'

        # Fill board with pieces and empty spaces
        for i in range(8):
            for j in range(8):
                piece = None
                if i == 0:  # Main black pieces
                    piece = pieces_main[j]
                elif i == 1:  # Black pawns
                    piece = pieces_pawn
                elif 2 <= i <= 5:  # Empty rows
                    piece = None
                elif i == 6:  # White pawns
                    piece = pieces_pawn.upper()
                elif i == 7:  # Main white pieces
                    piece = pieces_main[j].upper()

                initial_board[(j, i)] = Square(grid_size, (j, i), piece)
        self.data = initial_board

    def update(self):
        pass

    def draw(self, game_window):
        mouse_pos = pygame.mouse.get_pos()
        for coord in self.data:
            pygame.draw.rect(game_window, self.data[coord].colour, self.data[coord].rect)

            # Highlight squares with the .playable attribute set to True
            if self.data[coord].playable:
                highlight_color = (0, 255, 0, 120)  # White with 100 alpha (semi-transparent)
                highlight_surface = pygame.Surface(self.data[coord].rect.size, pygame.SRCALPHA)
                highlight_surface.fill(highlight_color)
                game_window.blit(highlight_surface, self.data[coord].rect.topleft)

            # Highlight square the mouse is hovering over
            if self.data[coord].rect.collidepoint(mouse_pos):
                highlight_color = (0, 0, 255, 120)  # White with 100 alpha (semi-transparent)
                highlight_surface = pygame.Surface(self.data[coord].rect.size, pygame.SRCALPHA)
                highlight_surface.fill(highlight_color)
                game_window.blit(highlight_surface, self.data[coord].rect.topleft)

        if self.selected:
            highlight_color = (0, 0, 255, 120)  # White with 100 alpha (semi-transparent)
            highlight_surface = pygame.Surface(self.data[self.selected].rect.size, pygame.SRCALPHA)
            highlight_surface.fill(highlight_color)
            game_window.blit(highlight_surface, self.data[self.selected].rect.topleft)

        # If there's a piece on the square, draw its letter
        for coord in self.data:
            if self.data[coord].piece:
                text_surf = font.render(self.data[coord].piece, True, (0, 0, 0))
                text_rect = text_surf.get_rect(center=self.data[coord].rect.center)
                game_window.blit(text_surf, text_rect)

    def check_playability(self):
        if self.selected:
            selected_piece = self.data[self.selected].piece
            x, y = self.selected
            for square in self.data.values():
                square.playable = False

            # White Pawn
            if selected_piece == "P":
                # One square forward
                if 0 <= y - 1 < 8 and not self.data[(x, y - 1)].piece:
                    self.data[(x, y - 1)].playable = True

                # Two squares forward from the initial position
                if y == 6 and not self.data[(x, y - 1)].piece and not self.data[(x, y - 2)].piece:
                    self.data[(x, y - 2)].playable = True

                # Capture diagonally left
                if 0 <= x - 1 < 8 and 0 <= y - 1 < 8 and self.data[(x - 1, y - 1)].piece and self.data[(x - 1, y - 1)].piece.islower():
                    self.data[(x - 1, y - 1)].playable = True

                # Capture diagonally right
                if 0 <= x + 1 < 8 and 0 <= y - 1 < 8 and self.data[(x + 1, y - 1)].piece and self.data[(x + 1, y - 1)].piece.islower():
                    self.data[(x + 1, y - 1)].playable = True

                print("white pawn")

            # Black Pawn
            elif selected_piece == "p":
                # One square forward
                if 0 <= y + 1 < 8 and not self.data[(x, y + 1)].piece:
                    self.data[(x, y + 1)].playable = True

                # Two squares forward from the initial position
                if y == 1 and not self.data[(x, y + 1)].piece and not self.data[(x, y + 2)].piece:
                    self.data[(x, y + 2)].playable = True

                # Capture diagonally left
                if 0 <= x - 1 < 8 and 0 <= y + 1 < 8 and self.data[(x - 1, y + 1)].piece and self.data[(x - 1, y + 1)].piece.isupper():
                    self.data[(x - 1, y + 1)].playable = True

                # Capture diagonally right
                if 0 <= x + 1 < 8 and 0 <= y + 1 < 8 and self.data[(x + 1, y + 1)].piece and self.data[(x + 1, y + 1)].piece.isupper():
                    self.data[(x + 1, y + 1)].playable = True

                print("black pawn")

            # Rooks
            elif selected_piece in ["r", "R"]:
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                for dx, dy in directions:
                    for i in range(1, 8):
                        new_x, new_y = x + i * dx, y + i * dy

                        # Check if the move is inside the self
                        if 0 <= new_x < 8 and 0 <= new_y < 8:
                            target_square = self.data[(new_x, new_y)]

                            # If the square is empty, it's a playable move
                            if not target_square.piece:
                                target_square.playable = True
                            else:
                                # If the square contains an opponent's piece, it's a playable move but
                                # the rook cannot move further in this direction
                                if selected_piece.isupper() != target_square.piece.isupper():
                                    target_square.playable = True
                                break
                        else:
                            break
                print("rook")

            # Knights
            elif selected_piece in ["n", "N"]:
                knight_moves = [(1, 2), (2, 1), (-1, 2), (2, -1), (-1, -2), (-2, -1), (1, -2), (-2, 1)]
                for move in knight_moves:
                    new_x, new_y = x + move[0], y + move[1]
                    if 0 <= new_x < 8 and 0 <= new_y < 8:
                        target_square = self.data[(new_x, new_y)]
                        # Check if the target square doesn't have a piece of the same color
                        if not target_square.piece or (selected_piece.isupper() != target_square.piece.isupper()):
                            target_square.playable = True
                print("knight")

            # Bishops
            elif selected_piece in ["b", "B"]:
                directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # NE, SE, NW, SW

                for dx, dy in directions:
                    i = 1
                    while True:
                        new_x, new_y = x + dx * i, y + dy * i
                        if 0 <= new_x < 8 and 0 <= new_y < 8:  # within self
                            target_square = self.data[(new_x, new_y)]

                            # Stop if there's a piece
                            if target_square.piece:
                                # If the piece isn't of the same color, it can be captured
                                if selected_piece.isupper() != target_square.piece.isupper():
                                    target_square.playable = True
                                break  # Stop in this direction

                            target_square.playable = True
                        else:  # If outside the board
                            break
                        i += 1
                print("bishop")

            # Queens (Combination of rook and bishop)
            elif selected_piece in ["q", "Q"]:
                # Rook part
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Right, Left, Down, Up
                for dx, dy in directions:
                    i = 1
                    while True:
                        new_x, new_y = x + dx * i, y + dy * i
                        if 0 <= new_x < 8 and 0 <= new_y < 8:  # within board
                            target_square = self.data[(new_x, new_y)]

                            # Stop if there's a piece
                            if target_square.piece:
                                # If the piece isn't of the same color, it can be captured
                                if selected_piece.isupper() != target_square.piece.isupper():
                                    target_square.playable = True
                                break  # Stop in this direction

                            target_square.playable = True
                        else:  # If outside the board
                            break
                        i += 1

                # Bishop part
                directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # NE, SE, NW, SW
                for dx, dy in directions:
                    i = 1
                    while True:
                        new_x, new_y = x + dx * i, y + dy * i
                        if 0 <= new_x < 8 and 0 <= new_y < 8:  # within board
                            target_square = self.data[(new_x, new_y)]

                            # Stop if there's a piece
                            if target_square.piece:
                                # If the piece isn't of the same color, it can be captured
                                if selected_piece.isupper() != target_square.piece.isupper():
                                    target_square.playable = True
                                break  # Stop in this direction

                            target_square.playable = True
                        else:  # If outside the board
                            break
                        i += 1
                print("queen")

            # Kings
            elif selected_piece in ["k", "K"]:
                king_moves = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
                for move in king_moves:
                    new_x, new_y = x + move[0], y + move[1]
                    if 0 <= new_x < 8 and 0 <= new_y < 8:
                        target_square = self.data[(new_x, new_y)]

                        # If the square is empty or contains a piece of the opposite color
                        if not target_square.piece or (selected_piece.isupper() != target_square.piece.isupper()):
                            target_square.playable = True
                print("king")

    def select(self, mouse_pos):
        if not mouse_pos:
            for square in self.data.values():
                square.playable = False
            self.selected = None
            return

        for coord in self.data:
            if self.data[coord].rect.collidepoint(mouse_pos):
                if self.data[coord].playable:
                    print("move")
                    self.data[coord].piece = self.data[self.selected].piece
                    self.data[self.selected].piece = None
                    self.selected = None
                    for square in self.data.values():
                        square.playable = False
                else:
                    self.selected = coord
