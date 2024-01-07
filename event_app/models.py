from django.db import models
import uuid
from users.models import User
from datetime import datetime
from django.utils.text import slugify
from random import  randint
# Create your models here.

class EventPicture(models.Model):
    event = models.ForeignKey('EventObject', on_delete=models.CASCADE, related_name='pictures')
    image = models.ImageField(upload_to='event_pictures/')
    class Meta:
        verbose_name = "Picture"
        verbose_name_plural = "Pictures"
    def __str__(self):
        return f"{self.event.title} picture"

class EventObject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    title = models.CharField(max_length= 255)
    organizer_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    event_Date = models.DateField()
    event_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_archieved = models.BooleanField(default=False)
    list_of_items = models.JSONField(blank=True, null=True, default=list)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    def __str__(self):
        return f"{self.title} by {self.owner.username}"
    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"


class Guests(models.Model):
    event = models.ForeignKey('EventObject', on_delete=models.CASCADE, related_name='event')
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    donations = models.JSONField(blank=True, null=True, default=list)
    class Meta:
        verbose_name = "Guest"
        verbose_name_plural = "Guests"
    def __str__(self):
        return f"{self.name} - {self.event.title} - {self.created_at}"
