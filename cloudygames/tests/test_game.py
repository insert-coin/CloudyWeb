from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import serializers
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient

from cloudygames.models import Game, PlayerSaveData, GameOwnership
from cloudygames.serializers import GameSerializer

import json

# Create your tests here.

class GameAPITest(APITestCase):

    # Set Up necessary temporary database for the tests
    def setUp(self):
        # Users (User 1 = Operator, User 2 = Normal User)
        self.operator = User.objects.create(
            username="operator",
            password="operator",
            email="operator@email.com",
            first_name="firstname",
            last_name="lastname"
        )
        self.operator.is_staff = True
        self.operator.save()
        self.player = User.objects.create(
            username="player",
            password="player",
            email="player@email.com",
            first_name="firstname",
            last_name="lastname"
        )

        # Game
        self.game1 = Game.objects.create(
            name="game1",
            publisher="pub1",
            max_limit=1,
            address="addr1",
            description="a"
        )
        self.game2 = Game.objects.create(
            name="game2",
            publisher="pub1",
            max_limit=1,
            address="addr2",
            description="b"
        )
        self.game3 = Game.objects.create(
            name="game3",
            publisher="pub2",
            max_limit=4,
            address="addr3",
            description="c"
        )
        GameOwnership.objects.create(user=self.operator, game=self.game1)
        GameOwnership.objects.create(user=self.operator, game=self.game2)
        GameOwnership.objects.create(user=self.player, game=self.game1)

        self.mockdata = {
            'name': 'game4',
            'publisher': 'pub2',
            'max_limit': 4,
            'address': 'addr4',
            'description': 'abc'
        }

    ############################################################################
    # TEST CREATE
    ############################################################################

    # Expected result : Accepted, created a new game
    def test_create_game_by_operator_success(self):

        # Arrange
        self.client.force_authenticate(self.operator)

        # Act
        response_create = client.post('/games/', self.mockdata},
            format='json')

        # Assert
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

        response_get_game = client.get('/games/?name=game4')
        self.assertEqual(response_get_game.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get_game.data), 1) # Data exists


    # Expected result : Access denied
    def test_create_game_by_user_forbidden(self):

        # Arrange
        self.client.force_authenticate(self.player)

        # Act
        response_create = client.post('/games/', self.mockdata}, 
            format='json')

        # Assert
        self.assertEqual(response_create.status_code, \
            status.HTTP_403_FORBIDDEN)

        response_get_game = client.get('/games/?name=game4')
        self.assertEqual(response_get_game.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get_game.data), 0) # Data is not created


    ############################################################################
    # TEST READ (GET)
    ############################################################################

    def test_get_games(self):
        client1 = APIClient()
        client1.force_authenticate(user=self.operator)
        client2 = APIClient()
        client2.force_authenticate(user=self.player)
        clients = [client1, client2]

        response1 = client1.get('/games/?owned=1')
        response2 = client2.get('/games/?owned=1')

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 2)
        self.assertEqual(len(response2.data), 1)
        
        for client in clients:
            response3 = client.get('/games/?owned=1&name=game1')
            response4 = client.get('/games/?owned=1&name=game3')
            response5 = client.get('/games/')
            response6 = client.get('/games/1/')
            response7 = client.get('/games/?id=1&name=game1')
            response8 = client.get('/games/?publisher=pub1')
            response9 = client.get('/games/?owned=0')

            self.assertEqual(response3.status_code, status.HTTP_200_OK)
            self.assertEqual(response4.status_code, status.HTTP_200_OK)
            self.assertEqual(response5.status_code, status.HTTP_200_OK)
            self.assertEqual(response6.status_code, status.HTTP_200_OK)
            self.assertEqual(response7.status_code, status.HTTP_200_OK)
            self.assertEqual(response8.status_code, status.HTTP_200_OK)
            self.assertEqual(response9.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response3.data), 1)
            self.assertEqual(len(response4.data), 0)
            self.assertEqual(len(response5.data), 3)
            self.assertEqual(response6.data['id'], 1)
            self.assertEqual(len(response7.data), 1)
            self.assertEqual(len(response8.data), 2)
            self.assertEqual(len(response9.data), 3)

    def test_get_owned_games(self, client):
        client = APIClient()
        client


    ############################################################################
    # TEST CREATE
    ############################################################################

    # Expected : Accepted, update some of the fields
    def test_update_game_by_operator(self):
        client = APIClient()
        client.force_authenticate(user=self.operator)

        response_update = client.patch('/games/1/', data={
            'name': 'game10',
            'address': 'addr10'
        }, format='json')
        response = client.get('/games/1/')

        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['name'], 'game10')
        self.assertEqual(response.data['description'], 'a')
        self.assertEqual(response.data['address'], 'addr10')
        self.assertEqual(response.data['publisher'], 'pub1')
        self.assertEqual(response.data['max_limit'], 1)

    # Expected : Forbidden
    def test_update_game_by_user(self):
        client = APIClient()
        client.force_authenticate(user=self.player)

        response_update = client.patch('/games/1/', data={
            'name': 'game10',
            'address': 'addr10'
        }, format='json')
        response = client.get('/games/1/')

        self.assertEqual(response_update.status_code, \
            status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['name'], 'game1')
        self.assertEqual(response.data['description'], 'a')
        self.assertEqual(response.data['address'], 'addr1')
        self.assertEqual(response.data['publisher'], 'pub1')
        self.assertEqual(response.data['max_limit'], 1)

    # Expected : Allowed, delete game with certain id
    def test_delete_game_by_operator(self):
        client = APIClient()
        client.force_authenticate(user=self.operator)

        response_delete = client.delete('/games/3/')
        response1 = client.get('/games/')
        response2 = client.get('/games/?name=game3')

        self.assertEqual(response_delete.status_code, \
            status.HTTP_204_NO_CONTENT)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 2)
        self.assertEqual(len(response2.data), 0)

    # Expected : Forbidden
    def test_delete_game_by_user(self):
        client = APIClient()
        client.force_authenticate(user=self.player)

        response_delete = client.delete('/games/3/')
        response1 = client.get('/games/')
        response2 = client.get('/games/?name=game3')

        self.assertEqual(response_delete.status_code, \
            status.HTTP_403_FORBIDDEN)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 3)
        self.assertEqual(len(response2.data), 1)