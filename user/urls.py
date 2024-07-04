from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import ManageUserView, VerifyEmail, SignUp, FavoriteListView, FavouriteRetrieveView

app_name = "user"

urlpatterns = [
    path("me/", ManageUserView.as_view(), name="my_info"),
    path("register/", SignUp.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("email-verify/", VerifyEmail.as_view(), name="email-verify"),
    path("my-favourites/", FavoriteListView.as_view(), name="my_favourites"),
    path("my-favourites/<int:pk>/", FavouriteRetrieveView.as_view(), name="my_favourite_retrieve"),
]
