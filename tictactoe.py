from math import inf as infinity
from random import choice
import platform
import time
from os import system


HUMAN = -1
COMPUTER = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

def minimax(state, depth, player):
    """
    AI function that chooses the best move
    param state: current state of the board
    param depth: node index in the tree (0 <= depth <= 9),
    but never nine in this case (see iaturn() function)
    param player: an human or a computer
    return: a list with [the best row, best col, best score]
    """
    if player == COMPUTER:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMPUTER:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best

def evaluate(state):
    """
    state: the state of the current board
    return: +1 if the computer wins; -1 if the human wins; 0 draw
    """
    if win(state, COMPUTER):
        score = +1
    elif win(state, HUMAN):
        score = -1
    else:
        score = 0
    return score


def win(state, player):
    """
    This function tests if a specific player win.s Possibilities:
    Three rows    [X X X] or [O O O]
    Three cols    [X X X] or [O O O]
    Two diagonals [X X X] or [O O O]
    param state: the state of the current board
    param player: a human or a computer
    return: True if the player win
    """
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    """
    This function test if the human or computer win
    param state: the state of the current board
    return: True if the human or computer win
    """
    return win(state, HUMAN) or win(state, COMPUTER)


def empty_cells(state):
    """
    Each empty cell will be added into cells' list
    param state: the state of the current board
    return: a list of empty cells
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    """
    A move is valid if the chosen cell is empty
    param x: X coordinate
    param y: Y coordinate
    return: True if the board[x][y] is empty
    """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    """
    Set the move on board, if the coordinates are valid
    param x: X coordinate
    param y: Y coordinate
    param player: the current player
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def clean():
    """
    Clears the console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, computer_choice, human_choice):
    """
    Print the board on console
    param state: current state of the board
    """

    chars = {
        -1: human_choice,
        +1: computer_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(computer_choice, human_choice):
    """
    It calls the minimax function if the depth < 9,
    else it chooses a random coordinate.
    param computer_choice: computer's choice X or O
    param human_choice: human's choice X or O
    return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print(f'Computer turn [{computer_choice}]')
    render(board, computer_choice, human_choice)

    if depth == 9:
        x = choice([0, 1, 2]) #returns a random item from a list
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMPUTER)
        x, y = move[0], move[1]

    set_move(x, y, COMPUTER)
    time.sleep(1)


def human_turn(computer_choice, human_choice):
    """
    The Human plays choosing a valid move.
    param computer_choice: computer's choice X or O
    param human_choice: human's choice X or O
    return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Human turn [{human_choice}]')
    render(board, computer_choice, human_choice)

    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


def main():
    clean()
    human_choice = ''  # X or O
    computer_choice = ''  # X or O
    first_move = ''  # if human is the first_move

    # Human chooses X or O to play
    while human_choice != 'O' and human_choice != 'X':
        try:
            print('')
            human_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Setting computer's choice
    if human_choice == 'X':
        computer_choice = 'O'
    else:
        computer_choice = 'X'

    # Human may starts first_move
    clean()
    while first_move != 'Y' and first_move != 'N':
        try:
            first_move = input('first_move to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Main loop of this game
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first_move == 'N':
            ai_turn(computer_choice, human_choice)
            first_move = ''

        human_turn(computer_choice, human_choice)
        ai_turn(computer_choice, human_choice)

    # Game over message
    if win(board, HUMAN):
        clean()
        print(f'Human turn [{human_choice}]')
        render(board, computer_choice, human_choice)
        print('YOU WIN!')
    elif win(board, COMPUTER):
        clean()
        print(f'Computer turn [{computer_choice}]')
        render(board, computer_choice, human_choice)
        print('YOU LOSE!')
    else:
        clean()
        render(board, computer_choice, human_choice)
        print('DRAW!')

    exit()


if __name__ == '__main__':
    main()