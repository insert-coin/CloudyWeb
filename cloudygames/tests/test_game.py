
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient

from cloudygames.models import Game, GameOwnership


class GameAPITest(APITestCase):


    ############################################################################
    # Set Up necessary temporary database for the tests
    ############################################################################
    
    def setUp(self):

        # Users (Role: Operator & Player)        
        self.operator = User.objects.create(
            username="operator",
            password="operator",
            email="operator@email.com",
            first_name="firstname",
            last_name="lastname",
            is_staff=True
        )
        self.player = User.objects.create(
            username="player",
            password="player",
            email="player@email.com",
            first_name="firstname",
            last_name="lastname"
        )

        # Games
        self.game1 = Game.objects.create(
            name="game1",
            publisher="pub1",
            max_limit=1,
            address="http://127.0.0.1/",
            description="a"
        )
        self.game2 = Game.objects.create(
            name="game2",
            publisher="pub1",
            max_limit=1,
            address="http://127.0.0.2/",
            description="b"
        )
        self.game3 = Game.objects.create(
            name="game3",
            publisher="pub2",
            max_limit=4,
            address="http://127.0.0.3/",
            description="c"
        )

        # Give game ownerships to users
        GameOwnership.objects.create(user=self.operator, game=self.game1)
        GameOwnership.objects.create(user=self.operator, game=self.game2)
        GameOwnership.objects.create(user=self.player, game=self.game1)

        # Mock data for game creation
        self.mockdata = {
            'name': 'game4',
            'publisher': 'pub2',
            'max_limit': 4,
            'address': 'http://127.0.0.4/',
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
        response_create = self.client.post('/games/', self.mockdata, format='json')

        # Assert
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

        response_get_game = self.client.get('/games/?name=game4')
        self.assertEqual(response_get_game.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get_game.data), 1) # Data exists


    # Expected result : Access denied
    def test_create_game_by_player_forbidden(self):

        # Arrange
        self.client.force_authenticate(self.player)

        # Act
        response_create = self.client.post('/games/', self.mockdata, format='json')

        # Assert
        self.assertEqual(response_create.status_code,
            status.HTTP_403_FORBIDDEN)

        response_get_game = self.client.get('/games/?name=game4')
        self.assertEqual(response_get_game.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get_game.data), 0) # Data is not created


    ############################################################################
    # TEST READ (GET)
    ############################################################################

    def test_get_games(self):
        # Arrange
        self.client.force_authenticate(self.player)

        # Act
        response_get_all = self.client.get('/games/')
        response_get_by_id = self.client.get('/games/1/')

        # Assert
        self.assertEqual(response_get_all.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get_all.data), 3)

        self.assertEqual(response_get_by_id.status_code, status.HTTP_200_OK)
        self.assertEqual(response_get_by_id.data['id'], 1)


    def test_game_filter(self):

        # Arrange
        self.client.force_authenticate(self.player)

        # Act        
        response_filter1 = self.client.get('/games/?id=1&name=game1')
        response_filter2 = self.client.get('/games/?publisher=pub1')
        
        # Assert
        self.assertEqual(response_filter1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_filter1.data), 1)

        self.assertEqual(response_filter2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_filter2.data), 2)


    def test_owned_games(self):

        # Arrange
        self.client.force_authenticate(self.player)

        # Act
        response_owned = self.client.get('/games/?owned=1')
        response_not_owned = self.client.get('/games/?owned=0')

        # Assert
        self.assertEqual(response_owned.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_owned.data), 1)

        self.assertEqual(response_not_owned.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_not_owned.data), 3)


    ############################################################################
    # TEST UPDATE
    ############################################################################

    # Expected : Accepted, update some of the fields
    def test_update_game_by_operator_success(self):

        # Arrange
        self.client.force_authenticate(self.operator)

        # Act
        response_update = self.client.patch('/games/1/', data={
            'name': 'game10',
            'address': 'http://127.0.1.1/'
        }, format='json')

        # Assert
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)

        response = self.client.get('/games/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['name'], 'game10')
        self.assertEqual(response.data['description'], 'a')
        self.assertEqual(response.data['address'], 'http://127.0.1.1/')
        self.assertEqual(response.data['publisher'], 'pub1')
        self.assertEqual(response.data['max_limit'], 1)


    # Expected : Forbidden, no change should be made
    def test_update_game_by_player_forbidden(self):

        # Arrange
        self.client.force_authenticate(self.player)

        # Act
        response_update = self.client.patch('/games/1/', data={
            'name': 'game10',
            'address': 'http://127.0.1.1/'
        }, format='json')

        # Assert
        self.assertEqual(response_update.status_code,
            status.HTTP_403_FORBIDDEN)

        response = self.client.get('/games/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['name'], 'game1')
        self.assertEqual(response.data['description'], 'a')
        self.assertEqual(response.data['address'], 'http://127.0.0.1/')
        self.assertEqual(response.data['publisher'], 'pub1')
        self.assertEqual(response.data['max_limit'], 1)


    ############################################################################
    # TEST DELETE
    ############################################################################

    # Expected : Allowed, delete game with certain id
    def test_delete_game_by_operator_success(self):

        # Arrange
        self.client.force_authenticate(self.operator)

        # Act
        response_delete = self.client.delete('/games/3/')
        
        # Assert
        self.assertEqual(response_delete.status_code,
            status.HTTP_204_NO_CONTENT)

        response = self.client.get('/games/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # Expected : Forbidden, data should not be deleted
    def test_delete_game_by_player_forbidden(self):
        
        # Arrange
        self.client.force_authenticate(self.player)

        # Act
        response_delete = self.client.delete('/games/3/')

        # Assert
        self.assertEqual(response_delete.status_code,
            status.HTTP_403_FORBIDDEN)
        
        response = self.client.get('/games/3/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 3)