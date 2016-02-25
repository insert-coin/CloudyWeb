from rest_framework import serializers
from accounts.serializers import UserSerializer
from django.contrib.auth.models import User
from cloudygames.models \
    import Game, PlayerSaveData, GameSession, GameOwnership

class GameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Game
        fields = ('id', 'name', 'publisher', 'max_limit', 'address')

class GameOwnershipSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = GameOwnership
        fields = ('id', 'user', 'game')

class GameSessionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset = User.objects.all(),
        slug_field = 'username'
    )
    controller = serializers.IntegerField(required=False)

    class Meta:
        model = GameSession
        fields = ('id', 'user', 'game', 'controller')

    def get_validation_exclusions(self):
        exclusions = super(GameSessionSerializer, self). \
                     get_validation_exclusions()
        return exclusions + ['controller']

class PlayerSaveDataSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset = User.objects.all(),
        slug_field = 'username'
    )
    is_autosaved = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = PlayerSaveData
        fields = ('id', 'saved_file', 'is_autosaved', 'user', 'game')

    def get_validation_exclusions(self):
        exclusions = super(PlayerSaveDataSerializer, self). \
                     get_validation_exclusions()
        return exclusions + ['is_autosaved']