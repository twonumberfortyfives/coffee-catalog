from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurant_search.views import get_nearby_places, retrieve_the_place

app_name = "main"

router = DefaultRouter()

urlpatterns = [
    path("get-restaurants/<str:location>/", get_nearby_places, name="get-restaurants"),
    path("retrieve-restaurant/<int:pk>/", retrieve_the_place, name="restaurant-retrieve"),
    path("", include(router.urls)),
]
