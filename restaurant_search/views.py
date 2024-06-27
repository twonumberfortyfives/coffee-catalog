from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from restaurant_search.permissions import IsAuthorizedAndVerifiedOrNot
from restaurant_search.models import Restaurant


@permission_classes(["IsAuthorizedAndVerifiedOrNot"])
@api_view(["GET"])
def get_all_restaurants_in_the_city(request, country, city, coffee_id: int = None) -> Response:
    url = f"https://api.foursquare.com/v3/places/search?query=coffee&near={country}%2C%20{city}"
    headers = {
        "accept": "application/json",
        "Authorization": "fsq3+c+Y2TIAq3ICleVq6WIcVDJccQFuadeNFvnSTt+xnDc="
    }
    response = requests.get(url, headers=headers)
    print(response.text)
    response_json = response.json()
    result = [response for response in response_json["results"]]
    restaurants = [Restaurant.objects.create(name=response["name"], address=response["location"]["formatted_address"], image=response["link"]) for response in result]

    if coffee_id:
        return Response(result[coffee_id])
    return Response(result)
