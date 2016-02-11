from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

from cloudygames import utils

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
    player = models.ForeignKey(User, blank=True, null=True)
    game = models.ForeignKey(Game, blank=True, null=True)
    controller = models.IntegerField(blank=True, null=True)

    def join_game(self, _game):
        _controller = -1
        try:
            _session = GameSession.objects.get(player=self.request.user, game=_game)
            _controller = _session.controller
        except GameSession.DoesNotExist:
            try:
                _controllers = range(_game.max_limit)
                _occupied = GameSession.objects.filter(game=_game).values_list('controller', flat=True)
                _available = list(set(_controllers)-set(_occupied))
                _controller = _available[0]
            except IndexError:
                _controller = -1

        if(_controller != -1):
            _command = JOIN_CMD + str(_controller).zfill(4)
            _result = utils.connect_to_CPP(_command)
            if(_result != ERROR_MSG):
                return _controller
        return -1

    def quit_game(self, _game_session):
        _command = QUIT_CMD + str(_game_session.controller).zfill(4)
        _result = utils.connect_to_CPP(_command)
        if(_result != ERROR_MSG):
            return True
        return False

class PlayerSaveData(models.Model):
    saved_file = models.CharField(max_length=45)
    is_autosaved = models.BooleanField(default=True)
    player = models.ForeignKey(User)
    game = models.ForeignKey(Game)

# Need to add for genres in future sprints