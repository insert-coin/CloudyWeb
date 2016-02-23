from rest_framework import serializers
from accounts.serializers import UserSerializer
from django.contrib.auth.models import User
from cloudygames.models import Game, PlayerSaveData, GameSession

class GameSerializer(serializers.ModelSerializer):
    users = serializers.SlugRelatedField(
        many=True,
        queryset=User.objects.all(),
        slug_field='username'
    )
    
    class Meta:
        model = Game
        fields = ('id', 'name', 'publisher', 'max_limit', 'address', 'users')

class GameSessionSerializer(serializers.ModelSerializer):
    player = serializers.SlugRelatedField(
        queryset = User.objects.all(),
        slug_field = 'username',
        required = False,
    )
    controller = serializers.IntegerField(required=False)

    class Meta:
        model = GameSession
        fields = ('id', 'player', 'game', 'controller')

    def get_validation_exclusions(self):
        exclusions = super(GameSessionSerializer, self).get_validation_exclusions()
        return exclusions + ['player', 'game']

class PlayerSaveDataSerializer(serializers.ModelSerializer):
    is_autosaved = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = PlayerSaveData
        fields = ('id', 'saved_file', 'is_autosaved', 'player', 'game')

    def get_validation_exclusions(self):
        exclusions = super(PlayerSaveDataSerializer, self).get_validation_exclusions()
        return exclusions + ['is_autosaved']