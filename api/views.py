import os
import boto3

from django.shortcuts import render, get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer

sagemaker_client = boto3.client(
    "sagemaker",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
)
runtime_client = boto3.client("sagemaker-runtime")


def validate(field, msg):
    if not field:
        raise Exception(msg)


@api_view(["POST"])
def create_model(request):
    """
    Creates a SageMaker model based on the type specified by the user.

    :param request:
    """

    try:
        model_name = request.data.get("model_name", None)
        model_type = request.data.get("model_type", None)
        user_id = request.data.get("user_id", None)
        project_id = request.data.get("project_id", None)

        validate(model_name, "Model name is required!")
        # validate(model_type, "Model type is required!")
        validate(user_id, "User ID is required!")
        validate(project_id, "Project ID is required!")

        model_info = sagemaker_client.create_model(
            ModelName="%s" % model_name,
            PrimaryContainer={
                "Image": "%s" % os.getenv("AWS_IMAGE_URI"),
                "ImageConfig": {"RepositoryAccessMode": "Platform"},
                # "ModelDataUrl": "s3://%s" % os.getenv("AWS_S3_BUCKET_NAME"),
            },
            ExecutionRoleArn="arn:aws:iam::%s:role/SageMakerOperator"
            % os.getenv("AWS_ACCOUNT_ID"),
        )

        return Response(
            {"message": "Model creation started", "response": model_info},
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
