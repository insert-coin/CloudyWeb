from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

import socketserver
import socket
import errno

ERROR_MSG = 'error'
JOIN_CMD = '0000'
QUIT_CMD = '0001'

class Game(models.Model):
    name = models.CharField(max_length=45)
    publisher = models.CharField(max_length=45)
    max_limit = models.IntegerField()
    address = models.CharField(max_length=45)
    users = models.ManyToManyField(User)

class GameSession(models.Model):
    player = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    controller = models.IntegerField()

    def joinGame(self, _game):
        _controller = -1
        try:
            _session = GameSession.objects.get(player=self.request.user, game=_game)
            _controller = _session.controller
        except GameSession.DoesNotExist:
            try:
                controllers = range(_game.max_limit)
                occupied = GameSession.objects.filter(game=_game).values_list('controller', flat=True)
                available = list(set(controllers)-set(occupied))
                _controller = available[0]
            except IndexError:
                _controller = -1

        if(_controller != -1):
            command = '0000' + str(_controller).zfill(4)
            result = connectToCPP(command)
            if(result != ERROR_MSG):
                return _controller
        return -1

    def quitGame(self, _gameSession):
        command = '0001' + str(_gameSession.controller).zfill(4)
        result = connectToCPP(command)
        print (result)
        if(result != ERROR_MSG):
            return True
        return False

class PlayerSaveData(models.Model):
    saved_file = models.CharField(max_length=45)
    is_autosaved = models.BooleanField(default=True)
    player = models.ForeignKey(User)
    game = models.ForeignKey(Game)

# Need to add for genres in future sprints


#################### Additional Functions ######################

def connectToCPP(COMMAND):
    response = ""
    IP = '127.0.0.1'
    PORT_NO = 55556
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((IP, PORT_NO))
        s.sendall(COMMAND.encode("utf-8"))
        response = s.recv(BUFFER_SIZE).decode("utf-8")
    except socket.error as error:
        if error.errno == errno.WSAECONNRESET:
            response = ERROR_MSG
        else:
            raise
    finally:
        s.close()
        return response