from django.urls import path

from .views.smmodel_views import create_model
from .views.endpoint_views import create_endpoint

urlpatterns = [
    path("model/create/", create_model, name="create_model"),
    path("model/deploy/", create_endpoint, name="deploy_model"),
]
