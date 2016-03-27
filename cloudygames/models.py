from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.conf import settings

from cloudygames import utils

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

ERROR_MSG = 'error'
JOIN_CMD = '0000'
PORT_NUM = 30000
INVALID = -1

class Game(models.Model):
    name = models.CharField(max_length=45)
    publisher = models.CharField(max_length=45)
    max_limit = models.IntegerField()
    address = models.CharField(max_length=45)
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

    def join_game(self, gameobj):
        data = {
            'controllerid': INVALID,
            'streaming_port': INVALID
        }
        try:
            controllers = range(gameobj.max_limit)
            occupied = GameSession.objects.filter(game=gameobj). \
                       values_list('controller', flat=True)
            available = list(set(controllers)-set(occupied))
            data['controllerid'] = available[0]
        except IndexError:
            return data

        if(data['controllerid'] != INVALID):
            command = JOIN_CMD + str(data['controllerid']).zfill(4)
            result = utils.connect_to_CPP(command)
            if(result != ERROR_MSG):
                data['streaming_port'] = data['controllerid'] + PORT_NUM
        return data

    def __str__(self):
        return self.user.username + ' - ' + self.game.name

class PlayerSaveData(models.Model):
    saved_file = models.FileField(upload_to='save_data')
    is_autosaved = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)

    class Meta:
        unique_together = ['user', 'game', 'is_autosaved']

    def __str__(self):
        return self.user.username + ' - ' + self.game.name

# Need to add for genres in future sprints
