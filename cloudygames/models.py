from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.conf import settings

from cloudygames import utils

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

############################################################################
# Constants
############################################################################

ERROR_MSG = 'error'
PORT_NUM = 30000 # Offset for port number for player to plays the game
INVALID = -1

############################################################################
# Codes
############################################################################

class Game(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField()
    publisher = models.CharField(max_length=45)
    max_limit = models.IntegerField(default=4)
    address = models.URLField()
    thumbnail = ProcessedImageField(
        upload_to = 'thumbnails',
        processors = [ResizeToFill(100, 100)],
        format = 'PNG',
        options = {'quality': 60},
        default = 'thumbnails/default.png',
    )

    def __str__(self): # Python object representation
        return self.name


class GameOwnership(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)

    class Meta:
        unique_together = ['user', 'game']

    def __str__(self):
        return self.user.username + ' - ' + self.game.name


class GameSession(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    controller = models.IntegerField()
    streaming_port = models.IntegerField()

    class Meta:
        unique_together = ['user', 'game']


    # This function sends session data to see whether the session is accepted.
    #
    # param -    self
    #            gameobj : Game
    #            user : User
    # returns -  GameSession (error: None)
    #
    def join_game(gameobj, user):
        user_controller = INVALID

        try:

            controllers = range(gameobj.max_limit) # Valid controller id
            # Controller id currently used by user
            occupied = GameSession.objects.filter(game = gameobj). \
                       values_list('controller', flat=True)
            # Find suitable controller id
            available = list(set(controllers) - set(occupied))
            user_controller = available[0]

        except IndexError:
            return None

        if(user_controller != INVALID):
            session = GameSession.objects.create(
                        game = gameobj,
                        user = user,
                        controller = user_controller,
                        streaming_port = user_controller + PORT_NUM
                    )

            data = {
                'game_session_id': session.id,
                'controller': user_controller,
                'streaming_port': session.streaming_port,
                'streaming_ip': gameobj.address,
                'game_id': gameobj.id,
                'username': user.username,
                'command': 'join'
            }
            result = utils.connect_to_CPP(data)
            if(result != ERROR_MSG):
                return session

        # Failed: rollback
        session.delete()
        return None

    def __str__(self):
        return self.user.username + ' - ' + self.game.name


class PlayerSaveData(models.Model):
    saved_file = models.FileField(upload_to='save_data')
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)

    class Meta:
        unique_together = ['user', 'game']

    def __str__(self):
        return self.user.username + ' - ' + self.game.name
