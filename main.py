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
    animate = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    col = event.pos[0] // field_size    #Col position of the mouse
                    row = event.pos[1] // field_size    #Row position of the mouse
                    if selected_piece == (row, col):
                        selected_piece = () #unselects the piece
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
                                animate = True
                                selected_piece = () #After a move was made, it unselects the piece
                                player_clicks = []
                                break
                        if not move_made:
                            player_clicks = [selected_piece]
                            move_made = False

        if move_made:
            if animate:
                animate_move(game_state.move_log[-1], screen, game_state.board, clock)
            legal_moves = game_state.get_legal_moves() #getting all legal moves
            move_made = False

        draw_game(screen, game_state, legal_moves, selected_piece)

        if game_state.checkmate:    #looking for a checkmate
            if game_state.white_to_move: #after detecting a checkmate and white has to move, it is a checkmate for black
                draw_checkmate_message(screen, clock, custom_text="Black wins by checkmate!")
            else:
                draw_checkmate_message(screen, clock, custom_text="White wins by checkmate!")

        clock.tick(30)

        #animation for the checkanimation

        if counter < 30:
            counter += 1
        else:
            counter = 0
        counter = 0
        pygame.display.flip()

#draw everything
def draw_game(screen, game_state, legal_moves, selected_piece):
    draw_board(screen)  #drawing the board
    draw_selected_piece(screen, selected_piece) #draw the selected piece
    draw_legal_moves(screen, game_state, legal_moves, selected_piece) #draw all possible moves
    draw_piece(screen, game_state.board) #draw all pieces
    if game_state.is_in_check():
        if game_state.white_to_move:
            draw_flash_king(screen, game_state.white_king_location)
        else:
            draw_flash_king(screen, game_state.black_king_location)

#draw the board
def draw_board(screen):
    global colors
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for row in range(8):
        for column in range(8):
            color = colors[((row + column) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(column * field_size, row * field_size, field_size, field_size))

#draw the checkmate message
def draw_checkmate_message(screen, clock, custom_text=None):
    font = pygame.font.Font(None, 36)
    checkmate_text = font.render("Checkmate!", True, pygame.Color("red"))
    screen.blit(checkmate_text, (board_width // 2 - checkmate_text.get_width() // 2, board_height // 2 - checkmate_text.get_height() // 2))

    if custom_text:
        custom_message = font.render(custom_text, True, pygame.Color("blue"))
        screen.blit(custom_message, (board_width // 2 - custom_message.get_width() // 2, board_height // 2 + checkmate_text.get_height()))

    pygame.display.flip()
    pygame.time.wait(3000)

#draw the selected piece
def draw_selected_piece(screen, selected_piece):
    if selected_piece:
        row, col = selected_piece
        pygame.draw.rect(screen, pygame.Color("blue"), (col * field_size, row * field_size, field_size, field_size), 3)

#draw all legal moves
def draw_legal_moves(screen, game_state, legal_moves, selected_piece):
    for move in legal_moves:
        if selected_piece == (move.start_row, move.start_col):
            pygame.draw.rect(screen, pygame.Color("green"),(move.end_col * field_size, move.end_row * field_size, field_size, field_size), 3)
            if game_state.board[move.end_row][move.end_col] != "--":
                pygame.draw.rect(screen, pygame.Color("red"),
                                 (move.end_col * field_size, move.end_row * field_size, field_size, field_size), 3)

#draw pieces
def draw_piece(screen, board):
    for row in range(8):
        for column in range(8):
            piece = board[row][column]
            if piece != "--":
                screen.blit(img[piece], pygame.Rect(column * field_size, row * field_size, field_size, field_size))

#draw king check animation
def draw_flash_king(screen, king_position):
    row, col = king_position
    flash_color = pygame.Color("red") if counter % 4 < 2 else pygame.Color("White")
    pygame.draw.rect(screen, flash_color, (col * field_size, row * field_size, field_size, field_size), 3)

#a little animation, where you have a better visuality of the moves
def animate_move(move, screen, board, clock):
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 3  # frames to move one square
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1): #without the + 1, it seems to be a little laggy
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        draw_board(screen)
        draw_piece(screen, board)

        color = colors[(move.end_row + move.end_col) % 2]
        end_square = pygame.Rect(move.end_col * field_size, move.end_row * field_size, field_size, field_size)
        pygame.draw.rect(screen, color, end_square)

        # draw moving piece
        screen.blit(img[move.piece_moved], pygame.Rect(col * field_size, row * field_size, field_size, field_size))
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
