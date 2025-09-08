from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Perfil"

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Re-registrar User con la nueva config
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
