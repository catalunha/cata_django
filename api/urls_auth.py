from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import (
    obtain_jwt_token, 
    refresh_jwt_token, 
    verify_jwt_token,
)
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.db.models.signals import post_save

app_name = 'auth'


urlpatterns = [
    path("get-auth-token", obtain_auth_token),
    path('jwt/', include([
        path('auth-token/', obtain_jwt_token),
        path('refresh-token/', refresh_jwt_token),
        path('verify-token/', verify_jwt_token),
    ])),    
]

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
