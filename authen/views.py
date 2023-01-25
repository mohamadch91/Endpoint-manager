
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

class RegisterView(generics.CreateAPIView):
    """view for registering a new user

    Args:
        generics (Api view): Api view for creating a new user
    """
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer   

class LogoutView(APIView):
    """Logout view for logging out a user and blacklisting the refresh token

    Args:
        APIView (Django view): Django view for logging out a user

    Returns:
        _type_: Http response
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)    
