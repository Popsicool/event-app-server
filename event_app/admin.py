from django.contrib import admin

# Register your models here.
from .models import EventObject, EventPicture,Guests


class EventObjectAdmin(admin.ModelAdmin):
    list_display = ['id','slug','owner', 'title', 'event_Date', 'created_at']
    search_fields = ('email', 'username')
    ordering = ('-created_at',)
    list_filter = ('is_archieved',)

class GuestsAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'email', 'phone']
    search_fields = ('name', 'event')
    ordering = ('-created_at',)

admin.site.register(EventObject, EventObjectAdmin)
admin.site.register(EventPicture)
admin.site.register(Guests, GuestsAdmin)