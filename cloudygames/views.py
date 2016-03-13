from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.db import IntegrityError

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

    def get_queryset(self):
        if not self.request.user.is_anonymous():
            is_owned = self.request.query_params.get('owned', 0)
            # Only returns the games this user owns
            if is_owned == '1':
                user = self.request.user
                owned_games_id = GameOwnership.objects.filter(
                    user=user).values_list('game__id', flat=True)
                return Game.objects.filter(pk__in=owned_games_id)
        # Returns all games
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
        response_data = {}

        if serializer.is_valid():
            game = serializer.validated_data['game']
            user = serializer.validated_data['user']

            # User has access over the game
            if (game.id in GameOwnership.objects.filter(
            user=user).values_list('game__id', flat=True)) or \
                (self.request.user.is_staff):

                controller = GameSession.join_game(self, game)
                # User can play using the valid id
                if(controller['controllerid'] != INVALID):
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
                else:
                    response_data['message'] = \
                        'We currently could not find a valid \
                        controllerid for you. This could be due to \
                        temporary lost of connection with CloudyGames \
                        or the game\'s limit has been exceeded. \
                        Please try again after a while.'
            else:
                response_data['message'] = 'User does not have access for the game'
                return Response(
                    json.dumps(response_data),
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            response_data['message'] = 'The request data is not valid'

        return Response(
            json.dumps(response_data),
            status=status.HTTP_400_BAD_REQUEST
        )

class PlayerSaveDataViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSaveDataSerializer
    filter_class = PlayerSaveDataFilter
    permission_classes = (UserIsOperatorButOwnerCanRead,)

    def get_queryset(self):
        user = self.request.user
        if(user.is_staff):
            return PlayerSaveData.objects.all()
        return PlayerSaveData.objects.filter(user=user)

    def create(self, request):
        response_data = {}

        controller = request.data.get('controller')
        game_name = request.data.get('game_name');
        is_autosaved = request.data.get('is_autosaved')
        saved_file = request.data.get('saved_file')

        # Validating
        if(controller == None or game_name == None or saved_file == None):
            response_data['message'] = 'The request data is not valid'
            return Response(
                json.dumps(response_data),
                status=status.HTTP_400_BAD_REQUEST
            )
        if(is_autosaved == None or is_autosaved != True):
            is_autosaved = False # Default value

        game = get_object_or_404(Game, name=game_name)
        user = get_object_or_404(
            GameSession,
            game=game, controller=controller
        ).user

        # Duplicate
        if(len(PlayerSaveData.objects.filter(user=user, game=game,
        is_autosaved=is_autosaved)) > 0):
            response_data['message'] = \
                'Duplicated data. Please update the existing data instead'
            return Response(
                json.dumps(response_data),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            save_data = PlayerSaveData.objects.create(
                game = game,
                user = user,
                is_autosaved = is_autosaved,
                saved_file = saved_file
            )
            serializer = PlayerSaveDataSerializer(save_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            response_data['message'] = e.message
            return Response(
                json.dumps(response_data),
                status=status.HTTP_400_BAD_REQUEST
            )

#import ipdb; ipdb.set_trace()