
# Create your views here.
from .serializers import EndpointSerializer,RequestSerializer,EndpointRegisterSerializer

from .models import Endpoint,Request
from authen.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import datetime
import copy
class EndpointCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EndpointSerializer   
    def post(self, request):
        user=get_object_or_404(User,pk=request.user.id)
        user_Endpoint=user.endpoint_count
        if user_Endpoint<20:
            request_data={
                "user":user.id,
                "address":request.data['address'],
                "fail_limit":request.data['fail_limit']
            }
            serializer = EndpointRegisterSerializer(data=request_data)
            if serializer.is_valid():
                user.endpoint_count+=1
                user.save()
                serializer.save()
                response_data=copy.deepcopy(serializer.data)
                del response_data['user']
                response = {
                    "message":"Endpoint created successfully",
                    "data":response_data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"You have reached the limit of 20 endpoints"}, status=status.HTTP_400_BAD_REQUEST)

        
        

class UserEndpointView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EndpointSerializer
    def get_queryset(self):
        return Endpoint.objects.filter(user=self.request.user)

class EndpointStatsView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EndpointSerializer
    queryset=Endpoint.objects.all()
    def get(self, request, *args, **kwargs):
        id=kwargs['pk']
        print(id)
        endpoint=get_object_or_404(Endpoint,id=id)
        if (endpoint.user==self.request.user):
            yesterday=datetime.datetime.now()-datetime.timedelta(days=1)
            requests=Request.objects.filter(endpoint=endpoint,created_at__gte=yesterday)
            if (requests.count()>0):
                response=[]
                for request in requests:
                    status_code=request.status_code
                    status_type="success" if status_code>=200 and status_code<300 else "fail"
                    endpoint=request.endpoint.address
                    response.append({"status":status_type,"endpoint":endpoint,"status_code":status_code,"created_at":request.created_at})
                return Response(response, status=status.HTTP_200_OK)
            else:
                response={"message":"No requests found  for this endpoint"}
                return Response(response, status=status.HTTP_204_NO_CONTENT)
            
        else:
            response={"message":"You are not authorized to view this endpoint"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
class CallEndpointView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        endpoint=get_object_or_404(Endpoint,address=self.kwargs['endpoint'])
        endpoint.success_count+=1
        endpoint.save()
        
        data={
            "endpoint":endpoint.id,
            "status_code":200
        }
        serializer=RequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response("Success", status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        endpoint=get_object_or_404(Endpoint,address=self.kwargs['endpoint'])
        endpoint.fail_count+=1
        endpoint.save()
        data={
            "endpoint":endpoint.id,
            "status_code":400
        }
        serializer=RequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response("Fail", status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, *args, **kwargs):
        endpoint=get_object_or_404(Endpoint,address=self.kwargs['endpoint'])
        endpoint.fail_count+=1
        endpoint.save()
        data={
            "endpoint":endpoint.id,
            "status_code":403
        }
        serializer=RequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response("Fail", status=status.HTTP_403_FORBIDDEN)
    def delete(self, request, *args, **kwargs):
        endpoint=get_object_or_404(Endpoint,address=self.kwargs['endpoint'])
        endpoint.fail_count+=1
        endpoint.save()
        data={
            "endpoint":endpoint.id,
            "status_code":406
        }
        serializer=RequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response("Fail", status=status.HTTP_406_NOT_ACCEPTABLE)        
    def patch(self, request, *args, **kwargs):
        endpoint=get_object_or_404(Endpoint,address=self.kwargs['endpoint'])
        endpoint.fail_count+=1
        endpoint.save()
        data={
            "endpoint":endpoint.id,
            "status_code":503
        }
        serializer=RequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response("Fail", status=status.HTTP_503_SERVICE_UNAVAILABLE)       
    def options(self, request, *args, **kwargs):
        endpoint=get_object_or_404(Endpoint,address=self.kwargs['endpoint'])
        endpoint.success_count+=1
        endpoint.save()
        data={
            "endpoint":endpoint.id,
            "status_code":202
        }
        serializer=RequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(["GET","OPTIONS"], status=status.HTTP_202_ACCEPTED)       
         
        
class EndpointWarningView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Endpoint.objects.all()
    def get (self, request, *args, **kwargs):
        id=self.kwargs['pk']
        endpoint=get_object_or_404(Endpoint,id=id)
        if(endpoint.user == request.user):
            if (endpoint.fail_count>endpoint.fail_limit):
                requests=Request.objects.filter(endpoint=endpoint,status_code__gte=300)
                diffrence=endpoint.fail_count-endpoint.fail_limit
                response=[]
                length=requests.count()
                for i in range(diffrence):
                    serializer=RequestSerializer(requests[length-i-1])
                    serilizer_data=copy.deepcopy(serializer.data)
                    del serilizer_data['id']
                    del serilizer_data['endpoint']
                    serilizer_data['endpoint']=endpoint.address
                    serilizer_data['status']="Fail"
                    response_data={
                        "message":"Endpoint Fail Limit Exceeded",
                        "data":serilizer_data
                        
                    }
                    response.append(response_data)
                return Response(response, status=status.HTTP_200_OK)
                
            else:
                response={"message":"Endpoint is working properly"}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response={"message":"You are not authorized to view this endpoint"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        
        

            
