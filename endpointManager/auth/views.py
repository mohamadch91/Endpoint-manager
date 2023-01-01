import json
from os import stat
import os
from urllib import response
from django.shortcuts import render
from django.contrib.auth.hashers import make_password

# Create your views here.
from .serializers import ChangePasswordSerializer,UpdateUserSerializer,UserSerializer
from rest_framework.permissions import AllowAny

from authen.models import User
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
import copy
from facilities.models import Facility

class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer   

class ChangePasswordView(generics.UpdateAPIView):
    
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer  
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"Password changed succesfully"}, status=status.HTTP_200_OK) 

class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer     
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)    
class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)            
class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        new_data=copy.deepcopy(serializer.data)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
class Userdata(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        id=request.query_params.get('id',None)
        req_user=request.user
        if(id):
            
            user = User.objects.filter(facilityid=id)
            if(req_user.id !=1):
                user=user.filter(id__gt=1)
            serializer = UserSerializer(user,many=True)
            new_data=copy.deepcopy(serializer.data)
            new_data=sorted(new_data,key=lambda x:x['pk'])
            return Response(data=new_data,status=status.HTTP_200_OK)
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        new_data=copy.deepcopy(serializer.data)
        new_data=sorted(new_data,key=lambda x:x['pk'])

        return Response(data=new_data,status=status.HTTP_200_OK)
   
class UrlCheckView(APIView):
    def get(self,request):
        return Response({"message":"ok"},status=status.HTTP_200_OK)

class userdb(APIView):
    def get(self,request):
        f=open("./authen/Results.json","r")
        data=json.load(f)
        for i in data:
            copys=i.copy()
            del copys['ID']
            copys['is_active']=copys['enable']
            del copys['enable']
            del copys['idnumber']
            del copys['creatondate']
            del copys['lastLogin']
            del copys['facilityid']
            user=User.objects.filter(id=i['createby'])[0]
            copys['owner']=user.name
            facility=Facility.objects.filter(name__icontains=i['faciltyName'].strip())
            if(len(facility)==0):
                continue
            facility=facility[0]
            copys['facilityid']=facility.id
            ser=RegisterSerializer(data=copys)
            if ser.is_valid():
                ser.save()
        return Response({"message":"ok"},status=status.HTTP_200_OK)

