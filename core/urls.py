# chat/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path("<str:id_user>/redirect", views.room_redirect, name="room_redirect"),
    path("<str:room_name>", views.room, name="room"),
    path("", views.index, name="index"),
    
]