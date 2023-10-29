from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from config.helpers.rename import PathAndRename


class User(AbstractUser):
    avatar = models.ImageField(upload_to=PathAndRename("profile_images/"))
    email = models.EmailField(unique=True, db_index=True)

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
