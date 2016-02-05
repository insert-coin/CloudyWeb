from rest_framework import serializers
from accounts.serializers import UserSerializer
from cloudygames.models import Game, PlayerSaveData, GameSession

class GameSerializer(serializers.HyperlinkedModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Game
        fields = ('id', 'name', 'publisher', 'max_limit', 'address', 'users')

class PlayerSaveDataSerializer(serializers.HyperlinkedModelSerializer):
    player = UserSerializer()
    game = GameSerializer()

    class Meta:
        model = PlayerSaveData
        fields = ('id', 'saved_file', 'is_autosaved', 'player', 'game')

    def create(self, data):
        data.player = self.request.user
        return PlayerSaveData.objects.create(data)

class GameSessionSerializer(serializers.HyperlinkedModelSerializer):
    player = UserSerializer()
    game = GameSerializer()

    class Meta:
        model = GameSession
        fields = ('player', 'game', 'controller')