from rest_framework import serializers
from apps.users.models import User


class LoginSeriazlier(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ("username", "password")
