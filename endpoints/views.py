
# Create your views here.
from .serializers import UrlSerializer,RequestSerializer

from .models import Url,Request
from authen.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import datetime

class UrlCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UrlSerializer   
    def post(self, request):
        user=get_object_or_404(User,pk=request.user.id)
        user_url=user.url_count
        if user_url<20:
            data=request.data
            data['user']=user.id
            serializer = UrlSerializer(data=data)
            if serializer.is_valid():
                user.url_count+=1
                user.save()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"You have reached the limit of 20 urls"}, status=status.HTTP_400_BAD_REQUEST)

        
        

class UserUrlView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UrlSerializer
    def get_queryset(self):
        return Url.objects.filter(user=self.request.user)

class UrlStatsView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UrlSerializer
    def get_queryset(self):
        url=get_object_or_404(Url,pk=self.kwargs['pk'])
        if (url.user==self.request.user):
            yesterday=datetime.datetime.now()-datetime.timedelta(days=1)
            requests=Request.objects.filter(url=url,created_at__gte=yesterday)
            if (requests.count()>0):
                response=[]
                for request in requests:
                    status_code=request.status_code
                    status="success" if status_code>=200 and status<300 else "fail"
                    url=request.url.address
                    response.append({"status":status,"url":url,"status_code":status_code,"created_at":request.created_at})
                return Response(response, status=status.HTTP_200_OK)
            else:
                response={"message":"No requests found  for this url"}
                return Response(response, status=status.HTTP_204_NO_CONTENT)
            
        else:
            response={"message":"You are not authorized to view this url"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
class CallUrlView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        url=get_object_or_404(Url,pk=self.kwargs['pk'])
        pass
        