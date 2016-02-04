from django.shortcuts import render
from django.core import serializers

from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cloudygames.serializers import GameSerializer, GameSessionSerializer, PlayerSaveDataSerializer
from cloudygames.models import Game, GameSession, PlayerSaveData

import json

class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer

    def get_queryset(self):
        is_owned = self.request.query_params.get('owned', 0)
        if is_owned:
            _user = self.request.user
            queryset = Game.objects.filter(users=_user)
        else:
            queryset = Game.objects.all()
        return queryset.order_by('name')

class GameSessionViewSet(viewsets.ModelViewSet):
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer
    
    def put(self, request, format=None):
        data = json.loads(request.body.decode())

        _game = Game.objects.get(id=data['game_id'])
        _user = self.request.user
        _controller = GameSession.getController(self, _game)
        if(_controller == -1):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        session = GameSession.objects.create(game=_game, player=_user, controller=_controller)
        serializer = GameSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PlayerSaveDataViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSaveDataSerializer
    queryset = PlayerSaveData.objects.all()