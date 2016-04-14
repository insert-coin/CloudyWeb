

import socketserver
import socket
import errno
import json

############################################################################
# Constants
############################################################################

ERROR_MSG = 'error'

# Address for CloudyWeb Plugin
PORT_NO = 55556
BUFFER_SIZE = 1024

############################################################################
# Codes
############################################################################


# This function sends session data to see whether the session is accepted.
#
# param -    data {
#                 game_session_id : id of the game session object,
#                 controller : controller id in which we try connecting to,
#                 streaming_port : streaming port for the game,
#                 streaming_ip : streaming ip for the game,
#                 game_id : id of the game object,
#                 username : username of the player,
#                 command : in this case should always be 'join'
#              }
# returns -  response from server or error message
#
def connect_to_CPP(data):
    response = ""
    IP = data['streaming_ip']

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cmd = json.dumps(data)
        s.connect((IP, PORT_NO))
        s.sendall(cmd.encode("utf-8"))
        response = s.recv(BUFFER_SIZE).decode("utf-8")
    except socket.error as error:
        if error.errno == errno.WSAECONNRESET:
            response = ERROR_MSG
        else:
            raise
    finally:
        s.close()
        return response