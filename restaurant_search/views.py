from rest_framework.response import Response
from rest_framework.views import APIView
import requests


class GetClosestRestaurants(APIView):
    def get(self, request, country, city):
        url = f"https://api.foursquare.com/v3/places/search?query=coffee&near={country}%2C%20{city}"
        headers = {
            "accept": "application/json",
            "Authorization": "fsq3+c+Y2TIAq3ICleVq6WIcVDJccQFuadeNFvnSTt+xnDc="
        }
        response = requests.get(url, headers=headers)
        response_json = response.json()
        return Response(response_json)
