from django.urls import path

from restaurant_search.views import get_all_restaurants_in_the_city

app_name = "main"
urlpatterns = [
    path("restaurants/<str:country>/<str:city>/", get_all_restaurants_in_the_city, name='closest-restaurants'),
    path("restaurants/<str:country>/<str:city>/<int:coffee_id>/", get_all_restaurants_in_the_city, name="closest-restaurant-detail"),
]
