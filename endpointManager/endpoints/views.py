
# Create your views here.
from .serializers import UrlSerializer
from rest_framework.permissions import AllowAny

from .models import Url
from auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class UrlCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UrlSerializer   
    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            user=User.objects.get(id=request.user.id)
            user.url_count+=1
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

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
        response={
            'success_count':url.success_count,
            'fail_count':url.fail_count,
            'fail_limit':url.fail_limit,
            'total_count':url.success_count+url.fail_count
        }
        return Response(response,status=status.HTTP_200_OK)