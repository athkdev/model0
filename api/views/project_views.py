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
