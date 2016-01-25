from rest_framework import serializers
from cloudygames.models import Game, PlayerSaveData, GameSession

class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ('name', 'publisher', 'max_limit', 'address', 'user')

class PlayerSaveDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlayerSaveData
        fields = ('saved_file', 'is_autosaved', 'player', 'game')

class GameSessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameSession
        fields = ('player', 'game', 'controller')

