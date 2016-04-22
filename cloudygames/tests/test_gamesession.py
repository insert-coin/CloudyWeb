
from unittest import mock
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient

from cloudygames.models import Game, GameOwnership, GameSession

import socket

CLOUDYWEB_CONNECTOR_PORT = 55556


class GameSessionAPITest(APITestCase):


    ############################################################################
    # Set Up necessary temporary database for the tests
    ############################################################################
    
    def setUp(self):
        patcher = mock.patch('socket.socket.connect',
                                  side_effect=socket.socket.connect)
        self.connect_to_cpp = patcher.start()
        self.addCleanup(patcher.stop)

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

        # Give game ownerships to users
        GameOwnership.objects.create(user=self.operator, game=self.game1)
        GameOwnership.objects.create(user=self.operator, game=self.game2)
        GameOwnership.objects.create(user=self.player, game=self.game2)
        GameOwnership.objects.create(user=self.player, game=self.game3)

        # Game sessions
        GameSession.objects.create(
            user=self.operator,
            game=self.game1,
            controller=0,
            streaming_port=30000
        )
        GameSession.objects.create(
            user=self.player,
            game=self.game3,
            controller=0,
            streaming_port=30000
        )


    ############################################################################
    # TEST CREATE (JOIN GAME)
    ############################################################################

    # Expected : Success
    def test_join_game_operator_has_the_game_success(self):

        # Arrange
        self.client.force_authenticate(self.operator)

        # Act
        response_create = self.client.post('/game-session/', data={
            'user': self.operator.username,
            'game': self.game2.id
        }, format='json')

        # Assert
        self.assertEqual(response_create.status_code,
            status.HTTP_201_CREATED)
        self.connect_to_cpp.assert_called_once_with(
                (self.game2.address, CLOUDYWEB_CONNECTOR_PORT))

        response_read_game2 = self.client.get('/game-session/?game=2')
        self.assertEqual(response_read_game2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_read_game2.data), 1)


    # Expected : Success, operator can create for all game
    def test_join_game_operator_does_not_have_the_game_success(self):

        # Arrange
        self.client.force_authenticate(self.operator)

        # Act
        response_create = self.client.post('/game-session/', data={
            'user': self.operator.username,
            'game': self.game3.id
        }, format='json')

        # Assert
        self.assertEqual(response_create.status_code,
            status.HTTP_201_CREATED)
        self.connect_to_cpp.assert_called_once_with(
                (self.game3.address, CLOUDYWEB_CONNECTOR_PORT))

        response_read_game3 = self.client.get('/game-session/?game=3')
        self.assertEqual(response_read_game3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_read_game3.data), 2)

    
    # Expected : Success, operator can create for all user all game
    def test_join_game_operator_create_for_other_success(self):

        # Arrange
        self.client.force_authenticate(self.operator)

        # Act
        response_create = self.client.post('/game-session/', data={
            'user': self.player.username,
            'game': self.game2.id
        }, format='json')

        # Assert
        self.assertEqual(response_create.status_code,
            status.HTTP_201_CREATED)
        self.connect_to_cpp.assert_called_once_with(
                (self.game2.address, CLOUDYWEB_CONNECTOR_PORT))

        response_read_game2 = self.client.get('/game-session/?game=2')
        self.assertEqual(response_read_game2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_read_game2.data), 1)


    # Expected : Success, player can create for their own
    def test_join_game_player_has_the_game_success(self):

        # Arrange
        self.client.force_authenticate(self.player)

        # Act
        response_create = self.client.post('/game-session/', data={
            'user': self.player.username,
            'game': self.game2.id
        }, format='json')

        # Assert
        self.assertEqual(response_create.status_code,
            status.HTTP_201_CREATED)
        self.connect_to_cpp.assert_called_once_with(
                (self.game2.address, CLOUDYWEB_CONNECTOR_PORT))

        response_read_game2 = self.client.get('/game-session/?game=2')
        self.assertEqual(response_read_game2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_read_game2.data), 1)


    # Expected : Forbidden
    def test_join_game_player_does_not_own_the_game_forbidden(self):

        # Arrange
        self.client.force_authenticate(self.player)

        # Act
        response_create = self.client.post('/game-session/', data={
            'user': self.player.username,
            'game': self.game1.id
        }, format='json') # Game Ownership problem

        # Assert
        self.assertEqual(response_create.status_code,
            status.HTTP_403_FORBIDDEN)
        self.connect_to_cpp.assert_not_called()


    # Expected : Forbidden, player can only create for their own
    def test_join_game_player_create_for_other_forbidden(self):

        # Arrange
        self.client.force_authenticate(self.player)

        # Act
        response_create = self.client.post('/game-session/', data={
            'user': self.operator.username,
            'game': self.game2.id
        }, format='json')

        # Assert
        self.assertEqual(response_create.status_code,
            status.HTTP_403_FORBIDDEN)
        self.connect_to_cpp.assert_not_called()


    # Expected : Can not create duplicated session
    def test_join_game_duplicate_failed(self):

        # Arrange
        self.client.force_authenticate(self.operator)

        # Act
        response_duplicate = self.client.post('/game-session/', data={
            'user': self.operator.username,
            'game': self.game1.id
        }, format='json') # Duplicate

        # Assert
        self.assertEqual(response_duplicate.status_code,
            status.HTTP_400_BAD_REQUEST)
        self.connect_to_cpp.assert_not_called()


    # Expected : Failed
    def test_join_game_invalid_failed(self):

        # Arrange
        self.client.force_authenticate(self.operator)

        # Act
        response_invalid = self.client.post('/game-session/', data={
            'user': self.operator.username,
            'game': '5'
        }, format='json') # Not a valid game id

        # Assert
        self.assertEqual(response_invalid.status_code,
            status.HTTP_400_BAD_REQUEST)
        self.connect_to_cpp.assert_not_called()


    # Expected : Failed
    def test_join_game_limit_exceeded_failed(self):

        # Arrange
        self.client.force_authenticate(self.operator)

        # Act
        response_limit = self.client.post('/game-session/', data={
            'user': self.player.username,
            'game': self.game1.id
        }, format='json') # controller id all used

        # Assert
        self.assertEqual(response_limit.status_code,
            status.HTTP_400_BAD_REQUEST)
        self.connect_to_cpp.assert_not_called()


    ############################################################################
    # TEST READ
    ############################################################################

    # Expected : Can access all
    def test_read_game_session_by_operator(self):

        # Arrange
        self.client.force_authenticate(self.operator)

        # Act
        response_read_all = self.client.get('/game-session/')
        response_filter_by_game = self.client.get('/game-session/?game=1')
        response_filter_by_user_self = self.client.get(
            '/game-session/?user=operator')
        response_filter_by_user_other = self.client.get(
            '/game-session/?user=player')
        response_read_owned = self.client.get('/game-session/1/')
        response_read_others = self.client.get('/game-session/2/')

        # Assert
        self.assertEqual(response_read_all.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_read_all.data), 2) # See all

        self.assertEqual(response_filter_by_game.status_code,
            status.HTTP_200_OK)
        self.assertEqual(len(response_filter_by_game.data), 1)

        self.assertEqual(response_filter_by_user_self.status_code,
            status.HTTP_200_OK)
        self.assertEqual(len(response_filter_by_user_self.data), 1)

        self.assertEqual(response_filter_by_user_other.status_code,
            status.HTTP_200_OK)
        self.assertEqual(len(response_filter_by_user_other.data), 1)

        self.assertEqual(response_read_owned.status_code, status.HTTP_200_OK)
        self.assertEqual(response_read_owned.data['id'], 1)

        self.assertEqual(response_read_others.status_code, status.HTTP_200_OK)
        self.assertEqual(response_read_others.data['id'], 2)


    # Expected : Can only access their own
    def test_read_game_session_by_player(self):

        # Arrange
        self.client.force_authenticate(self.player)

        # Act
        response_read_all = self.client.get('/game-session/')
        response_filter_by_game = self.client.get('/game-session/?game=1')
        response_filter_by_user_self = self.client.get(
            '/game-session/?user=player')
        response_filter_by_user_other = self.client.get(
            '/game-session/?user=operator')
        response_read_owned = self.client.get('/game-session/2/')
        response_read_others = self.client.get('/game-session/1/')

        # Assert
        self.assertEqual(response_read_all.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_read_all.data), 1) # Can only see own

        self.assertEqual(response_filter_by_game.status_code,
            status.HTTP_200_OK)
        self.assertEqual(len(response_filter_by_game.data), 0) # Don't have

        self.assertEqual(response_filter_by_user_self.status_code,
            status.HTTP_200_OK)
        self.assertEqual(len(response_filter_by_user_self.data), 1)

        self.assertEqual(response_filter_by_user_other.status_code,
            status.HTTP_200_OK)
        self.assertEqual(len(response_filter_by_user_other.data), 0)

        self.assertEqual(response_read_owned.status_code, status.HTTP_200_OK)
        self.assertEqual(response_read_owned.data['id'], 2)

        self.assertEqual(response_read_others.status_code,
            status.HTTP_404_NOT_FOUND) # Can not access


    ############################################################################
    # TEST UPDATE
    ############################################################################

    # Disabled
    def test_update_game_session(self):
        
        # Arrange
        self.client.force_authenticate(self.operator)

        # Act
        response_update_owned = self.client.patch('/game-session/1/', data={
            'game': self.game2.id
        }, format='json')
        response_update_others = self.client.patch('/game-session/2/', data={
            'controller': 100
        }, format='json')

        # Assert
        self.assertEqual(response_update_owned.status_code,
            status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_update_others.status_code,
            status.HTTP_403_FORBIDDEN)


    ############################################################################
    # TEST DELETE (QUIT GAME)
    ############################################################################

    # Expected: Can delete all
    def test_quit_game_by_operator(self):

        # Arrange
        self.client.force_authenticate(self.operator)

        # Act
        response_delete_owned = self.client.delete('/game-session/1/')
        response_delete_others = self.client.delete('/game-session/2/')

        # Assert
        self.assertEqual(response_delete_owned.status_code,
            status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_delete_others.status_code,
            status.HTTP_204_NO_CONTENT)

        response_read_all = self.client.get('/game-session/')
        self.assertEqual(response_read_all.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_read_all.data), 0)


    # Expected : Can delete their own
    def test_quit_game_by_player_success(self):

        # Arrange
        self.client.force_authenticate(self.player)

        # Act
        response_delete_owned = self.client.delete('/game-session/2/')

        # Assert
        self.assertEqual(response_delete_owned.status_code,
            status.HTTP_204_NO_CONTENT)
        
        response_read = self.client.get('/game-session/2/')
        self.assertEqual(response_read.status_code, status.HTTP_404_NOT_FOUND)


    # Expected : Cannot delete their others'
    def test_quit_others_game_by_player_failed(self):

        # Arrange
        self.client.force_authenticate(self.player)

        # Act
        response_delete_others = self.client.delete('/game-session/1/')

        # Assert
        self.assertEqual(response_delete_others.status_code,
            status.HTTP_404_NOT_FOUND)
