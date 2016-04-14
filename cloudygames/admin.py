from django.contrib import admin

from . import models

# Register models here.
admin.site.register([models.Game, models.GameSession,
    models.GameOwnership, models.PlayerSaveData])
