from rest_framework import serializers
from cloudygames.models import Game, PlayerSaveData, GameSession, UserGames

class GameSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Game
		fields = ('name', 'publisher', 'max_limit', 'address', 'user')

	def create(self, validated_data):
		return Game.objects.create(**validated_data)

	def update(self, instance, validated_data):
		instance.name = validated_data.get('name', instance.name)
		instance.publisher = validated_data.get('publisher', instance.publisher)
		instance.max_limit = validated_data.get('max_limit', instance.max_limit)
		instance.address = validated_data.get('address', instance.address)
		instance.user = validated_data.get('user', instance.user)
		instance.save()
		return instance

class PlayerSaveDataSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = PlayerSaveData
		fields = ('saved_file', 'is_autosaved', 'player', 'game')

	def create(self, validated_data):
		return PlayerSaveData.create(**validated_data)

	def update(self, instance, validated_data):
		instance.saved_file = validated_data.get('saved_file', instance.saved_file)
		instance.is_autosaved = validated_data.get('is_autosaved', instance.is_autosaved)
		instance.player = validated_data.get('player', instance.player)
		instance.game = validated_data.get('game', instance.game)
		instance.save()
		return instance

class GameSessionSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = GameSession
		fields = ('player', 'game', 'controller')

	def create(self, validated_data):
		return GameSession.create(**validated_data)

	def update(self, instance, validated_data):
		instance.player = validated_data.get('player', instance.player)
		instance.game = validated_data.get('game', instance.game)
		instance.controller = validated_data.get('controller', instance.controller)
		instance.save()
		return instance

