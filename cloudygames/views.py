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
    player = django_filters.CharFilter(name='player__username')

    class Meta:
        model = GameSession
        fields = ['game', 'player']

class PlayerSaveDataFilter(django_filters.FilterSet):
    game = django_filters.CharFilter(name='game__id')
    player = django_filters.CharFilter(name='player__username')

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
        user = self.request.user
        if(user.is_staff):
            return GameSession.objects.all()
        return GameSession.objects.filter(player=user)

    def put(self, request):
        serializer = GameSessionSerializer(data=json.loads(request.body.decode('utf-8')))

        if serializer.is_valid():
            user = self.request.user
            game = serializer.validated_data['game']

            try:
                session = GameSession.objects.get(player=self.request.user, game=game) # Case 1: Already joined
            except GameSession.DoesNotExist:
                controller = GameSession.join_game(self, game)
                if(controller == -1): # Case 2: Invalid Request
                    return Response(status=status.HTTP_400_BAD_REQUEST)

                #Create game session
                session = GameSession.objects.create(game=game, player=user, controller=controller)
                serializer = GameSessionSerializer(session)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        data = json.loads(request.body.decode())

        game = Game.objects.get(id=data['game'])
        user = self.request.user
        session = GameSession.objects.get(game=game, player=user)

        if(GameSession.quit_game(self, session)):
            session.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class PlayerSaveDataViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSaveDataSerializer
    filter_class = PlayerSaveDataFilter

    def get_queryset(self):
        user = self.request.user
        if(user.is_staff):
            return PlayerSaveData.objects.all()
        return PlayerSaveData.objects.filter(player=user)

#import ipdb; ipdb.set_trace()