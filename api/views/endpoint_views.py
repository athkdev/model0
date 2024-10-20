import os

from django.shortcuts import render, get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Project, SMModel
from api.serializer import UserSerializer

from ..services import sagemaker_client, runtime_client
from ..helpers import validate


@api_view(["POST"])
def create_endpoint(request):
    try:
        model_name = request.data.get("model_name", None)

        validate(model_name, "Model name is required!")

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

        return Response(
            {"message": "Model deployed.", "response": endpoint_response},
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
