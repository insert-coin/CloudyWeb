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
        self.user1 = User.objects.create(username="user1", password="user1", email="user1@email.com", first_name="firstname", last_name="lastname")
        self.user2 = User.objects.create(username="user2", password="user2", email="user2@email.com", first_name="firstname", last_name="lastname")

        self.game1 = Game.objects.create(name="game1", publisher="pub1", max_limit=1, address="addr1")
        self.game2 = Game.objects.create(name="game2", publisher="pub1", max_limit=1, address="addr2")
        self.game3 = Game.objects.create(name="game3", publisher="pub1", max_limit=1, address="addr3")
        self.game1.users.add(self.user1, self.user2)
        self.game2.users.add(self.user1)

        self.savedUser1Game1auto = PlayerSaveData.objects.create(player=self.user1, game=self.game1, saved_file="game1auto.txt")
        self.savedUser1Game1 = PlayerSaveData.objects.create(player=self.user1, game=self.game1, saved_file="game1.txt", is_autosaved=False)
        self.savedUser1Game2 = PlayerSaveData.objects.create(player=self.user1, game=self.game2, saved_file="game2.txt")

    def test_get_gamelist(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.get('/games/?owned=0')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        response = client.get('/games/?id=1&name=game1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = client.get('/games/?publisher=pub1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_owned_gamelist(self):
        #user1
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.get('/games/?owned=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        #user2
        client = APIClient()
        client.force_authenticate(user=self.user2)
        response = client.get('/games/?owned=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_join_quit_game(self):
        #user1 joins game1 & 2
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.put('/game-session/', {'game': self.game1.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = client.put('/game-session/', {'game': self.game2.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #read user1's game session
        response = client.get('/game-session/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        response = client.get('/game-session/', {'game': self.game1.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        #user1 quits game2
        response = client.delete('/game-session/', {'game': self.game2.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = client.get('/game-session/', {'game': self.game2.id}, format='json')
        self.assertEqual(len(response.data), 0)
        #user2 fails to join game1
        client = APIClient()
        client.force_authenticate(user=self.user2)
        response = client.put('/game-session/', {'game': self.game1.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_player_save_data(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.get('/save-data/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        response = client.get('/save-data/?game=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        response = client.get('/save-data/?game=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)