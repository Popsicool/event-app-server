from django.urls import path
from . import views

app_name = 'event_app'

urlpatterns = [
    path('create', views.CreateEvent.as_view(), name='create'),
    path('modify/<pk>/', views.ModifyEvent.as_view(), name='modify'),
    path('invite/<slug>/', views.Invite.as_view(), name="register"),
    path('register/<slug>/', views.Register.as_view(), name="register"),
    path('donate/<slug>', views.Donation.as_view(), name='donate')

]