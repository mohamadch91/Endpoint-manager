from django.urls import path
from .views import *


urlpatterns = [
    path('create/', UrlCreateView.as_view(), name='url_create'),
    path('user_urls/', UserUrlView.as_view(), name='user_urls'),
    path('url_stats/<int:pk>/', UrlStatsView.as_view(), name='url_stats'),
    



]