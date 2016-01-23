from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
	name = models.CharField(max_length=45)
	publisher = models.CharField(max_length=45)
	max_limit = models.IntegerField()
	address = models.CharField(max_length=45)

class PlayerSaveData(models.Model):
	saved_file = models.CharField(max_length=45)
	is_autosaved = models.BooleanField(default=True)
	player_id = models.ForeignKey(User)
	game_id = models.ForeignKey(Game)

class GameSession(models.Model):
	player_id = models.ForeignKey(User)
	game_id = models.ForeignKey(Game)
	controller_id = models.IntegerField()

class UserGames(models.Model):
	player_id = models.ForeignKey(User)
	game_id = models.ForeignKey(Game)
	

# Need to add for genres in future sprints