from django.urls import path
from authen.views import *
from rest_framework_simplejwt.views import   TokenRefreshView, TokenObtainPairView


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('logout_all/', LogoutAllView.as_view(), name='auth_logout_all'),
    path('get-user/',UserView.as_view(),name='get_user'),
    path('get-users/',Userdata.as_view(),name='get_user_personal'),
    path('urlCheck/',UrlCheckView.as_view(),name='chekck user url'),
    path('db/',userdb.as_view(),name='chekck user url'),



]