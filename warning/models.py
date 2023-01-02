from django.db import models

# Create your models here.

from endpoints.models import Url

class Warning(models.Model):

    id=models.AutoField(primary_key=True)
    url = models.ForeignKey(Url, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # managed = False
        db_table = 'Warning'