import tempfile

from django.core.urlresolvers import reverse

from rest_framework import test as drf_test
from rest_framework import status

from .. import models


class SaveGameAPITest(drf_test.APITestCase):
    def setUp(self):

        # Setup initial Database
        self.operator = models.User.objects.create_superuser(
                username='operator1', email='op1@test.net', password='pass')
        self.player = models.User.objects.create_user(username='user1')
        self.game = models.Game.objects.create(name='game1', publisher='pub1',
                max_limit=1, address='addr1')
        models.GameOwnership.objects.create(user=self.player, game=self.game)
        self.game_session = models.GameSession.objects.create(user=self.player,
                game=self.game, controller=1, streaming_port=30001)
        
        # Setup Mock File for Uploading
        self.mockfile = tempfile.NamedTemporaryFile()
        self.mockfile.write(b'0123456789')
        self.mockfile.seek(0)

        # Setup Resource Endpoint
        self.url = reverse('playersavedata-list')

    def tearDown(self):
        self.mockfile.close()

    def test_player_upload_save_data_forbidden(self):
        # Arrange
        self.client.force_authenticate(self.player)
        data = {
            'saved_file': self.mockfile,
            'is_autosaved': True,
            'user': self.player,
            'game': self.game_session.game.name,
        }

        # Act
        response = self.client.post(self.url, data, format='multipart')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_operator_upload_save_data_success(self):
        # Arrange
        self.client.force_authenticate(self.operator)
        data = {
            'saved_file': self.mockfile,
            'is_autosaved': True,
            'user': self.player.username,
            'game': self.game_session.game.id,
        }

        # Act
        response = self.client.post(self.url, data, format='multipart')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_overwrite_save_data_success(self):

        # Arrange
        models.PlayerSaveData.objects.create(user=self.player, game=self.game,
                is_autosaved=True)
        self.client.force_authenticate(self.operator)
        data = {
            'saved_file': self.mockfile,
            'is_autosaved': True,
            'user': self.player.username,
            'game': self.game_session.game.id,
        }

        # Act
        response = self.client.post(self.url, data, format='multipart')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.PlayerSaveData.objects.count(), 1)
