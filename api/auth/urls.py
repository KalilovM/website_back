from api.auth.views import ObtainTokenView
from django.urls import path

urlpatterns = [path("token/", ObtainTokenView.as_view(), name="obtain-token")]
