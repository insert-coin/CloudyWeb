from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from rest_framework import test as drf_test
from rest_framework.authtoken.models import Token
from rest_framework import status


User = get_user_model()


class AccountTest(drf_test.APITestCase):


    def test_create_user(self):
        url = reverse('user-list')
        data = {
            'username': 'foo',
            'password': 'bar',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.last().username, 'foo')
        self.assertEqual(Token.objects.count(), 1)

    def test_token_auth(self):

        url = reverse('token-auth')
        data = {
            'username': 'foo',
            'password': 'bar',
        }
        user = User.objects.create_user(**data)

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'token': user.auth_token.key})

    def test_user_resource_by_anonymous(self):
        url = reverse('user-list')
        data = {
            'username': 'foo',
            'password': 'bar',
        }
        user = User.objects.create_user(**data)

        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"detail":"Authentication credentials were not provided."})


    def test_user_resource_by_staff(self):
        url = reverse('user-list')

        user = User.objects.create_user(**{
            'username': 'foo',
            'password': 'bar',
        })
        user.is_staff = True
        user.save()

        self.client.force_authenticate(user=user)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)