from django.urls import path

from restaurant_search.views import GetClosestRestaurants

app_name = "main"
urlpatterns = [
    path('restaurants/<str:country>/<str:city>/', GetClosestRestaurants.as_view(), name='closest-restaurants'),
]
