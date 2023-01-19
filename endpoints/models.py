from django.db import models

# Create your models here.

from authen.models import User

class Url(models.Model):
    id=models.AutoField(primary_key=True,db_index=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,db_index=True)
    fail_limit = models.IntegerField(default=0,db_index=True)
    success_count = models.IntegerField(default=0)
    fail_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Url'

class Request(models.Model):
    id=models.AutoField(primary_key=True,db_index=True)
    url=models.ForeignKey(Url,on_delete=models.CASCADE,blank=True,null=True,db_index=True)
    status_code=models.IntegerField(default=0)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Request'