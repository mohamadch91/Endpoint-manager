from .serializers import GetWarningSerializer, WarningSerializer
from rest_framework.permissions import AllowAny

from .models import Warning
from authen.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import copy
class GetWarningView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetWarningSerializer
    def get_queryset(self):
        warnings=Warning.objects.filter(url=self.request.url)
        serializers=WarningSerializer(warnings,many=True)
        serializers_copy=copy.deepcopy(serializers.data)
        for i in serializers_copy:
            del i['url']
        return Response(serializers_copy,status=status.HTTP_200_OK)
        