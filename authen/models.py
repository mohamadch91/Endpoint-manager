from django.db import models

from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
  
    name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    endpoint_count = models.IntegerField(default=0)

    REQUIRED_FIELDS = []
    class Meta:
        # managed = False
        db_table = 'User'
 
 