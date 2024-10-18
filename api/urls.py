from django.urls import path

from .views import create_model

urlpatterns = [
    path("create-model/", create_model, name="create_model"),
]
