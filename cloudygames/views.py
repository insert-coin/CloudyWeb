from django.shortcuts import render
from rest_framework import viewsets, generics
from cloudygames.serializers import GameSerializer
from cloudygames.models import Game

class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer

    def get_queryset(self):
        is_owned = self.request.query_params.get('owned', None)
        if is_owned is not None and is_owned is 1:
            _user = self.request.user
            queryset = Game.objects.filter(user=_user)
        else:
            queryset = Game.objects.all()
        return queryset.order_by('name')
