import socket
from collections import namedtuple
ServerConnection = namedtuple('ServerConnection', 'socket input output')
DEBUG = False


def connect_server() -> ServerConnection:
    """
    Establish connection and return ServerConnection
    based on the host and port user input.
    """
    host = input('Enter the host (either IP address or hostname): ').strip()
    port = int(input('Enter the port: ').strip())
    server_socket = socket.socket()
    server_socket.connect((host, port))
    server_input = server_socket.makefile('w')
    server_output = server_socket.makefile('r')
    return ServerConnection(socket=server_socket, input=server_input, output=server_output)


def write_server(connection: ServerConnection, message: str) -> None:
    """Write message to the server."""
    connection.input.write(message + '\r\n')
    connection.input.flush()
    if DEBUG:
        print('SENT: ' + message)


def read_server(connection: ServerConnection) -> str:
    """Read message from the server."""
    line = connection.output.readline().rstrip('\n')
    if DEBUG:
        print('Reci: ' + line)
    return line
