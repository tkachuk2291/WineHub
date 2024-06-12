from django.contrib.auth.models import AbstractUser
from django.db import models
from wine_vault.models import Wine


class WineUser(AbstractUser):
    pass


class UserFavoriteBottle(models.Model):
    user = models.ForeignKey(WineUser, on_delete=models.CASCADE, related_name='favorite_bottles_user')
    wine = models.ForeignKey(Wine, on_delete=models.CASCADE, related_name='favorite_bottles_wine')

    class Meta:
        unique_together = ('user', 'wine')

    def __str__(self):
        return f'{self.user.username} - {self.wine.name}'
