from django.shortcuts import render, get_object_or_404
from django.core import serializers

from rest_framework import viewsets, generics, status, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cloudygames.serializers \
    import GameSerializer, \
           GameSessionSerializer, \
           PlayerSaveDataSerializer, \
           GameOwnershipSerializer
from cloudygames.models \
    import Game, \
           GameSession, \
           PlayerSaveData, \
           GameOwnership
from cloudygames.permissions \
    import OperatorOnlyButPublicReadAccess, \
           UserIsOwnerOrOperator, \
           UserIsOwnerOrOperatorExceptUpdate
from cloudygames.filters \
    import GameFilter, \
           GameOwnershipFilter, \
           GameSessionFilter, \
           PlayerSaveDataFilter

import json

class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    filter_class = GameFilter
    permission_classes = (OperatorOnlyButPublicReadAccess,)

    def get_queryset(self):
        if not self.request.user.is_anonymous():
            is_owned = self.request.query_params.get('owned', 0)
            if is_owned == '1':
                user = self.request.user
                owned_games_id = GameOwnership.objects.filter(
                    user=user).values_list('game__id', flat=True)
                return Game.objects.filter(pk__in=owned_games_id)
        return Game.objects.all().order_by('name')

class GameOwnershipViewSet(viewsets.ModelViewSet):
    serializer_class = GameOwnershipSerializer
    filter_class = GameOwnershipFilter
    permission_classes = (UserIsOwnerOrOperatorExceptUpdate,)

    def get_queryset(self):
        user = self.request.user
        if(user.is_staff):
            return GameOwnership.objects.all()
        return GameOwnership.objects.filter(user=user)

class GameSessionViewSet(viewsets.ModelViewSet):
    serializer_class = GameSessionSerializer
    filter_class = GameSessionFilter
    permission_classes = (UserIsOwnerOrOperatorExceptUpdate,)
    
    def get_queryset(self):
        user = self.request.user
        if(user.is_staff):
            return GameSession.objects.all()
        return GameSession.objects.filter(user=user)

    def create(self, request):
        serializer = GameSessionSerializer(data=request.data)

        if serializer.is_valid():
            game = serializer.validated_data['game']
            user = serializer.validated_data['user']

            if (game.id in GameOwnership.objects.filter(
                user=user).values_list('game__id', flat=True)) or \
                (self.request.user.is_staff):
                # User owns the game
                controller = GameSession.join_game(self, game)
                if(controller['controllerid'] != -1):
                    #Create game session
                    session = GameSession.objects.create(
                        game=game,
                        user=user,
                        controller=controller['controllerid'],
                        streaming_port=controller['streaming_port']
                    )
                    serializer = GameSessionSerializer(session)
                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED
                    )
        return Response(status=status.HTTP_400_BAD_REQUEST)

class PlayerSaveDataViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSaveDataSerializer
    filter_class = PlayerSaveDataFilter
    permission_classes = (UserIsOwnerOrOperator,)

    def get_queryset(self):
        user = self.request.user
        if(user.is_staff):
            return PlayerSaveData.objects.all()
        return PlayerSaveData.objects.filter(user=user)

#import ipdb; ipdb.set_trace()