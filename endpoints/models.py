from django.db import models

# Create your models here.

from authen.models import User

class Endpoint(models.Model):
    """Endpoint model for saving endpoint information

    Args:
        models (Django models): Django models

    Returns:
        None: None
    """
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
        """String representation of Endpoint model"""
        return self.user.username+" : "+self.address
class Request(models.Model):
    """Request model for saving request information for each endpoint

    Args:
        models (Django models): Django models

   
    """
    id=models.AutoField(primary_key=True,db_index=True)
    endpoint=models.ForeignKey(Endpoint,on_delete=models.CASCADE,blank=True,null=True,db_index=True)
    status_code=models.IntegerField(default=0)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Request'
    
    def __str__(self) -> str:
        """string representation of Request model"""

        return self.endpoint.address