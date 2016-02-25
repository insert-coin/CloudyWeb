import django_filters

from cloudygames.models \
    import Game, GameSession, PlayerSaveData, GameOwnership

class GameFilter(django_filters.FilterSet):

    class Meta:
        model = Game
        fields = ['id', 'name', 'publisher']
        order_by = ['name']
        read_only_fields = ('id',)

class GameOwnershipFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(name='user__username')

    class Meta:
        model = GameOwnership
        fields = ['user', 'game']

class GameSessionFilter(django_filters.FilterSet):
    game = django_filters.CharFilter(name='game__id')
    user = django_filters.CharFilter(name='user__username')

    class Meta:
        model = GameSession
        fields = ['game', 'user']

class PlayerSaveDataFilter(django_filters.FilterSet):
    game = django_filters.CharFilter(name='game__id')
    user = django_filters.CharFilter(name='user__username')

    class Meta:
        model = PlayerSaveData
        fields = ['game', 'user']