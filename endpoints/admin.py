from django.contrib import admin
from .models import Endpoint,Request
# Register your models here.
admin.site.register(Endpoint)
admin.site.register(Request)