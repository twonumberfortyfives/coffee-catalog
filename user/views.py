import jwt
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics, status, response, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import UserSerializer, EmailVerificationSerializer
from user.utils import Util


class LoginUserView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class SignUp(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.data

        # getting tokens
        user_email = get_user_model().objects.get(email=user["email"])
        tokens = RefreshToken.for_user(user_email).access_token
        # send email for user verification
        current_site = get_current_site(request).domain
        relative_link = reverse("user:email-verify")
        absurl = "http://" + current_site + relative_link + "?token=" + str(tokens)
        email_body = (
            "Hi "
            + user["email"]
            + " Use the link below to verify your email \n"
            + absurl
        )
        data = {
            "email_body": email_body,
            "to_email": user["email"],
            "email_subject": "Verify your email",
        }

        Util.send_email(data=data)

        return response.Response(
            {"user_data": user, "access_token": str(tokens)},
            status=status.HTTP_201_CREATED,
        )


class VerifyEmail(GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get("token")
        try:
            print(token)
            payload = jwt.decode(token, options={"verify_signature": False})
            print(payload)
            user = get_user_model().objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return response.Response(
                {"email": "Successfully activated"}, status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError as identifier:
            return response.Response(
                {"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as identifier:
            print(identifier)
            return response.Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )
