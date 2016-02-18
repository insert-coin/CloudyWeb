from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import serializers
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient

from cloudygames.models import Game, PlayerSaveData
from cloudygames.serializers import GameSerializer

import json

# Create your tests here.

class CloudyGamesTests(APITestCase):

    def setUp(self):
        # Users
        self.user1 = User.objects.create(username="user1", password="user1", email="user1@email.com", first_name="firstname", last_name="lastname")
        self.user2 = User.objects.create(username="user2", password="user2", email="user2@email.com", first_name="firstname", last_name="lastname")

        # Games
        self.game1 = Game.objects.create(name="game1", publisher="pub1", max_limit=1, address="addr1")
        self.game2 = Game.objects.create(name="game2", publisher="pub1", max_limit=1, address="addr2")
        self.game3 = Game.objects.create(name="game3", publisher="pub1", max_limit=1, address="addr3")
        self.game1.users.add(self.user1, self.user2)
        self.game2.users.add(self.user1)

        # PlayerSaveData
        self.savedUser1Game1auto = PlayerSaveData.objects.create(player=self.user1, game=self.game1, saved_file="game1auto.txt")
        self.savedUser1Game1 = PlayerSaveData.objects.create(player=self.user1, game=self.game1, saved_file="game1.txt", is_autosaved=False)
        self.savedUser1Game2 = PlayerSaveData.objects.create(player=self.user1, game=self.game2, saved_file="game2.txt")

    def test_create_game(self):
        # Authenticate user1
        client = APIClient()
        client.force_authenticate(user=self.user1)

        request = client.post('/games/', data={'name': 'game4', 'publisher': 'pub2', 'max_limit': 4, 'address': 'addr4', 'users': [self.user1.username, self.user2.username]}, format='json')
        response1 = client.get('/games/')
        response2 = client.get('/games/?name=game4')

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 4)
        self.assertEqual(len(response2.data), 1)

    def test_get_gamelist(self):
        # Authenticate user1
        client = APIClient()
        client.force_authenticate(user=self.user1)

        # Get Request
        response1 = client.get('/games/?owned=0')
        response2 = client.get('/games/?id=1&name=game1')
        response3 = client.get('/games/?publisher=pub1')

        # Check
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 3)
        self.assertEqual(len(response2.data), 1)
        self.assertEqual(len(response3.data), 3)

    def test_get_owned_gamelist(self):
        # Authenticate users
        client1 = APIClient()
        client1.force_authenticate(user=self.user1)
        client2 = APIClient()
        client2.force_authenticate(user=self.user2)

        # Get Request
        response1 = client1.get('/games/?owned=1')
        response2 = client2.get('/games/?owned=1')

        # Check
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 2)
        self.assertEqual(len(response2.data), 1)

    def test_join_quit_game(self):
        # Authenticate users
        client1 = APIClient()
        client1.force_authenticate(user=self.user1)
        client2 = APIClient()
        client2.force_authenticate(user=self.user2)

        # Request
        # User1 joins game1 and game2
        response_create1 = client1.put('/game-session/', data={'game': self.game1.id}, format='json')
        response_create2 = client1.put('/game-session/', data={'game': self.game2.id}, format='json')
        # Request Get
        response_read_all = client1.get('/game-session/')
        response_read_game1 = client1.get('/game-session/?game=' + str(self.game1.id))
        # User1 quits game2
        response_delete = client1.delete('/game-session/?game=' + str(self.game2.id), {'player': '', 'game': self.game2.id}, format='json')
        response_read_game2 = client1.get('/game-session/?game=' + str(self.game2.id))  
        # User2 fails to join game1
        response_fail = client2.put('/game-session/', data={'game': self.game1.id}, format='json')
        
        # Assert
        # Check expected response
        self.assertEqual(response_create1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_create2.status_code, status.HTTP_201_CREATED)      
        self.assertEqual(response_read_all.status_code, status.HTTP_200_OK)
        self.assertEqual(response_read_game1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_delete.status_code, status.HTTP_200_OK)
        self.assertEqual(response_read_game2.status_code, status.HTTP_200_OK)
        self.assertEqual(response_fail.status_code, status.HTTP_400_BAD_REQUEST)
        # Check Response data
        self.assertEqual(len(response_read_all.data), 2)
        self.assertEqual(len(response_read_game1.data), 1)
        self.assertEqual(len(response_read_game2.data), 0)

    def test_player_save_data(self):
        # Authenticate user
        client = APIClient()
        client.force_authenticate(user=self.user1)

        # Request Get
        response_all = client.get('/save-data/')
        response_game2 = client.get('/save-data/?game=2')
        response_game1 = client.get('/save-data/?game=1')

        # Check
        self.assertEqual(response_all.status_code, status.HTTP_200_OK)
        self.assertEqual(response_game1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_game2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_all.data), 3)
        self.assertEqual(len(response_game1.data), 2)
        self.assertEqual(len(response_game2.data), 1)