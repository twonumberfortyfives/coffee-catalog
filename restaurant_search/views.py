import aiohttp
import asyncio
import time
import os
from rest_framework.decorators import permission_classes
from adrf.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from asgiref.sync import sync_to_async  # Import sync_to_async
from .models import Restaurant, Image, Comment
from .serializers import RestaurantListSerializer, ImageSerializer, CommentListSerializer
from .permissions import IsAuthorizedAndVerifiedOrNot
from rest_framework.permissions import IsAuthenticated


async def fetch_images(session, fsq_id):
    try:
        base_url = f"https://api.foursquare.com/v3/places/{fsq_id}/photos"
        async with session.get(base_url) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        print(f"Image request failed for fsq_id {fsq_id}: {e}")
        return None


async def fetch_restaurants(session, country, city):
    try:
        base_url = f"https://api.foursquare.com/v3/places/search?query=coffee&near={country}%2C%20{city}&limit=50"
        async with session.get(base_url) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        print(f"Restaurant request failed: {e}")
        return None


@api_view(["GET"])
@permission_classes([IsAuthorizedAndVerifiedOrNot])
async def get_all_restaurants_in_the_city(request, country, city, coffee_id: int = None) -> Response:
    start_time = time.time()
    headers = {
        "accept": "application/json",
        "Authorization": os.environ.get("PLACES_API"),
    }
    restaurant_to_serialize = []

    async with aiohttp.ClientSession(headers=headers) as session:
        # Fetch restaurant data
        response_json = await fetch_restaurants(session, country, city)
        if response_json is None:
            return Response({"error": "Failed to fetch restaurant data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Collect fsq_ids
        fsq_ids = [item["fsq_id"] for item in response_json.get("results", [])]

        # Fetch all images concurrently
        image_tasks = [fetch_images(session, fsq_id) for fsq_id in fsq_ids]
        images_responses = await asyncio.gather(*image_tasks)

        for index, item in enumerate(response_json["results"]):
            images_json = images_responses[index]
            if images_json is None:
                continue

            # Use sync_to_async for ORM operations
            restaurant, created = await sync_to_async(Restaurant.objects.update_or_create)(
                unique_id=item["fsq_id"],
                defaults={
                    "name": item["name"],
                    "address": item.get("location", {}).get("formatted_address"),
                    "opening_hours": item.get("closed_bucket"),
                }
            )

            # Clear images for the restaurant asynchronously
            await sync_to_async(restaurant.images.clear)()

            for image_data in images_json:
                image_url = image_data.get("prefix") + "original" + image_data.get("suffix")
                image_instance, _ = await sync_to_async(Image.objects.get_or_create)(
                    url=image_url
                )
                ImageSerializer(instance=image_instance)
                # Add image to restaurant's images
                await sync_to_async(restaurant.images.add)(image_instance)

            restaurant_to_serialize.append(restaurant)

    # Serialize the list of restaurants outside the async context
    serialized_data = await sync_to_async(lambda: RestaurantListSerializer(restaurant_to_serialize, many=True).data)()

    # Retrieving the exact restaurant

    if coffee_id:
        restaurant_to_retrieve = [item for item in serialized_data if item.get("id") == coffee_id]
        return Response(restaurant_to_retrieve, status.HTTP_200_OK)

    total_time = time.time() - start_time
    print(f"Total time: {total_time} seconds")
    return Response(serialized_data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user).select_related("restaurant", "user")
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
