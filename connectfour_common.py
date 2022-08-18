import connectfour
import connectfour_shell


def game_board_format(game_state: connectfour.GameState) -> str:
    """Draw a formatted game board according to the given game state."""
    columns = connectfour.columns(game_state)
    board = ''
    for col in range(columns):
        if col + 1 > 8:
            board += f"{col + 1} "
        else:
            board += f"{col + 1}  "
    board = board.rstrip() + '\n'
    board_list = connectfour_shell.transpose(game_state.board)
    for row in range(len(board_list)):
        for col in range(len(board_list[row])):
            if board_list[row][col] == connectfour.EMPTY:
                board += '.  '
            elif board_list[row][col] == connectfour.RED:
                board += 'R  '
            elif board_list[row][col] == connectfour.YELLOW:
                board += 'Y  '
        board += '\n'
    return board


def start_game() -> connectfour.GameState:
    """
    Ask user the numbers of columns and rows, generate
    and print the gameboard accordingly.
    The function will print an error message if the 
    numbers of columns and rows is out of range.
    """
    while True:
        columns, rows = connectfour_shell.set_up_input()
        try:
            gamestate = connectfour.new_game(columns, rows)
            print(game_board_format(gamestate))
            return gamestate
        except ValueError:
            print('The numbers of columns and rows range from 4 to 20.')


def action_input() -> tuple:
    """
    Make sure user input valid action(P/D) and 
    that user enter an integer for column_num.
    Return action and column_num as tuple.
    Print error message if user failed to input valid 
    action or failed to input integer for column_num.
    """
    action = input("Enter action(P/D): ")
    while action.strip() != 'P' and action.strip() != 'D':
        print('Invalid action, try again')
        action = input("Enter action(P/D): ")

    while True:
        try:
            column_num = int(input("Action on which column: ")) - 1
            break
        except ValueError:
            print('Please enter an integer.')

    return (action, column_num)


def pop_action(game_state: connectfour.GameState, column_num: int) -> connectfour.GameState or bool:
    """
    Perform pop_action and return new GameState
    if the input is valid, otherwise return False.
    """
    try:
        return connectfour.pop(game_state, column_num)
    except connectfour.InvalidMoveError:
        print("The piece cannot be popped from the bottom of the given column.")
        return False
    except ValueError:
        print("The column number is invalid.")
        return False


def drop_action(game_state: connectfour.GameState, column_num: int) -> connectfour.GameState or bool:
    """
    Perform drop_action and return new GameState 
    if the input is valid, otherwise return False.
    """
    try:
        return connectfour.drop(game_state, column_num)
    except connectfour.InvalidMoveError:
        print("The move cannot be made in the given column.")
        return False
    except ValueError:
        print("The column number is invalid.")
        return False
