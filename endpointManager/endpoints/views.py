
# Create your views here.
from .serializers import UrlSerializer
from rest_framework.permissions import AllowAny

from .models import Url
from auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

class UrlCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UrlSerializer   
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"Url created succesfully"}, status=status.HTTP_201_CREATED)

class UserUrlView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UrlSerializer
    def get_queryset(self):
        return Url.objects.filter(user=self.request.user)

class UrlStatsView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UrlSerializer
    def get_queryset(self):
        return Url.objects.filter(user=self.request.user)