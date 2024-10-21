from django.urls import path

from .views.smmodel_views import (
    create_model,
    get_inference,
    create_endpoint,
    delete_endpoint,
    get_models,
)

from .views.project_views import create_project, get_user_projects

urlpatterns = [
    path("model/", get_models, name="get_models"),
    path("model/create/", create_model, name="create_model"),
    path("model/deploy/", create_endpoint, name="deploy_model"),
    path("model/withdraw/", delete_endpoint, name="withdraw_model"),
    path("model/inference", get_inference, name="get_inference"),
    path("project/create", create_project, name="create_project"),
    path("project/", get_user_projects, name="get_user_projects"),
]
