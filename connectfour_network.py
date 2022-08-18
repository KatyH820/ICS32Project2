import connectfour
import connectfour_socket
import connectfour_common


def login(connection: connectfour_socket.ServerConnection) -> bool:
    """
    Ask user to input the username and 
    tell user if the username is invalid.
    """
    username = input("Enter username: ")
    connectfour_socket.write_server(connection, 'I32CFSP_HELLO ' + username)
    response = connectfour_socket.read_server(connection)
    if response == 'ERROR':
        print('Invalid username; username cannot contain whitespace characters(e.g.,spaces or tabs).')
        return False
    else:
        return True


def start_game(connection: connectfour_socket.ServerConnection) -> connectfour.GameState:
    """Start the game, ask user to input the number of columns and rows"""
    game_state = connectfour_common.start_game()
    num_columns = connectfour.columns(game_state)
    num_rows = connectfour.rows(game_state)
    connectfour_socket.write_server(
        connection, f'AI_GAME {num_columns} {num_rows}')
    connectfour_socket.read_server(connection)
    return game_state


def unwanted_response(connection: connectfour_socket.ServerConnection) -> None:
    """Keep read from the server until the server send OKAY"""
    response = connectfour_socket.read_server(connection).strip()
    while response != 'OKAY':
        response = connectfour_socket.read_server(connection)


def red_turn(connection: connectfour_socket.ServerConnection, game_state: connectfour.GameState) -> connectfour.GameState:
    """
    Ask user to input the action and column_num, write the message
    to the server and return an updated GameState
    If the move is invalid, the function will keep asking user to 
    input the action and column number until the inputs are valid.
    """
    print("Red player's turn")
    while True:
        action, column_num = connectfour_common.action_input()
        if action == 'D':
            connectfour_socket.write_server(
                connection, f'DROP {column_num + 1}')
            if connectfour_common.drop_action(game_state, column_num) == False:
                connectfour_socket.read_server(connection)
                continue
            else:
                unwanted_response(connection)
                return connectfour_common.drop_action(game_state, column_num)
        elif action == 'P':
            connectfour_socket.write_server(
                connection, f'POP {column_num + 1}')
            if connectfour_common.pop_action(game_state, column_num) == False:
                connectfour_socket.read_server(connection)
                continue
            else:
                unwanted_response(connection)
                return connectfour_common.pop_action(game_state, column_num)


def yellow_turn(connection: connectfour_socket.ServerConnection, game_state: connectfour.GameState) -> connectfour.GameState:
    """
    Read action and column number from server.
    Perform the action and return the updated GameState.
    """
    print("Yellow player's turn")
    response = connectfour_socket.read_server(connection)
    column_num = int(response.split()[-1])
    if 'POP ' in response:
        game_state = connectfour_common.pop_action(
            game_state, column_num - 1)
        connectfour_socket.read_server(connection)
    elif 'DROP ' in response:
        game_state = connectfour_common.drop_action(
            game_state, column_num - 1)
        connectfour_socket.read_server(connection)
    return game_state


def game(connection: connectfour_socket.ServerConnection):
    """
    Create a new game and run the game.
    Print updated game board each time an action is perform.
    The game will stop when winner appear.
    """
    current_game = start_game(connection)
    while connectfour.winner(current_game) == connectfour.EMPTY:
        if current_game.turn == connectfour.RED:
            current_game = red_turn(connection, current_game)
        else:
            current_game = yellow_turn(connection, current_game)
        print(connectfour_common.game_board_format(current_game))
    else:
        if connectfour.winner(current_game) == connectfour.RED:
            print("Red player wins!")
            print(connectfour_common.game_board_format(current_game))
        elif connectfour.winner(current_game) == connectfour.YELLOW:
            print("Yellow player wins!")
            print(connectfour_common.game_board_format(current_game))


def close(connection: connectfour_socket.ServerConnection) -> None:
    """Close the connection"""
    connection.input.close()
    connection.output.close()
    connection.socket.close()


def run() -> None:
    """
    Try to connect with the server, if it is able to 
    connect to the server, it will ask user to input the 
    username to login and start the game, once the game is
    over, the connection will be closed.
    If it is unable to connect with the server, it will print an
    error message to the user.
    """
    try:
        connection = connectfour_socket.connect_server()
    except Exception:
        print(
            "The connection is unsuccessful; cannot connect to the host and port provided.")
    else:
        if login(connection) == True:
            game(connection)
            close(connection)


if __name__ == '__main__':
    run()
