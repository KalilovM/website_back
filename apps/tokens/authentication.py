from rest_framework import authentication, exceptions
from utils import jwt


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            return None

        payload = jwt.decode_jwt_token(token)

        if payload is None:
            raise exceptions.AuthenticationFailed("Invalid token")

        user_id = payload.get("user_id")
        user = self.get_user(user_id)

        return (user, None)

    def get_user(self, user_id):
        from tokens.models import User

        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None
