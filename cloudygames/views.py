from django.shortcuts import render

from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cloudygames.serializers import GameSerializer, GameSessionSerializer, PlayerSaveDataSerializer
from cloudygames.models import Game, GameSession, PlayerSaveData

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
	serializer_class = GameSessionSerializer
	queryset = GameSession.objects.all()

class PlayerSaveDataViewSet(viewsets.ModelViewSet):
	serializer_class = PlayerSaveDataSerializer
	queryset = PlayerSaveData.objects.all()