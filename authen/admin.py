from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
# Register your models here.

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ( 'name','password','username','endpoint_count' ,'created_at','updated_at')
    list_filter = ( 'name','password','username','endpoint_count' ,'created_at','updated_at')
    fieldsets = (
        ('infos', {'fields': ('name','password','username','endpoint_count' )}),
        ('Permissions', {
         'fields': ('is_staff', 'is_active', 'user_permissions')}),
    )
    
    search_fields = ('name','username' ,'created_at','updated_at')
    ordering = ('name','username' ,'created_at','updated_at')
      
