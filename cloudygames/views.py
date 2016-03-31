from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.db import IntegrityError

from rest_framework import viewsets, generics, status, filters, mixins
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
           UserIsOwnerOrOperatorExceptUpdate, \
           UserIsOperatorButOwnerCanRead
from cloudygames.filters \
    import GameFilter, \
           GameOwnershipFilter, \
           GameSessionFilter, \
           PlayerSaveDataFilter

import json

INVALID = -1

class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    filter_class = GameFilter
    permission_classes = (OperatorOnlyButPublicReadAccess,)
    queryset = Game.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_anonymous():
            is_owned = self.request.query_params.get('owned', 0)
            # Only returns the games this user owns
            if is_owned == '1':
                user = self.request.user
                owned_games_id = GameOwnership.objects.filter(
                    user=user).values_list('game__id', flat=True)
                return qs.filter(pk__in=owned_games_id)
        # Returns all games
        return qs.order_by('name')

class GameOwnershipViewSet(viewsets.ModelViewSet):
    serializer_class = GameOwnershipSerializer
    filter_class = GameOwnershipFilter
    permission_classes = (UserIsOwnerOrOperatorExceptUpdate,)
    queryset = GameOwnership.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_staff:
            qs = qs.filter(user=user)
        return qs

class GameSessionViewSet(viewsets.ModelViewSet):
    serializer_class = GameSessionSerializer
    filter_class = GameSessionFilter
    permission_classes = (UserIsOwnerOrOperatorExceptUpdate,)
    queryset = GameSession.objects.all()
    
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_staff:
            qs = qs.filter(user=user)
        return qs

    def create(self, request):
        serializer = GameSessionSerializer(data=request.data)
        response_data = {}

        if serializer.is_valid():
            game = serializer.validated_data['game']
            user = serializer.validated_data['user']

            # User has access over the game
            if (game.id in GameOwnership.objects.filter(
            user=user).values_list('game__id', flat=True)) or \
                (self.request.user.is_staff):

                session = GameSession.join_game(self, game, user)
                # User can play using the valid id
                if(session != None):
                    serializer = GameSessionSerializer(session)
                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED
                    )
                else:
                    response_data['message'] = \
                        'Game\'s limit has been reached.\nPlease try again later'
            else:
                response_data['message'] = 'User does not have access for the game'
                return Response(
                    response_data,
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            response_data['message'] = 'The request data is not valid'

        return Response(
            response_data,
            status=status.HTTP_400_BAD_REQUEST
        )

class PlayerSaveDataViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    serializer_class = PlayerSaveDataSerializer
    filter_class = PlayerSaveDataFilter
    permission_classes = (UserIsOperatorButOwnerCanRead,)
    queryset = PlayerSaveData.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_staff:
            qs = qs.filter(user=user)
        return qs
