import os

from django.shortcuts import render, get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Project, SMModel
from ..models import User
from api.serializer import UserSerializer

from ..services import sagemaker_client, runtime_client

from ..helpers import validate


@api_view(["POST"])
def create_project(request):
    try:
        user_id = request.data.get("user_id", None)
        project_name = request.data.get("project_name", None)
        description = request.data.get("description", None)

        validate(user_id, "User ID is required!")
        validate(project_name, "Project name is required!")

        user = get_object_or_404(User, id=user_id)
        project = Project.objects.create(
            user_id=user,
            name=project_name,
            description=description if description else "",
        )

        project.save()

        return Response(
            {
                "message": f"Project {project_name} created successfully!",
                "model_id": project.id,
            },
            status=status.HTTP_201_CREATED,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
