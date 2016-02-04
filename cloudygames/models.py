from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

class Game(models.Model):
    name = models.CharField(max_length=45)
    publisher = models.CharField(max_length=45)
    max_limit = models.IntegerField()
    address = models.CharField(max_length=45)
    users = models.ManyToManyField(User)

class PlayerSaveData(models.Model):
    saved_file = models.CharField(max_length=45)
    is_autosaved = models.BooleanField(default=True)
    player = models.ForeignKey(User)
    game = models.ForeignKey(Game)

class GameSession(models.Model):
    player = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    controller = models.IntegerField()

    def getController(self, _game):
        try:
            _session = GameSession.objects.get(player=self.request.user, game=_game)
            return _session.controller
        except GameSession.DoesNotExist:
            try:
                controllers = range(_game.max_limit)
                occupied = GameSession.objects.filter(game=_game).values_list('controller', flat=True)
                available = list(set(controllers)-set(occupied))
                return available[0]
            except IndexError:
                return -1

# Need to add for genres in future sprints