from django.contrib.auth import get_user_model
from rest_framework import status, permissions, views
from rest_framework.response import Response

from api.auth.auth import JWTAuthentication
from apps.tokens.serializers import ObtainTokenSerializer


User = get_user_model()


class ObtainTokenView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ObtainTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

        jwt_token = JWTAuthentication.create_jwt(user)
        return Response({"token": jwt_token})
