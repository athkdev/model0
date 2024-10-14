from urllib import request

from django.shortcuts import render, get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
# from django.contrib.auth.models import User
from .serializer import UserSerializer

# Create your views here.

@api_view(['GET'])
def get_users(request):
    return Response(UserSerializer(User.objects.all(), many=True).data)

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):

    user = get_object_or_404(User, username=request.data['email'])

    if not user.check_password(request.data['password']):
        pass

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()



    return Response({})

@api_view(['POST'])
def signup(request):

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()

        token = Token.objects.create(user=user)

        return Response({'token': token.key})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



