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

class GameOwnership(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)

class GameSession(models.Model):
    player = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    controller = models.IntegerField()

    def join_game(self, gameobj):
        controllerid = -1
        try:
            controllers = range(gameobj.max_limit)
            occupied = GameSession.objects.filter(game=gameobj).values_list('controller', flat=True)
            available = list(set(controllers)-set(occupied))
            controllerid = available[0]
        except IndexError:
            controllerid = -1

        if(controllerid != -1):
            command = JOIN_CMD + str(controllerid).zfill(4)
            result = utils.connect_to_CPP(command)
            if(result != ERROR_MSG):
                return controllerid
        return -1

    def quit_game(self, game_session):
        command = QUIT_CMD + str(game_session.controller).zfill(4)
        result = utils.connect_to_CPP(command)
        if(result != ERROR_MSG):
            return True
        return False

class PlayerSaveData(models.Model):
    saved_file = models.CharField(max_length=45)
    is_autosaved = models.BooleanField(default=True)
    player = models.ForeignKey(User)
    game = models.ForeignKey(Game)

# Need to add for genres in future sprints