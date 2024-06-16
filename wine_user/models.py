from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

from wine_user.validators import validate_first_name, validate_last_name, validate_age, email_validate
from wine_vault.models import Wine


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class WineUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, validators=[email_validate])
    first_name = models.CharField(max_length=30, validators=[validate_first_name])
    last_name = models.CharField(max_length=30, validators=[validate_last_name])
    age = models.IntegerField(max_length=2, validators=[validate_age], null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserFavoriteBottle(models.Model):
    user = models.ForeignKey(WineUser, on_delete=models.CASCADE, related_name='favorite_bottles_user')
    wine = models.ForeignKey(Wine, on_delete=models.CASCADE, related_name='favorite_bottles_wine')

    class Meta:
        unique_together = ('user', 'wine')

    def __str__(self):
        return f'{self.user.username} - {self.wine.name}'
