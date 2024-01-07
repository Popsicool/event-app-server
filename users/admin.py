from django.contrib import admin

# Register your models here.
from .models import User, EmailVerification


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'auth_provider', 'created_at']
    search_fields = ('email', 'username')
    ordering = ('-created_at',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

admin.site.register(User, UserAdmin)
admin.site.register(EmailVerification)