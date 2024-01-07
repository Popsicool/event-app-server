from django.urls import path

from .views import GoogleSocialAuthView, FacebookSocialAuthView, TwitterSocialAuthView


app_name = 'social_auth'

urlpatterns = [
    path('google/', GoogleSocialAuthView.as_view()),
    path('facebook/', FacebookSocialAuthView.as_view()),
    path('twitter/', TwitterSocialAuthView.as_view()),


]