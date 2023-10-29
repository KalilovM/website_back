from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpRequest
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User
from .services import create_user, get_user
from .utils import generate_avatar
from .validators import LoginValidator, RegisterValidator


class RegisterSerializer(serializers.Serializer):
    avatar = serializers.SerializerMethodField()
    username = serializers.CharField(max_length=60)
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj: User):
        user: User = get_user(username=obj.username)
        return {"refresh": user.tokens()["refresh"], "access": user.tokens()["access"]}

    def get_avatar(self, obj: User):
        request: "HttpRequest" = self.context.get("request")
        try:
            avatar = generate_avatar(obj.username, sub_path="profile_images/defaults/", request=request)
            obj.avatar = avatar
            obj.save()
            return request.build_absolute_uri(obj.avatar.url)
        except FileNotFoundError:
            raise serializers.ValidationError("Error while generating avatar")

    def validate(self, attrs):
        validator = RegisterValidator(attrs)
        return validator.validate()

    def create(self, validated_data):
        return create_user(validated_data)


class LoginSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(max_length=50, min_length=3)
    tokens = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        user: "User" = get_user(username=obj["username"])
        request: "HttpRequest" = self.context.get("request")
        return request.build_absolute_uri(user.avatar.url)

    def get_tokens(self, obj):
        user: "User" = get_user(username=obj["username"])
        return {"refresh": user.tokens()["refresh"], "access": user.tokens()["access"]}

    class Meta:
        model = User
        fields = ["password", "username", "tokens", "avatar"]

    def validate(self, attrs):
        validator = LoginValidator(attrs)
        return validator.validate()


class LogoutSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def create(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")
