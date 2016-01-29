from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import serializers
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient

from cloudygames.models import Game
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

    def test_get_gamelist(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.get('/games/')
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