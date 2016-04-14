
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient

from cloudygames.models import Game, GameOwnership


class GameOwnershipAPITest(APITestCase):


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


    ############################################################################
    # TEST CREATE (BUY)
    ############################################################################

    # Expected : No restriction
    #            Can create any GameOwnership for any user with any game
    def test_buy_game_by_operator_success(self):

        # Arrange
        self.client.force_authenticate(self.operator)

        # Act
        response_create_own = self.client.post('/game-ownership/', data={
            'user': self.operator.username,
            'game': self.game3.id
        }, format='json')
        response_create_others = self.client.post('/game-ownership/', data={
            'user': self.player.username,
            'game': self.game3.id
        }, format='json')

        # Assert
        self.assertEqual(response_create_own.status_code,
            status.HTTP_201_CREATED)
        self.assertEqual(response_create_others.status_code,
            status.HTTP_201_CREATED)

        response_count_game3 = self.client.get('/game-ownership/?game=3')
        self.assertEqual(response_count_game3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_count_game3.data), 2)


    # Expected : Can create their own
    def test_buy_game_by_player_success(self):

        # Arrange
        self.client.force_authenticate(self.player)

        # Act
        response_create = self.client.post('/game-ownership/', data={
            'user': self.player.username,
            'game': self.game3.id
        }, format='json')

        # Assert
        self.assertEqual(response_create.status_code,
        status.HTTP_201_CREATED)

        response_count_game3 = self.client.get('/game-ownership/?game=3')
        self.assertEqual(response_count_game3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_count_game3.data), 1)


    # Expected : Cannot create others'
    def test_buy_game_by_player_forbidden(self):

        # Arrange
        self.client.force_authenticate(self.player)

        # Act
        response_create = self.client.post('/game-ownership/', data={
            'user': self.operator.username,
            'game': self.game3.id
        }, format='json')

        # Assert
        self.assertEqual(response_create.status_code,
            status.HTTP_403_FORBIDDEN)

        response_count_game3 = self.client.get('/game-ownership/?game=3')
        self.assertEqual(response_count_game3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_count_game3.data), 0) # Not created


    # Can not create duplicate games
    def test_buy_game_duplicate_failed(self):

        # Arrange
        self.client.force_authenticate(self.operator)

        # Assert
        response_duplicate = self.client.post('/game-ownership/', data={
            'user': self.operator.username,
            'game': self.game1.id
        }, format='json')

        # Act
        self.assertEqual(response_duplicate.status_code,
            status.HTTP_400_BAD_REQUEST)


    ############################################################################
    # TEST READ
    ############################################################################

    # Expected : Allow all
    def test_read_game_ownership_by_operator(self):

        # Arrange
        self.client.force_authenticate(self.operator)

        # Act
        response_all = self.client.get('/game-ownership/')
        response_owned_all = self.client.get('/game-ownership/?user=operator')
        response_others_all = self.client.get('/game-ownership/?user=player')
        response_owned_game1 = self.client.get('/game-ownership/?game=1')
        response_owned = self.client.get('/game-ownership/1/')
        response_others = self.client.get('/game-ownership/3/')

        # Asssert
        self.assertEqual(response_all.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_all.data), 3)

        self.assertEqual(response_owned_all.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_owned_all.data), 2)

        self.assertEqual(response_others_all.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_others_all.data), 1)

        self.assertEqual(response_owned_game1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_owned_game1.data), 2)

        self.assertEqual(response_owned.status_code, status.HTTP_200_OK)
        self.assertEqual(response_owned.data['id'], 1)

        self.assertEqual(response_others.status_code, status.HTTP_200_OK)
        self.assertEqual(response_others.data['id'], 3)

    
    # Expected: Can only see their own
    def test_read_game_ownership_by_player(self):

        # Arrange
        self.client.force_authenticate(self.player)

        # Act
        response_all = self.client.get('/game-ownership/')
        response_others_all = self.client.get('/game-ownership/?user=operator')
        response_owned_all = self.client.get('/game-ownership/?user=player')
        response_owned_game1 = self.client.get('/game-ownership/?game=1')
        response_others = self.client.get('/game-ownership/1/') # Can not access
        response_owned = self.client.get('/game-ownership/3/')
        
        # Asssert
        self.assertEqual(response_all.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_all.data), 1) # Can only see their own

        self.assertEqual(response_others_all.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_others_all.data), 0) # Empty list

        self.assertEqual(response_owned_all.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_owned_all.data), 1)

        self.assertEqual(response_owned_game1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_owned_game1.data), 1)

        self.assertEqual(response_others.status_code,
            status.HTTP_404_NOT_FOUND) # Can not access

        self.assertEqual(response_owned.status_code, status.HTTP_200_OK)
        self.assertEqual(response_owned.data['id'], 3)
    

    ############################################################################
    # TEST UPDATE
    ############################################################################

    # Disabled
    def test_update_game_ownership(self):
        
        # Arrange
        self.client.force_authenticate(self.operator)

        # Act
        response_update_owned = self.client.patch('/game-ownership/1/', data={
            'game':self.game2.id}, format='json')
        response_update_others = self.client.patch('/game-ownership/3/', data={
            'user': self.player.username}, format='json')

        # Assert
        self.assertEqual(response_update_owned.status_code,
            status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_update_others.status_code,
            status.HTTP_403_FORBIDDEN)


    ############################################################################
    # TEST DELETE
    ############################################################################

    # Expected : Allow all
    def test_delete_game_ownership_by_operator(self):
        
        # Arrange
        self.client.force_authenticate(self.operator)        

        # Act
        response_delete_owned = self.client.delete('/game-ownership/1/')
        response_delete_others = self.client.delete('/game-ownership/3/')

        # Assert
        self.assertEqual(response_delete_owned.status_code,
            status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_delete_others.status_code,
            status.HTTP_204_NO_CONTENT)

        response_check_owned = self.client.get('/game-ownership/1/') # Deleted
        self.assertEqual(response_check_owned.status_code,
            status.HTTP_404_NOT_FOUND)
        
        response_check_others = self.client.get('/game-ownership/3/') # Deleted
        self.assertEqual(response_check_others.status_code,
            status.HTTP_404_NOT_FOUND)
        

    # Expected : Can only delete their own
    def test_delete_game_ownership_by_player(self):

        # Arrange
        self.client.force_authenticate(self.player)        

        # Act
        response_delete_others = self.client.delete('/game-ownership/1/')
        response_delete_owned = self.client.delete('/game-ownership/3/')

        # Assert
        self.assertEqual(response_delete_others.status_code,
            status.HTTP_404_NOT_FOUND) # Can not delete others
        self.assertEqual(response_delete_owned.status_code,
            status.HTTP_204_NO_CONTENT)

        response_check_owned = self.client.get('/game-ownership/3/') # Deleted
        self.assertEqual(response_check_owned.status_code,
            status.HTTP_404_NOT_FOUND)