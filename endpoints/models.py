from django.db import models

# Create your models here.

from authen.models import User

class Endpoint(models.Model):
    id=models.AutoField(primary_key=True,db_index=True)
    address = models.CharField(max_length=200, blank=True, null=True,unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,db_index=True)
    fail_limit = models.IntegerField(default=0,db_index=True)
    success_count = models.IntegerField(default=0)
    fail_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Endpoint'
    
    def __str__(self) -> str:
        return self.user.username+" : "+self.address
class Request(models.Model):
    id=models.AutoField(primary_key=True,db_index=True)
    enpoint=models.ForeignKey(Endpoint,on_delete=models.CASCADE,blank=True,null=True,db_index=True)
    status_code=models.IntegerField(default=0)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Request'
    
    def __str__(self) -> str:
        return self.enpoint.address