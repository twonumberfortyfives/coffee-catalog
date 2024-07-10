import time

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests
import os
from geopy.geocoders import Nominatim
from .models import Restaurant, Review, Image
from dotenv import load_dotenv

from .serializers import RestaurantListSerializer, RestaurantDetailSerializer

load_dotenv()

api_key = os.getenv("PLACES_API")

url = "https://places.googleapis.com/v1/places:searchNearby"
headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": api_key,
    "X-Goog-FieldMask": (
        "places.displayName,"
        "places.formattedAddress,"
        "places.googleMapsUri,"
        "places.id,"
        "places.location,"
        "places.photos,"
        "places.currentOpeningHours,"
        "places.internationalPhoneNumber,"
        "places.priceLevel,"
        "places.rating,"
        "places.userRatingCount,"
        "places.websiteUri,"
        "places.delivery,"
        "places.reviews"
    ),
}


def get_coordinates(location: str):
    geolocator = Nominatim(user_agent="Python-requests/2.26.0")
    location = geolocator.geocode(location)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None


def get_photos(photo_name: str) -> str:
    if not api_key:
        raise ValueError("API_KEY not set in environment variables")
    url = f"https://places.googleapis.com/v1/{photo_name}/media?key={api_key}&maxHeightPx=4800&maxWidthPx=4800"
    return url


@api_view(["GET"])
def get_nearby_places(request, location: str) -> Response:
    start = time.time()

    if not api_key:
        return Response(
            {"error": "API key is missing"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    latitude, longitude = get_coordinates(location)
    if latitude is None or longitude is None:
        return Response(
            {"error": "Invalid location provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    data = {
        "includedTypes": ["cafe"],
        "maxResultCount": 20,
        "locationRestriction": {
            "circle": {
                "center": {"latitude": latitude, "longitude": longitude},
                "radius": 5000.0,
            }
        },
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response.encoding = "utf-8"
        response_json = response.json()

        array_of_restaurants_to_serialize = []

        for place in response_json.get("places", []):
            try:
                unique_id = place.get("id", None)
                phone_number = place.get("internationalPhoneNumber", None)
                address = place.get("formattedAddress", None)
                location_data = place.get("location", {})
                latitude = location_data.get("latitude", None)
                longitude = location_data.get("longitude", None)
                rating = place.get("rating", None)
                google_url = place.get("googleMapsUri", None)
                website_url = place.get("websiteUri", None)
                total_users_ratings = place.get("userRatingCount", None)
                name = place.get("displayName", None).get("text", None)
                open_now = place.get("currentOpeningHours", {}).get("openNow", None)
                opening_hours_weekdays = place.get("currentOpeningHours", {}).get(
                    "weekdayDescriptions", None
                )
                restaurant, created = Restaurant.objects.update_or_create(
                    unique_id=unique_id,
                    defaults={
                        "phone_number": phone_number,
                        "address": address,
                        "latitude": latitude,
                        "longitude": longitude,
                        "rating": rating,
                        "google_url": google_url,
                        "website_url": website_url,
                        "total_users_ratings": total_users_ratings,
                        "name": name,
                        "open_now": open_now,
                        "opening_hours_weekdays": opening_hours_weekdays,
                    },
                )

                photos = place.get("photos", [])
                if photos:
                    main_photo_url = get_photos(photos[0]["name"])
                    restaurant.main_photo = main_photo_url
                    restaurant.save()

                array_of_restaurants_to_serialize.append(restaurant)
            except KeyError as key_err:
                print(
                    f"KeyError: {key_err}. Missing key in place data. Continuing to next place."
                )
                continue
        restaurants_serializer = RestaurantListSerializer(
            array_of_restaurants_to_serialize, many=True
        )
        end = time.time()
        print(f"{end - start} seconds")
        return Response(restaurants_serializer.data, status=status.HTTP_200_OK)

    except Exception as err:
        print(f"An error occurred: {err}")
        return Response(
            {"error": "An unknown error occurred", "details": str(err)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def retrieve_the_place(request, pk: int) -> Response:
    start = time.time()

    restaurant = Restaurant.objects.get(pk=pk)

    headers_to_retrieve = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "*",
    }

    url = f"https://places.googleapis.com/v1/places/{restaurant.unique_id}"

    response = requests.get(url, headers=headers_to_retrieve)
    response.raise_for_status()
    response.encoding = "utf-8"

    response_json = response.json()

    array_of_images = []

    for review in response_json.get("reviews", []):
        try:
            unique_name = review.get("name", None)
            author_name = review.get("authorAttribution", {}).get("displayName", None)
            text = review.get("text", None).get("text", None)
            created_at = review.get("relativePublishTimeDescription", None)
            rating = review.get("rating", None)
            profile_picture = review.get("authorAttribution", {}).get("photoUri", None)

            Review.objects.update_or_create(
                unique_name=unique_name,
                defaults={
                    "restaurant": restaurant,
                    "author_name": author_name,
                    "text": text,
                    "created_at": created_at,
                    "rating": rating,
                    "profile_picture": profile_picture,
                },
            )
        except Exception as err:
            print(f"An error occurred: {err}")
            continue

    for photo in response_json.get("photos", []):
        if photo:
            try:
                url = get_photos(photo["name"])
                contrib_url = photo.get("authorAttributions", [{}])[0].get("uri", None)
                image = Image.objects.update_or_create(
                    contrib_url=contrib_url,
                    defaults={"restaurant": restaurant, "url": url},
                )
                array_of_images.append(image)
            except Exception as e:
                print(f"Error processing photo: {e}")

    serializer = RestaurantDetailSerializer(restaurant)
    end = time.time()
    print(f"{end - start} seconds")
    return Response(serializer.data, status=status.HTTP_200_OK)
