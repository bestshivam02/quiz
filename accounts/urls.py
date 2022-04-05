from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from .views import *

urlpatterns = [
    path('login' , login_attempt  , name="login_attempt"),
    path('register' , register_attempt , name="register_attempt"),
    path('logout' , logout_attempt , name="logout_attempt")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

