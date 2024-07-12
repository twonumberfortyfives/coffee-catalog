from django.urls import path
from restaurant_search.views import (
    get_nearby_places,
    retrieve_the_place,
    get_top_restaurants,
)

app_name = "main"


urlpatterns = [
    path("get-restaurants/<str:location>/", get_nearby_places, name="get-restaurants"),
    path(
        "retrieve-restaurant/<int:pk>/", retrieve_the_place, name="restaurant-retrieve"
    ),
    path("get-top-restaurants/", get_top_restaurants, name="get-top-restaurants"),
]
