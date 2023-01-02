from django.urls import path
from .views import *


urlpatterns = [
    path('', GetWarningView.as_view(), name='warning')
    



]