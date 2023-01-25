
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
    #Check for user authentication
    permission_classes = (IsAuthenticated,)
    serializer_class = EndpointSerializer   
    def post(self, request: Request, *args, **kwargs)-> Response:
        #get user from request
        user=get_object_or_404(User,pk=request.user.id)
        user_Endpoint=user.endpoint_count
        #check if user has reached the limit of 20 endpoints
        if user_Endpoint<20:
            request_data={
                "user":user.id,
                "address":request.data['address'],
                "fail_limit":request.data['fail_limit']
            }
            #create endpoint
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
    #Check for user authentication
    permission_classes = (IsAuthenticated,)
    serializer_class = EndpointSerializer
    def get_queryset(self)-> Response:
        #all endpoints of the user
        return Endpoint.objects.filter(user=self.request.user)

class EndpointStatsView(generics.RetrieveAPIView):
    #Check for user authentication
    permission_classes = (IsAuthenticated,)
    serializer_class = EndpointSerializer
    queryset=Endpoint.objects.all()
    def get(self, request, *args, **kwargs)-> Response:
        #get endpoint id from url
        id=kwargs['pk']
        #get endpoint
        endpoint=get_object_or_404(Endpoint,id=id)
        #check if the user is the owner of the endpoint
        if (endpoint.user==self.request.user):
            #get all requests for this endpoint in the last 24 hours
            yesterday=datetime.datetime.now()-datetime.timedelta(days=1)
            requests=Request.objects.filter(endpoint=endpoint,created_at__gte=yesterday)
            #check if there are requests
            if (requests.count()>0):
                response=[]
                #get the status of each request
                for request in requests:
                    status_code=request.status_code
                    status_type="success" if status_code>=200 and status_code<300 else "fail"
                    endpoint=request.endpoint.address
                    response.append({"status":status_type,"endpoint":endpoint,"status_code":status_code,"created_at":request.created_at})
                return Response(response, status=status.HTTP_200_OK)
            else:
                #if there are no requests
                response={"message":"No requests found  for this endpoint"}
                return Response(response, status=status.HTTP_204_NO_CONTENT)
            
        else:
            #if the user is not the owner of the endpoint
            response={"message":"You are not authorized to view this endpoint"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
class CallEndpointView(APIView):
    permission_classes = (AllowAny,)
    #some junk method to call the endpoint
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
    #check if user authenticated
    permission_classes = (IsAuthenticated,)
    queryset = Endpoint.objects.all()
    def get (self, request, *args, **kwargs)->Response:
        #get the endpoint id from the url
        id=self.kwargs['pk']
        endpoint=get_object_or_404(Endpoint,id=id)
        #check if the user is the owner of the endpoint
        if(endpoint.user == request.user):
            #check if the endpoint fail limit is exceeded
            if (endpoint.fail_count>endpoint.fail_limit):
                #get the requests that have status code greater or equal than 300
                requests=Request.objects.filter(endpoint=endpoint,status_code__gte=300)
                #get the difference between the fail count and the fail limit
                diffrence=endpoint.fail_count-endpoint.fail_limit
                response=[]
                length=requests.count()
                #loop through the failed requests and create a response
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
                #if the endpoint fail limit is not exceeded return a success response
                response={"message":"Endpoint is working properly"}
                return Response(response, status=status.HTTP_200_OK)
        else:
            #if the user is not the owner of the endpoint return a bad request response
            response={"message":"You are not authorized to view this endpoint"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        
        

            
