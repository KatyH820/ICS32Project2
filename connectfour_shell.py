import connectfour
import connectfour_common


def transpose(matrix) -> list[list[int]]:
    """Transpose the matrix"""
    return [list(num) for num in zip(*matrix)]


def set_up_input() -> tuple:
    """
    Make sure user enter integer for columns and rows.
    Return a tuple of columns and rows number.
    The function will print an error message if the user 
    does not enter integers.
    """
    while True:
        try:
            columns = int(input('Enter the number of columns for the board\n'))
            rows = int(input('Enter the number of rows for the board:\n'))
            return columns, rows
        except ValueError:
            print("Please enter an integer.")
            pass


def label_turn(game_state: connectfour.GameState) -> None:
    """Print the player's turn."""
    current_turn = game_state.turn
    if current_turn == connectfour.RED:
        print("Red player's turn:")
    elif current_turn == connectfour.YELLOW:
        print("Yellow player's turn:")


def take_turn(game_state: connectfour.GameState) -> connectfour.GameState:
    """
    Perform action and return new GameState based on user's input. 
    If user enter invalid action or column number, 
    it will keep asking until user enter a valid one.
    """
    label_turn(game_state)
    while True:
        action, column_num = connectfour_common.action_input()
        if action.strip() == 'P':
            if connectfour_common.pop_action(game_state, column_num) == False:
                continue
            else:
                return connectfour_common.pop_action(game_state, column_num)
        elif action.strip() == 'D':
            if connectfour_common.drop_action(game_state, column_num) == False:
                continue
            else:
                return connectfour_common.drop_action(game_state, column_num)
        else:
            break


def run() -> None:
    """
    Create a new game and run the game.
    Print updated game board each time an action is perform.
    The game will stop when winner appear.
    """
    current_game = connectfour_common.start_game()
    while connectfour.winner(current_game) == connectfour.EMPTY:
        current_game = take_turn(current_game)
        try:
            print(connectfour_common.game_board_format(current_game))
        except Exception:
            pass
    else:
        if connectfour.winner(current_game) == connectfour.RED:
            print("Red player wins!")
            print(connectfour_common.game_board_format(current_game))
        elif connectfour.winner(current_game) == connectfour.YELLOW:
            print("Yellow player wins!")
            print(connectfour_common.game_board_format(current_game))


if __name__ == '__main__':
    run()
