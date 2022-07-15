from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractUser):
    """
    Model extends auth.user and stores more information like home-town, phone etc

    """
    username_validator = UnicodeUsernameValidator()

    username = models.EmailField(unique=True, validators=[username_validator])
    home_town = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    profile_description = models.TextField(null=True, blank=True)

    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.first_name == '':
            return self.username
        else:
            return u'%s %s' % (self.first_name, self.last_name)

