from rest_framework import serializers
from accounts.serializers import UserSerializer
from django.contrib.auth.models import User
from cloudygames.models \
    import Game, PlayerSaveData, GameSession, GameOwnership

class GameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Game
        fields = ('id', 'name', 'publisher', 'max_limit', 'address', 'thumbnail')

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
    streaming_port = serializers.IntegerField(required=False)

    class Meta:
        model = GameSession
        fields = ('id', 'user', 'game', 'controller', 'streaming_port')

    def get_validation_exclusions(self):
        exclusions = super(GameSessionSerializer, self). \
                     get_validation_exclusions()
        return exclusions + ['controller', 'streaming_port']


class PlayerSaveDataSerializer(serializers.ModelSerializer):
    is_autosaved = serializers.BooleanField(required=False, default=False)
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = PlayerSaveData
        fields = ('id', 'saved_file', 'is_autosaved', 'user', 'game')
        validators = []

    def create(self, validated_data):
        saved_data, created = self.Meta.model.objects.update_or_create(
                game=validated_data['game'],
                user=validated_data['user'],
                is_autosaved=validated_data['is_autosaved'],
                defaults={'saved_file': validated_data['saved_file']})
        return saved_data
