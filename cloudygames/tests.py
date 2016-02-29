from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import serializers
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient

from cloudygames.models import Game, PlayerSaveData, GameOwnership
from cloudygames.serializers import GameSerializer

import json

# Create your tests here.

class CloudyGamesTests(APITestCase):

    # Set Up necessary temporary database for the tests
    def setUp(self):
        # Users (User 1 = Operator, User 2 = Normal User)
        self.user1 = User.objects.create(
            username="user1",
            password="user1",
            email="user1@email.com",
            first_name="firstname",
            last_name="lastname"
        )
        self.user1.is_staff = True
        self.user1.save()
        self.user2 = User.objects.create(
            username="user2",
            password="user2",
            email="user2@email.com",
            first_name="firstname",
            last_name="lastname"
        )

        # Game
        self.game1 = Game.objects.create(
            name="game1",
            publisher="pub1",
            max_limit=1,
            address="addr1"
        )
        self.game2 = Game.objects.create(
            name="game2",
            publisher="pub1",
            max_limit=1,
            address="addr2"
        )
        self.game3 = Game.objects.create(
            name="game3",
            publisher="pub2",
            max_limit=4,
            address="addr3"
        )
        GameOwnership.objects.create(user=self.user1, game=self.game1)
        GameOwnership.objects.create(user=self.user1, game=self.game2)
        GameOwnership.objects.create(user=self.user2, game=self.game1)

        # PlayerSaveData
        self.savedUser1Game1auto = PlayerSaveData.objects.create(
            user=self.user1,
            game=self.game1,
            saved_file="game1auto.txt"
        )
        self.savedUser1Game1 = PlayerSaveData.objects.create(
            user=self.user1,
            game=self.game1,
            saved_file="game1.txt",
            is_autosaved=False
        )
        self.savedUser1Game2 = PlayerSaveData.objects.create(
            user=self.user1,
            game=self.game2,
            saved_file="game2.txt"
        )

    ############################################################# TEST GAME #############################################################

    # Expected result : Accepted, created a new game
    def test_create_game_by_operator(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response_create = client.post('/games/', data={
            'name': 'game4',
            'publisher': 'pub2',
            'max_limit': 4,
            'address': 'addr4'
        }, format='json')
        response1 = client.get('/games/')
        response2 = client.get('/games/?name=game4')

        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 4)
        self.assertEqual(len(response2.data), 1)

    # Expected result : Access denied
    def test_create_game_by_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)

        response_create = client.post('/games/', data={
            'name': 'game4',
            'publisher': 'pub2',
            'max_limit': 4,
            'address': 'addr4'
        }, format='json')
        response1 = client.get('/games/')
        response2 = client.get('/games/?name=game4')

        self.assertEqual(response_create.status_code, \
            status.HTTP_403_FORBIDDEN)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 3)
        self.assertEqual(len(response2.data), 0)

    def test_get_games(self):
        client1 = APIClient()
        client1.force_authenticate(user=self.user1)
        client2 = APIClient()
        client2.force_authenticate(user=self.user2)
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

    # Expected : Accepted, update some of the fields
    def test_update_game_by_operator(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response_update = client.patch('/games/1/', data={
            'name': 'game10',
            'address': 'addr10'
        }, format='json')
        response = client.get('/games/1/')

        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['name'], 'game10')
        self.assertEqual(response.data['address'], 'addr10')
        self.assertEqual(response.data['publisher'], 'pub1')
        self.assertEqual(response.data['max_limit'], 1)

    # Expected : Forbidden
    def test_update_game_by_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)

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
        self.assertEqual(response.data['address'], 'addr1')
        self.assertEqual(response.data['publisher'], 'pub1')
        self.assertEqual(response.data['max_limit'], 1)

    # Expected : Allowed, delete game with certain id
    def test_delete_game_by_operator(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

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
        client.force_authenticate(user=self.user2)

        response_delete = client.delete('/games/3/')
        response1 = client.get('/games/')
        response2 = client.get('/games/?name=game3')

        self.assertEqual(response_delete.status_code, \
            status.HTTP_403_FORBIDDEN)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 3)
        self.assertEqual(len(response2.data), 1)

    ##################################################### TEST GAME OWNERSHIP ###################################################

    # Expected : No restriction, can create any GameOwnership
    def test_buy_game_by_operator(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response_create1 = client.post('/game-ownership/', data={
            'user': self.user1.username,
            'game': self.game1.id
        }, format='json') # Duplicate
        response_create2 = client.post('/game-ownership/', data={
            'user': self.user1.username,
            'game': self.game3.id
        }, format='json')
        response_create3 = client.post('/game-ownership/', data={
            'user': self.user2.username,
            'game': self.game3.id
        }, format='json')
        response1 = client.get('/game-ownership/')
        response2 = client.get('/game-ownership/?user=user1')
        response3 = client.get('/game-ownership/?user=user2')
        response4 = client.get('/game-ownership/?game=3')
        
        self.assertEqual(response_create1.status_code, \
            status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_create2.status_code, \
            status.HTTP_201_CREATED)
        self.assertEqual(response_create3.status_code, \
            status.HTTP_201_CREATED)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response4.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 5)
        self.assertEqual(len(response2.data), 3)
        self.assertEqual(len(response3.data), 2)
        self.assertEqual(len(response4.data), 2)

    # Expected : Can only create their own
    def test_buy_game_by_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)

        response_create1 = client.post('/game-ownership/', data={
            'user': self.user1.username,
            'game': self.game3.id
        }, format='json') # Forbidden
        response_create2 = client.post('/game-ownership/', data={
            'user': self.user2.username,
            'game': self.game3.id
        }, format='json')
        
        self.assertEqual(response_create1.status_code, \
            status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_create2.status_code, \
            status.HTTP_201_CREATED)

    # Expected : Allow all
    def test_read_game_ownership_by_operator(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response1 = client.get('/game-ownership/')
        response2 = client.get('/game-ownership/?user=user1')
        response3 = client.get('/game-ownership/?user=user2')
        response4 = client.get('/game-ownership/?game=1')
        response5 = client.get('/game-ownership/1/')
        response6 = client.get('/game-ownership/3/')

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response4.status_code, status.HTTP_200_OK)
        self.assertEqual(response5.status_code, status.HTTP_200_OK)
        self.assertEqual(response6.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response1.data), 3)
        self.assertEqual(len(response2.data), 2)
        self.assertEqual(len(response3.data), 1)
        self.assertEqual(len(response4.data), 2)
        self.assertEqual(response5.data['id'], 1)
        self.assertEqual(response6.data['id'], 3)
    
    # Expected: Can only see their own
    def test_read_game_ownership_by_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)

        response1 = client.get('/game-ownership/')
        response2 = client.get('/game-ownership/?user=user1')
        response3 = client.get('/game-ownership/?user=user2')
        response4 = client.get('/game-ownership/?game=1')
        response5 = client.get('/game-ownership/1/') # Can not access
        response6 = client.get('/game-ownership/3/')

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response4.status_code, status.HTTP_200_OK)
        self.assertEqual(response5.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response6.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response1.data), 1)
        self.assertEqual(len(response2.data), 0)
        self.assertEqual(len(response3.data), 1)
        self.assertEqual(len(response4.data), 1)
        self.assertEqual(response6.data['id'], 3)

    # Disabled
    def test_update_game_ownership(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response_update1 = client.patch('/game-ownership/1/', data={
            'game':self.game2.id}, format='json')
        response_update2 = client.patch('/game-ownership/3/', data={
            'user': self.user2.username}, format='json')

        self.assertEqual(response_update1.status_code, \
            status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_update2.status_code, \
            status.HTTP_403_FORBIDDEN)

    def test_delete_game_ownership_by_operator(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)        

        response_delete1 = client.delete('/game-ownership/1/')
        response_delete2 = client.delete('/game-ownership/3/')
        response1 = client.get('/game-ownership/')
        response2 = client.get('/game-ownership/1/') # Deleted
        response3 = client.get('/game-ownership/?user=user2')

        self.assertEqual(response_delete1.status_code, \
            status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_delete2.status_code, \
            status.HTTP_204_NO_CONTENT)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 1)
        self.assertEqual(len(response3.data), 0)

    def test_delete_game_ownership_by_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)        

        response_delete1 = client.delete('/game-ownership/1/') # Does not have access
        response_delete2 = client.delete('/game-ownership/3/')
        response1 = client.get('/game-ownership/')
        response2 = client.get('/game-ownership/3/') # Deleted
        response3 = client.get('/game-ownership/?user=user2')

        self.assertEqual(response_delete1.status_code, \
            status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_delete2.status_code, \
            status.HTTP_204_NO_CONTENT)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 0)
        self.assertEqual(len(response3.data), 0)

    ##################################################### TEST GAME SESSION #####################################################
    
    def test_join_game(self):
        client1 = APIClient()
        client1.force_authenticate(user=self.user1)
        client2 = APIClient()
        client2.force_authenticate(user=self.user2)

        GameOwnership.objects.create(user=self.user2, game=self.game3)

        # User 1 joins
        response_create1 = client1.post('/game-session/', data={
            'user': 'user1',
            'game': self.game1.id
        }, format='json')
        response_create2 = client1.post('/game-session/', data={
            'user': 'user1', 'game': self.game2.id}, format='json')
        response_create3 = client1.post('/game-session/', data={
            'user': 'user1',
            'game': self.game3.id
        }, format='json') # Ownership problem
        response_create4 = client1.post('/game-session/', data={
            'user': 'user1',
            'game': self.game1.id
        }, format='json') # Duplicate
        response_create5 = client1.post('/game-session/', data={
            'user': 'user2',
            'game': self.game3.id
        }, format='json')
        response_create6 = client1.post('/game-session/', data={
            'user': 'user2',
            'game': '5'
        }, format='json') # Not a valid game id
        # Request Get
        response_read_all = client1.get('/game-session/')
        response_read_game1 = client1.get('/game-session/?game=1')
        response_read_user1 = client1.get('/game-session/?user=user1')
        # User 2 fails to join
        response_create7 = client2.post('/game-session/', data={
            'user': 'user2',
            'game': self.game1.id
        }, format='json') # Limit exceeded
        response_create8 = client2.post('/game-session/', data={
            'user': 'user1',
            'game': self.game1.id
        }, format='json') # Access denied

        self.assertEqual(response_create1.status_code, \
            status.HTTP_201_CREATED)
        self.assertEqual(response_create2.status_code, \
            status.HTTP_201_CREATED)
        self.assertEqual(response_create3.status_code, \
            status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_create4.status_code, \
            status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_create5.status_code, \
            status.HTTP_201_CREATED)
        self.assertEqual(response_create6.status_code, \
            status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_create7.status_code, \
            status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_create8.status_code, \
            status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_read_all.status_code, status.HTTP_200_OK)
        self.assertEqual(response_read_game1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_read_user1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_read_all.data), 3)
        self.assertEqual(len(response_read_game1.data), 1)
        self.assertEqual(len(response_read_user1.data), 2)

    def test_read_game_session_by_operator(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        # Joins game
        response_create1 = client.post('/game-session/', data={
            'user': 'user1',
            'game': self.game2.id
        }, format='json')
        response_create2 = client.post('/game-session/', data={
            'user': 'user2',
            'game': self.game1.id
        }, format='json')
        # Read Game Session
        response1 = client.get('/game-session/')
        response2 = client.get('/game-session/?game=1')
        response3 = client.get('/game-session/?user=user1')
        response4 = client.get('/game-session/?user=user2')
        response5 = client.get('/game-session/1/')
        response6 = client.get('/game-session/2/')

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response4.status_code, status.HTTP_200_OK)
        self.assertEqual(response5.status_code, status.HTTP_200_OK)
        self.assertEqual(response6.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 2)
        self.assertEqual(len(response2.data), 1)
        self.assertEqual(len(response3.data), 1)
        self.assertEqual(len(response4.data), 1)
        self.assertEqual(response5.data['id'], 1)
        self.assertEqual(response6.data['id'], 2)

    def test_read_game_session_by_user(self):
        client1 = APIClient()
        client1.force_authenticate(user=self.user1)
        client2 = APIClient()
        client2.force_authenticate(user=self.user2)

        # Joins game
        response_create1 = client1.post('/game-session/', data={
            'user': 'user1',
            'game': self.game2.id
        }, format='json')
        response_create2 = client1.post('/game-session/', data={
            'user': 'user2',
            'game': self.game1.id
        }, format='json')
        # Read Game Session
        response1 = client2.get('/game-session/')
        response2 = client2.get('/game-session/?game=1')
        response3 = client2.get('/game-session/?user=user1')
        response4 = client2.get('/game-session/?user=user2')
        response5 = client2.get('/game-session/1/')
        response6 = client2.get('/game-session/2/')

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response4.status_code, status.HTTP_200_OK)
        self.assertEqual(response5.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response6.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 1)
        self.assertEqual(len(response2.data), 1)
        self.assertEqual(len(response3.data), 0)
        self.assertEqual(len(response4.data), 1)
        self.assertEqual(response6.data['id'], 2)

    # Disabled
    def test_update_game_session(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        # Joins game
        response_create1 = client.post('/game-session/', data={
            'user': 'user1',
            'game': self.game2.id
        }, format='json')
        response_create2 = client.post('/game-session/', data={
            'user': 'user2',
            'game': self.game1.id
        }, format='json')
        # Update game
        response_update1 = client.patch('/game-session/1/', data={
            'game':self.game2.id
        }, format='json')
        response_update2 = client.patch('/game-ownership/2/', data={
            'controller': 100
        }, format='json')

        self.assertEqual(response_create1.status_code, \
            status.HTTP_201_CREATED)
        self.assertEqual(response_create2.status_code, \
            status.HTTP_201_CREATED)
        self.assertEqual(response_update1.status_code, \
            status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_update2.status_code, \
            status.HTTP_403_FORBIDDEN)

    def test_quit_game(self):
        client1 = APIClient()
        client1.force_authenticate(user=self.user1)
        client2 = APIClient()
        client2.force_authenticate(user=self.user2)

        # Joins game
        response_create1 = client1.post('/game-session/', data={
            'user': 'user1',
            'game': self.game2.id
        }, format='json')
        response_create2 = client1.post('/game-session/', data={
            'user': 'user2',
            'game': self.game1.id
        }, format='json')
        # Quits game
        response_delete1 = client2.delete('/game-session/1/') # Access denied
        response_delete2 = client1.delete('/game-session/1/')
        response_delete3 = client2.delete('/game-session/2/')
        # Check
        response_read = client1.get('/game-session/1/')
        response_read_all = client1.get('/game-session/')
        
        self.assertEqual(response_create1.status_code, \
            status.HTTP_201_CREATED)
        self.assertEqual(response_create2.status_code, \
            status.HTTP_201_CREATED)
        self.assertEqual(response_delete1.status_code, \
            status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_delete2.status_code, \
            status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_delete3.status_code, \
            status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_read.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_read_all.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_read_all.data), 0)

    ##################################################### TEST SAVE DATA #####################################################

    # Expected : Allowed
    def test_create_save_data_by_operator(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response_create1 = client.post('/save-data/', data={
            'user': 'user1',
            'game': '3',
            'saved_file': 'file1.txt'
        })
        response_create2 = client.post('/save-data/', data={
            'user': 'user2',
            'game': '3',
            'saved_file': 'file2.txt'
        })
        response1 = client.get('/save-data/')
        response2 = client.get('/save-data/?game=3')

        self.assertEqual(response_create1.status_code, \
            status.HTTP_201_CREATED)
        self.assertEqual(response_create2.status_code, \
            status.HTTP_201_CREATED)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 5)
        self.assertEqual(len(response2.data), 2)

    # Expected : Can only access own
    def test_create_save_data_by_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)

        response_create1 = client.post('/save-data/', data={
            'user': 'user1',
            'game': '3',
            'saved_file': 'file1.txt'
        }) # Access denied, can only create own
        response_create2 = client.post('/save-data/', data={
            'user': 'user2',
            'game': '3',
            'saved_file': 'file2.txt'
        })
        response1 = client.get('/save-data/')
        response2 = client.get('/save-data/?game=3')

        self.assertEqual(response_create1.status_code, \
            status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_create2.status_code, \
            status.HTTP_201_CREATED)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 1)
        self.assertEqual(len(response2.data), 1)

    # Expected : Allow all
    def test_read_save_data_by_operator(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response_create = client.post('/save-data/', data={
            'user': 'user2',
            'game': '3',
            'saved_file': 'file2.txt'
        })

        response1 = client.get('/save-data/')
        response2 = client.get('/save-data/1/')
        response3 = client.get('/save-data/?game=2')
        response4 = client.get('/save-data/?user=user1')
        response5 = client.get('/save-data/?user=user2')

        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response4.status_code, status.HTTP_200_OK)
        self.assertEqual(response5.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 4)
        self.assertEqual(response2.data['id'], 1)
        self.assertEqual(len(response3.data), 1)
        self.assertEqual(len(response4.data), 3)
        self.assertEqual(len(response5.data), 1)

    # Expected : Can only access their own
    def test_read_save_data_by_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)

        response_create = client.post('/save-data/', data={
            'user': 'user2',
            'game': '3',
            'saved_file': 'file2.txt'
        })

        response1 = client.get('/save-data/')
        response2 = client.get('/save-data/1/')
        response3 = client.get('/save-data/?game=2')
        response4 = client.get('/save-data/?user=user1')
        response5 = client.get('/save-data/?user=user2')

        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response4.status_code, status.HTTP_200_OK)
        self.assertEqual(response5.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 1)
        self.assertEqual(len(response3.data), 0)
        self.assertEqual(len(response4.data), 0)
        self.assertEqual(len(response5.data), 1)
    
    # Expected : Allowed all
    def test_update_save_data_by_operator(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response_create = client.post('/save-data/', data={
            'user': 'user2',
            'game': '3',
            'saved_file': 'file2.txt'
        })
        response_update1 = client.patch('/save-data/1/', data={
            'saved_file': 'file01.txt'
        }, format='json')
        response_update2 = client.patch('/save-data/4/', data={
            'saved_file': 'file02.txt'
        }, format='json')
        response1 = client.get('/save-data/1/')
        response2 = client.get('/save-data/4/')

        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_update2.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data['id'], 1)
        self.assertEqual(response1.data['saved_file'], 'file01.txt')
        self.assertEqual(response2.data['id'], 4)
        self.assertEqual(response2.data['saved_file'], 'file02.txt')

    # Expected : Can only update their own
    def test_update_save_data_by_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)

        response_create = client.post('/save-data/', data={
            'user': 'user2',
            'game': '3',
            'saved_file': 'file2.txt'
        })
        response_update1 = client.patch('/save-data/1/', data={
            'saved_file': 'file01.txt'
        }, format='json') # Can not update unless their own
        response_update2 = client.patch('/save-data/4/', data={
            'saved_file': 'file02.txt'
        }, format='json')
        response1 = client.get('/save-data/1/') # Can't read unless their own
        response2 = client.get('/save-data/4/')

        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update1.status_code, \
            status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_update2.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data['id'], 4)
        self.assertEqual(response2.data['saved_file'], 'file02.txt')

    # Expected : Allowed all
    def test_delete_save_data_by_operator(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response_create = client.post('/save-data/', data={
            'user': 'user2',
            'game': '3',
            'saved_file': 'file2.txt'
        })
        response_delete1 = client.delete('/save-data/1/')
        response_delete2 = client.delete('/save-data/4/')
        response1 = client.get('/save-data/1/')
        response2 = client.get('/save-data/4/')
        response3 = client.get('/save-data/')

        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_delete1.status_code, \
            status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_delete2.status_code, \
            status.HTTP_204_NO_CONTENT)
        self.assertEqual(response1.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response3.data), 2)

    # Expected : Can only delete their own
    def test_delete_save_data_by_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)

        response_create = client.post('/save-data/', data={
            'user': 'user2',
            'game': '3',
            'saved_file': 'file2.txt'
        })
        # Can not delete unless their own
        response_delete1 = client.delete('/save-data/1/')
        response_delete2 = client.delete('/save-data/4/')
        response1 = client.get('/save-data/4/')
        response2 = client.get('/save-data/')

        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_delete1.status_code, \
            status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_delete2.status_code, \
            status.HTTP_204_NO_CONTENT)
        self.assertEqual(response1.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 0)