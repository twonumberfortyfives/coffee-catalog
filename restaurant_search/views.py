import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
import httpx
from .models import Restaurant
from .serializers import RestaurantListSerializer
from restaurant_search.permissions import IsAuthorizedAndVerifiedOrNot
from dotenv import load_dotenv

load_dotenv()

@api_view(["GET"])
@permission_classes([IsAuthorizedAndVerifiedOrNot])
def get_all_restaurants_in_the_city(
    request, country, city, coffee_id: int = None
) -> Response:
    url = f"https://api.foursquare.com/v3/places/search?query=coffee&near={country}%2C%20{city}"
    headers = {
        "accept": "application/json",
        "Authorization": os.environ.get("PLACES_API"),
    }

    try:
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
    except httpx.RequestError as e:
        return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

    response_json = response.json()
    results = response_json.get("results", [])

    exists_restaurants = []

    for item in results:
        unique_id = item.get("fsq_id")
        name = item.get("name")
        address = item.get("location", {}).get("formatted_address")

        # Fetching images
        images_url = f"https://api.foursquare.com/v3/places/{unique_id}/photos"
        images_response = httpx.get(images_url, headers=headers)
        images_json = images_response.json()
        list_of_images = [
            f"{image.get('prefix')}original{image.get('suffix')}" for image in images_json
        ]

        if not unique_id or not name or not address:
            continue

        # Use get_or_create to handle existing and new restaurants
        restaurant, created = Restaurant.objects.get_or_create(
            unique_id=unique_id,
            defaults={
                "name": name,
                "address": address,
                "images": list_of_images,
            },
        )
        exists_restaurants.append(restaurant)

    serializer = RestaurantListSerializer(exists_restaurants, many=True)

    if coffee_id is not None:
        retrieve_restaurant = [
            item for item in serializer.data if item.get("id") == coffee_id
        ]
        return Response(retrieve_restaurant, status=status.HTTP_200_OK)

    return Response(serializer.data, status=status.HTTP_200_OK)
