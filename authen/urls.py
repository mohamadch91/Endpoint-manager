from django.urls import path
from .views import *
from rest_framework_simplejwt.views import   TokenRefreshView, TokenObtainPairView

"""define the urls for the authen app
"""
urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    



]