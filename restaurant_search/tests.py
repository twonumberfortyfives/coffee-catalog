
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from restaurant_search.models import Restaurant


GET_RESTAURANTS = "/api/main/get-restaurants/Kiev/"
RETRIEVE_RESTAURANT = "/api/main/retrieve-restaurant/1/"
TOP_RESTAURANTS = "/api/main/get-top-restaurants/"


class RestaurantSearchUnauthorizedTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_user_can_access_the_service(self):
        response = self.client.get(GET_RESTAURANTS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RestaurantSearchDataTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_database_data_sync(self):
        response = self.client.get(GET_RESTAURANTS)
        all_restaurants_db = Restaurant.objects.all()
        self.assertEqual(len(response.data), all_restaurants_db.count())

    def test_retrieve_restaurant(self):
        fetch_data = self.client.get(GET_RESTAURANTS)
        first_restaurant = fetch_data.data[0]
        response = self.client.get(RETRIEVE_RESTAURANT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(first_restaurant["id"], response.data["id"])

    def test_get_top_restaurants(self):
        fetch_data = self.client.get(GET_RESTAURANTS)
        response = self.client.get(TOP_RESTAURANTS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(fetch_data.data))