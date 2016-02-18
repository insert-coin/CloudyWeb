
import socketserver
import socket
import errno

ERROR_MSG = 'error'

def connect_to_CPP(command):
    response = ""
    IP = '127.0.0.1'
    PORT_NO = 55556
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((IP, PORT_NO))
        s.sendall(command.encode("utf-8"))
        response = s.recv(BUFFER_SIZE).decode("utf-8")
    except socket.error as error:
        if error.errno == errno.WSAECONNRESET:
            response = ERROR_MSG
        else:
            raise
    finally:
        s.close()
        return response