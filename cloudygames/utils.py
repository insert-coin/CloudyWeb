
import socketserver
import socket
import errno
import json

ERROR_MSG = 'error'

def connect_to_CPP(data):
    response = ""

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = data['streaming_ip']
    PORT_NO = 55556
    BUFFER_SIZE = 1024

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