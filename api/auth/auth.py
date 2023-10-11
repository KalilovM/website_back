from datetime import timedelta, datetime

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError


User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    @classmethod
    def get_token_from_header(cls, token: str):
        token = token.replace("Bearer", "").replace(" ", "")
        return token

    def authenticate(self, request):
        jwt_token = request.META.get("HTTP_AUTHORIZATION")
        if jwt_token is None:
            return None

        jwt_token = JWTAuthentication.get_token_from_header(jwt_token)

        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed("Invalid signature")
        except:
            raise ParseError()

        username = payload.get("username")
        if username is None:
            raise AuthenticationFailed("User identifier not found in JWT")

        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed("User not found")

        return user, payload

    def authenticate_header(self, request):
        return "Bearer"

    @classmethod
    def create_jwt(cls, user):
        payload = {
            "username": user.username,
            "exp": int(
                (
                    datetime.now()
                    + timedelta(hours=settings.JWT_CONF["TOKEN_LIFETIME_HOURS"])
                ).timestamp()
            ),
            "iat": datetime.now().timestamp(),
        }
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return jwt_token
