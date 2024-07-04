from django.urls import path, include
from rest_framework.routers import DefaultRouter

from restaurant_search.views import get_all_restaurants_in_the_city, CommentViewSet

app_name = "main"

router = DefaultRouter()
router.register('comments', CommentViewSet)

urlpatterns = [
    path("restaurants/<str:country>/<str:city>/", get_all_restaurants_in_the_city, name='closest-restaurants'),
    path("restaurants/<str:country>/<str:city>/<int:coffee_id>/", get_all_restaurants_in_the_city, name="closest-restaurant-detail"),
    path("", include(router.urls)),
]
