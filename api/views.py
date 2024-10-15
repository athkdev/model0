from shutil import which
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
def login(request):
    '''
    Return the JWT token for a user after successful login and authenticate the user
    '''

    try:
        user = get_object_or_404(User, username=request.data['email'])

        password = request.data['password']

        if not user.check_password(password):
            return Response({'authenticated': 'false','error': 'AuthenticationError: Email or password does not match.'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)

        payload = {
            'authenticated': 'true',
            'token': token.key,
            'user': UserSerializer(user).data
        }

        return Response(payload, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Login: user does not exist'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout(request):
    try:
        user_id = request.data.get('id')
        user = get_object_or_404(User, id=user_id)

        if user.is_authenticated:
            token = Token.objects.get(user=user)
            token.delete()

        return Response({'authenticated': 'false'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Logout: user does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def signup(request):
    '''
    Return the JWT token for a user after successful signup and authenticate the user
    '''

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():

        user = User.objects.get(email=request.data['username'])
        user.set_password(request.data['password'])
        user.save()

        token = Token.objects.create(user=user)

        serializer.save()

        return Response({'token': token.key})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



