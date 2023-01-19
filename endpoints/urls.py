from django.urls import path
from .views import *


urlpatterns = [
    path('create/', UrlCreateView.as_view(), name='endpoint create'),
    path('user_urls/', UserUrlView.as_view(), name='user endpoints'),
    path('url_stats/<int:pk>/', UrlStatsView.as_view(), name='endpoint stats'),
    path('<str:url>', UrlStatsView.as_view(), name='request url'),
    path('warnings/<int:pk>/', UrlWarningView.as_view(), name='warnings'),
    
    
    



]