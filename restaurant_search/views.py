import os
import time
from concurrent.futures import ThreadPoolExecutor

import httpx
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response

from restaurant_search.models import Image, Restaurant
from restaurant_search.permissions import IsAuthorizedAndVerifiedOrNot
from restaurant_search.serializers import RestaurantListSerializer, ImageSerializer


def fetch_photo(images_url, headers):
    try:
        response = httpx.get(images_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        print(f"Error fetching photo from {images_url}: {str(e)}")
        return []


@api_view(["GET"])
@permission_classes([IsAuthorizedAndVerifiedOrNot])
def get_all_restaurants_in_the_city(request, country, city, coffee_id: int = None) -> Response:
    start_time = time.time()
    url = f"https://api.foursquare.com/v3/places/search?query=coffee&near={country}%2C%20{city}&limit=50"
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
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {
            executor.submit(fetch_photo, f"https://api.foursquare.com/v3/places/{item.get('fsq_id')}/photos", headers): item
            for item in results
            if item.get("fsq_id") and item.get("name") and item.get("location", {}).get("formatted_address")
        }
        for future in future_to_url:
            item = future_to_url[future]
            try:
                images_json = future.result()
                image_urls = [
                    f"{image.get('prefix')}original{image.get('suffix')}" for image in images_json
                ]

                restaurant, created = Restaurant.objects.get_or_create(
                    unique_id=item.get("fsq_id"),
                    defaults={
                        "name": item.get("name"),
                        "address": item.get("location", {}).get("formatted_address"),
                    },
                )

                restaurant.images.clear()
                for url in image_urls:
                    image, _ = Image.objects.get_or_create(url=url)
                    serializer = ImageSerializer(image)
                    restaurant.images.add(image)

                exists_restaurants.append(restaurant)
            except Exception as e:
                print(f"Error processing restaurant {item.get('name')}: {str(e)}")

    serializer = RestaurantListSerializer(exists_restaurants, many=True)

    if coffee_id is not None:
        retrieve_restaurant = [
            item for item in serializer.data if item.get("id") == coffee_id
        ]
        return Response(retrieve_restaurant, status=status.HTTP_200_OK)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time}")
    return Response(serializer.data, status=status.HTTP_200_OK)
