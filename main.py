import pygame

import Move
import drawGame
import sys

board_width = 400
board_height = 400
field_size = board_height // 8
img = {}
counter = 0


def load_pieces():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        img[piece] = pygame.transform.scale(pygame.image.load("../Schach/img/" + piece + ".png"),(field_size, field_size))

def main():
    pygame.init()
    screen = pygame.display.set_mode((board_width, board_height))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    game_state = drawGame.GameState()
    legal_moves = game_state.get_legal_moves()

    load_pieces()

    run_game(clock, game_state, legal_moves, screen)


def run_game(clock, game_state, legal_moves, screen):
    global counter
    running = True
    selected_piece = ()
    player_clicks = []
    game_over = False
    move_made = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    col = event.pos[0] // field_size
                    row = event.pos[1] // field_size
                    if selected_piece == (row, col):
                        selected_piece = ()
                        player_clicks = []
                    else:
                        selected_piece = (row, col)
                        player_clicks.append(selected_piece)
                    if len(player_clicks) == 2:
                        move = Move.Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(legal_moves)):
                            if move == legal_moves[i]:
                                game_state.make_move(legal_moves[i])
                                move_made = True
                                selected_piece = ()
                                player_clicks = []
                        if not move_made:
                            player_clicks = [selected_piece]

        if move_made:
            legal_moves = game_state.get_legal_moves()
            move_made = False

        draw_game(screen, game_state, legal_moves, selected_piece)

        if game_state.checkmate:
            game_over = True
            if game_state.white_to_move:
                print("Black wins")
            else:
                print("White wins")

        clock.tick(30)

        if counter < 30:
            counter += 1
        else:
            counter = 0
        pygame.display.flip()


def draw_game(screen, game_state, legal_moves, selected_piece):
    draw_board(screen)
    draw_selected_piece(screen, selected_piece)
    draw_legal_moves(screen, game_state, legal_moves, selected_piece)
    draw_piece(screen, game_state.board)
    if game_state.is_in_check():
        if game_state.white_to_move:
            draw_flash_king(screen, game_state.white_king_location)
        else:
            draw_flash_king(screen, game_state.black_king_location)

def draw_board(screen):
    global colors
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for row in range(8):
        for column in range(8):
            color = colors[((row + column) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(column * field_size, row * field_size, field_size, field_size))


def draw_selected_piece(screen, selected_piece):
    if selected_piece:
        row, col = selected_piece
        pygame.draw.rect(screen, pygame.Color("blue"), (col * field_size, row * field_size, field_size, field_size), 3)


def draw_legal_moves(screen, game_state, legal_moves, selected_piece):
    for move in legal_moves:
        if selected_piece == (move.start_row, move.start_col):
            pygame.draw.rect(screen, pygame.Color("green"),(move.end_col * field_size, move.end_row * field_size, field_size, field_size), 3)
            if game_state.board[move.end_row][move.end_col] != "--":
                pygame.draw.rect(screen, pygame.Color("red"),(move.end_col * field_size, move.end_row * field_size, field_size, field_size), 3)


def draw_piece(screen, board):
    for row in range(8):
        for column in range(8):
            piece = board[row][column]
            if piece != "--":
                screen.blit(img[piece], pygame.Rect(column * field_size, row * field_size, field_size, field_size))


def draw_flash_king(screen, king_position):
    row, col = king_position
    flash_color = pygame.Color("red") if counter % 4 < 2 else pygame.Color("White")
    pygame.draw.rect(screen, flash_color, (col * field_size, row * field_size, field_size, field_size), 3)


if __name__ == "__main__":
    main()
