from django.urls import path

from .views import get_users, create_user

urlpatterns = [
    path('user/all', get_users, name='get_user'),
    path('user/create', create_user, name='get_user'),
]