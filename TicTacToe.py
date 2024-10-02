import pygame

board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
current_player = 'X'
winning_player = ''
count = 2
playing_colour = (225, 0, 87)
play_count = 0

converter_to_array = {
    (39, 3): (0, 0), (189, 3): (0, 1), (339, 3): (0, 2),
    (39, 153): (1, 0), (189, 153): (1, 1), (339, 153): (1, 2),
    (39, 303): (2, 0), (189, 303): (2, 1), (339, 303): (2, 2)
}

pygame.font.init()
pygame.init()

w_width = 450
w_height = 550
white = (255, 255, 255)

base_font = pygame.font.SysFont('comicsans', 20)
x_font = pygame.font.SysFont('comicsans', 100)
reset_font = pygame.font.SysFont('comicsans', 120)

window = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption('Tic Tac Toe')
window.fill(white)
pygame.display.flip()

bottom_text = base_font.render('Player ' + current_player + ', choose a square...', 1, (0, 0, 0))
window.blit(bottom_text, (10, w_height - 80))

grid_array = [(10, 10), (160, 10), (310, 10),
              (10, 160), (160, 160), (310, 160),
              (10, 310), (160, 310), (310, 310)]


# Drawing grid:
def drawGrid():
    block_size = 150
    for x in range(0, w_width, block_size):
        for y in range(0, (w_height - 100), block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(window, (0, 0, 0), rect, 1)
    pass


def multiplayer():
    global current_player, playing_colour, play_count, count, run
    check = True
    run = True
    while check_for_win(board) == False and check == True:
        if check_full(board) == True:
            check = False

        window.fill(white, rect=[10, w_height - 80, 300, 200])

        if count % 2 == 0:
            current_player = 'X'
            playing_colour = (225, 0, 87)
        else:
            current_player = 'O'
            playing_colour = (0, 89, 223)

        bottom_text = base_font.render('Player ' + current_player + ', choose a square...', 1, (0, 0, 0))
        window.blit(bottom_text, (10, w_height - 80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                user_click(event.pos)

        drawGrid()
        pygame.display.update()

    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(325, 475, 100, 50), 2)
    pygame.display.flip()
    reset_text = base_font.render('Reset', 1, (0, 0, 0))
    window.blit(reset_text, (346, 486))

    window.fill(white, rect=[10, w_height - 80, 100, 200])
    if winning_player != '':
        bottom_text = base_font.render(winning_player + ' Wins!!!', 1, (0, 0, 0))
        window.blit(bottom_text, (10, w_height - 80))
    else:
        bottom_text = base_font.render('Draw!!', 1, (0, 0, 0))
        window.blit(bottom_text, (10, w_height - 80))
    pygame.display.update()

    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(170, 475, 115, 50), 2)
    pygame.display.flip()
    main_menu_text = base_font.render('Main Menu', 1, (0, 0, 0))
    window.blit(main_menu_text, (175, 486))
    pygame.display.update()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(325, 425) and event.pos[1] in range(475, 525):
                    clear_board()
                elif event.pos[0] in range(170, 285) and event.pos[1] in range(475, 525):
                    return


def round_to_75(number, base=75):
    return base * round(number // base)


def user_click(coords):
    global current_player
    x = convert_to_centers(round_to_75(coords[0])) - 36
    y = convert_to_centers(round_to_75(coords[1])) - 72

    coords = (x, y)
    if update_board_screen(coords) == True:
        temp_text = x_font.render(current_player, 1, playing_colour)
        if y <= (450 - 72):
            window.blit(temp_text, (x, y))
        pygame.display.update()
    window.fill(white, rect=[10, w_height - 80, 250, 200])


def update_board_screen(pos):
    global count, play_count
    if pos in converter_to_array:
        temp = converter_to_array[pos]
        if board[temp[0]][temp[1]] != ' ':
            bottom_text = base_font.render('Sorry, that space is taken. Try again.', 1, (0, 0, 0))
            window.blit(bottom_text, (10, w_height - 80))
            pygame.display.update()
            return False
        else:
            board[temp[0]][temp[1]] = current_player
            count += 1
            return True
    return False


def check_full(board):
    for i in board:
        if ' ' in i:
            return False
    return True


def check_for_win(board):
    global winning_player
    for i in board:
        if i[0] == i[1] and i[1] == i[2] and i[0] != ' ':
            winning_player = i[0]
            return True
    for j in range(len(board)):
        if board[0][j] == board[1][j] and board[1][j] == board[2][j] and board[1][j] != ' ':
            winning_player = board[0][j]
            return True
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != ' ':
        winning_player = board[0][0]
        return True
    if board[2][0] == board[1][1] and board[1][1] == board[0][2] and board[2][0] != ' ':
        winning_player = board[2][0]
        return True
    return False


def convert_to_centers(x):
    if x in range(0, 150):
        x = 75
    elif x in range(150, 300):
        x = 225
    elif x in range(300, 450):
        x = 375
    return x


def clear_board():
    global board, winning_player, count
    for i in range(0, len(board)):
        for j in range(0, 3):
            board[i][j] = ' '

    for i in grid_array:
        window.fill(white, rect=[i[0], i[1], 138, 138])

    window.fill(white, rect=[325, 475, 100, 50])
    winning_player = ''
    count += 1
    multiplayer()


def main():
    drawGrid()
    multiplayer()


if __name__ == "__main__":
    main()
