from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import serializers

from rest_framework import status
from rest_framework.test import APITestCase

from cloudygames.models import Game

import json

# Create your tests here.

class AccountTests(APITestCase):

    def test_get_gamelist(self):
        response = self.client.get('/games/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(json.dumps(response.data), serializers.serialize('json', Game.objects.all()))