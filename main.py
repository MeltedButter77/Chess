import pygame
from chessboard import ChessBoard

pygame.init()

window_size = (800, 800)
game_window = pygame.display.set_mode(window_size)
grid_size = window_size[0] / 8
clock = pygame.time.Clock()
fps = 60

board = ChessBoard(grid_size)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                board.select(event.pos)
                board.check_playability()
            elif event.button == 3:
                board.select(None)

    board.update()
    board.draw(game_window)

    pygame.display.update()

    clock.tick(fps)
    real_fps = clock.get_fps()
    pygame.display.set_caption(f'FPS: {real_fps:.2f}')
