import json
from os import stat
import os
from urllib import response
from django.shortcuts import render
from django.contrib.auth.hashers import make_password

# Create your views here.
from .serializers import ChangePasswordSerializer,UpdateUserSerializer
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer   
