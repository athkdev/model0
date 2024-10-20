import os

from django.shortcuts import render, get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Project, SMModel
from api.serializer import UserSerializer, SMModelSerializer

from ..services import sagemaker_client, runtime_client

from ..helpers import validate


@api_view(["POST"])
def create_model(request):
    """
    Creates a SageMaker model based on the type specified by the user.

    :param request:
    """

    try:
        model_name = request.data.get("model_name", None)
        description = request.data.get("description", None)
        # model_type = request.data.get("model_type", None)
        user_id = request.data.get("user_id", None)
        project_id = request.data.get("project_id", None)
        auth_token = request.data.get("auth_token", None)

        validate(model_name, "Model name is required!")
        # validate(model_type, "Model type is required!")
        validate(user_id, "User ID is required!")
        validate(project_id, "Project ID is required!")
        validate(auth_token, "Auth token is required!")

        """
        if all validations are gtg, let's add the entry in the data base in the following format
        
        MODEL_ID (PK), MODEL_AWS_ARN, PROJECT_ID (FK), USER_ID (FK)
        
        """

        model_info = sagemaker_client.create_model(
            ModelName="%s" % model_name,
            PrimaryContainer={
                "Image": "%s" % os.getenv("AWS_IMAGE_URI"),
                "ImageConfig": {"RepositoryAccessMode": "Platform"},
            },
            ExecutionRoleArn="arn:aws:iam::%s:role/SageMakerOperator"
            % os.getenv("AWS_ACCOUNT_ID"),
        )

        project = get_object_or_404(Project, id=project_id)

        sm_model = SMModel.objects.create(
            project_id=project_id,
            name=model_name,
            description=description,
            aws_arn=model_info.get("ModelArn"),
        )

        sm_model.save()

        return Response(
            {
                "message": f"Model {model_name} created successfully!",
                "model_id": sm_model.id,
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_models(request):
    """
    Retrieves all models associated with a given project ID.

    Expects project_id as request parameters

    :return: Response
    """

    try:
        user_id = request.data.get("user_id", None)
        project_id = request.data.get("project_id", None)

        validate(project_id, "Project ID is required!")

        sm_models = SMModel.objects.filter(project_id=project_id)

        sm_models_serializer = SMModelSerializer(sm_models, many=True)

        return Response(sm_models_serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
