from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import ManageUserView, VerifyEmail, SignUp, FavouriteViewSet, CreateReview

app_name = "user"

router = DefaultRouter()
router.register("my-favourites", FavouriteViewSet, basename="favourites")

urlpatterns = [
    path("me/", ManageUserView.as_view(), name="my_info"),
    path("register/", SignUp.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("email-verify/", VerifyEmail.as_view(), name="email-verify"),
    path("create-review/", CreateReview.as_view(), name="create-review"),
    path("", include(router.urls)),
]
