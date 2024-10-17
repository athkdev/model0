from django.urls import path

from .views import get_hello

urlpatterns = [
    path('hello/', get_hello, name='get_hello'),
]