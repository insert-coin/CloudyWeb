from django.shortcuts import render
from django.core import serializers

from rest_framework import viewsets, generics, status, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cloudygames.serializers import GameSerializer, GameSessionSerializer, PlayerSaveDataSerializer
from cloudygames.models import Game, GameSession, PlayerSaveData

import django_filters
import json


######################## Filter ############################


class GameFilter(django_filters.FilterSet):
    users = django_filters.CharFilter(name='users__username')

    class Meta:
        model = Game
        fields = ['id', 'name', 'publisher', 'users']
        order_by = ['name']
        read_only_fields = ('id',)

class GameSessionFilter(django_filters.FilterSet):
    game = django_filters.CharFilter(name='game__id')
    player = django_filters.CharFilter(name='player_username')

    class Meta:
        model = GameSession
        fields = ['game', 'player']

class PlayerSaveDataFilter(django_filters.FilterSet):
    game = django_filters.CharFilter(name='game__id')
    player = django_filters.CharFilter(name='player_username')

    class Meta:
        model = PlayerSaveData
        fields = ['game', 'player']


######################## ViewSet ############################

class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    filter_class = GameFilter

    def get_queryset(self):
        is_owned = self.request.query_params.get('owned', 0)
        if is_owned == '1':
            _user = self.request.user
            return Game.objects.filter(users=_user)
        return Game.objects.all().order_by('name')

class GameSessionViewSet(viewsets.ModelViewSet):
    serializer_class = GameSessionSerializer
    filter_class = GameSessionFilter
    
    def get_queryset(self):
        _user = self.request.user
        if(_user.is_staff):
            return GameSession.objects.all()
        return GameSession.objects.filter(player=_user)

    def create(self, request):
        #import ipdb; ipdb.set_trace()
        _serializer = GameSessionSerializer(data=request.data)

        if _serializer.is_valid():
            _gameid = _serializer.data['game']
            _game = Game.objects.get(id=_gameid)
            _user = self.request.user
            _controller = GameSession.join_game(self, _game)
            if(_controller == -1):
                return Response(status=status.HTTP_400_BAD_REQUEST)

            _session = GameSession.objects.create(game=_game, player=_user, controller=_controller)
            _serializer = GameSessionSerializer(_session)
            return Response(_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, format=None):
        _data = json.loads(request.body.decode())

        _game = Game.objects.get(id=_data['game'])
        _user = self.request.user
        _session = GameSession.objects.get(game=_game, player=_user)

        if(GameSession.quit_game(self, _session)):
            _session.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class PlayerSaveDataViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSaveDataSerializer
    filter_class = PlayerSaveDataFilter

    def get_queryset(self):
        _user = self.request.user
        if(_user.is_staff):
            return GameSession.objects.all()
        return PlayerSaveData.objects.filter(player=_user)