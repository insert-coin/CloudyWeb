from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
	name = models.CharField(max_length=45)
	publisher = models.CharField(max_length=45)
	max_limit = models.IntegerField()
	address = models.CharField(max_length=45)
	user = models.ManyToManyField(User)

class PlayerSaveData(models.Model):
	saved_file = models.CharField(max_length=45)
	is_autosaved = models.BooleanField(default=True)
	player = models.ForeignKey(User)
	game = models.ForeignKey(Game)

class GameSession(models.Model):
	player = models.ForeignKey(User)
	game = models.ForeignKey(Game)
	controller = models.IntegerField()

# Need to add for genres in future sprints