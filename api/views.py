from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from bson.json_util import dumps
import json
from pymongo import MongoClient
# Create your views here.


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class Users(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username:
            return Response({'detail': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({'detail': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not first_name:
            return Response({'detail': 'First name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not last_name:
            return Response({'detail': 'LastName is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not email:
            return Response({'detail': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.get(username=username)
            return Response({'detail': 'User with this username already exist!'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:pass

        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        new_user.save()

        new_user.set_password(password)

        new_user.save()

        return Response({'message': "User creation was successful"}, status=status.HTTP_200_OK)

    def get(self, request):

        object_list = User.objects.all()

        serializer = UserSerializer(object_list, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class Products(APIView):
    permission_classes = [AllowAny,]

    def get(self, request):
        client = MongoClient('localhost', 27017)
        db = client['ecommerce']

        products = db['product'].find({})

        products = dumps(products)
        
        return Response(json.loads(products), status=status.HTTP_200_OK)
