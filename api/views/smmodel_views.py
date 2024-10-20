import os

from botocore.endpoint import Endpoint
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
    :return: Response
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

    :param request
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


@api_view(["POST"])
def create_endpoint(request):

    try:
        user_id = request.data.get("user_id", None)
        model_id = request.data.get("model_id", None)
        project_id = request.data.get("project_id", None)

        validate(user_id, "User ID is required!")
        validate(model_id, "Model ID is required!")
        # validate(project_id, "Project ID is required!")

        sm_model = get_object_or_404(SMModel, id=model_id)
        model_name = sm_model.name

        endpoint_config_name = model_name + "-endpoint-config"

        # create an endpoint config for the following endpoint
        endpoint_config_response = sagemaker_client.create_endpoint_config(
            EndpointConfigName=endpoint_config_name,
            ProductionVariants=[
                {
                    "VariantName": "AllTraffic",
                    "ModelName": model_name,
                    "InstanceType": "ml.m5.xlarge",
                    "InitialInstanceCount": 1,
                }
            ],
        )

        endpoint_name = model_name + "-endpoint"
        # create an endpoint that can be used to communicate with the model
        endpoint_response = sagemaker_client.create_endpoint(
            EndpointName=endpoint_name, EndpointConfigName=endpoint_config_name
        )

        sm_model.endpoint_name = endpoint_name
        sm_model.endpoint_config_name = endpoint_config_name
        sm_model.is_deployed = True

        sm_model.save()

        return Response(
            {"message": "Model deployed.", "response": endpoint_response},
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def delete_endpoint(request):
    try:
        model_id = request.data.get("model_id", None)

        validate(model_id, "Model ID is required!")

        sm_model = get_object_or_404(SMModel, id=model_id)

        if not sm_model.endpoint_name:
            raise Exception("Model does not contain an endpoint")

        delete_endpoint_config_response = sagemaker_client.delete_endpoint_config(
            EndpointConfigName=sm_model.endpoint_config_name
        )

        delete_endpoint_response = sagemaker_client.delete_endpoint(
            EndpointName=sm_model.endpoint_name
        )

        sm_model.endpoint_name = ""
        sm_model.endpoint_config_name = ""
        sm_model.is_deployed = False

        sm_model.save()

        return Response(
            {
                "message": "Endpoint and endpoint config deleted successfully.",
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def get_inference(request):

    try:
        user_id = request.data.get("user_id", None)
        model_id = request.data.get("model_id", None)

        user_prompt = request.data.get("user_prompt", None)

        validate(user_id, "User ID is required!")
        validate(model_id, "Model ID is required!")
        validate(user_prompt, "User prompt is required!")

        sm_model = get_object_or_404(SMModel, id=model_id)

        endpoint_name = sm_model.endpoint_name

        prompt_response = runtime_client.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType="application/json",
            Body=f'{"inputs": "{user_prompt}"}',
        )

        print(prompt_response)

        return Response(
            {
                "message": "Endpoint and endpoint config deleted successfully.",
                "response": prompt_response,
            },
            status=status.HTTP_204_NO_CONTENT,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
