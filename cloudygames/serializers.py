from rest_framework import serializers
from accounts.serializers import UserSerializer
from cloudygames.models import Game, PlayerSaveData, GameSession

class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ('name', 'publisher', 'max_limit', 'address', 'users')

class PlayerSaveDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlayerSaveData
        fields = ('saved_file', 'is_autosaved', 'player', 'game')

class GameSessionSerializer(serializers.HyperlinkedModelSerializer):
    player = UserSerializer()
    game = GameSerializer()

    class Meta:
        model = GameSession
        fields = ('player', 'game', 'controller')

