from django.shortcuts import HttpResponse
from string import ascii_letters
import sys
import os
import random
from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, DataSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# Create your views here.


    
#def home(request):
    #{'random_str': random_string()}
    #return Response(data = {'random_str': random_string()},status = status.HTTP_200_OK)

#def random_string():
    #random_str = ''
    #for i in range(random.randint(31,63)):
        #random_str += random.choice(ascii_letters)
    #return random_str
def random_string():
	random_str = ''
	for i in range(random.randint(31,63)):		
		random_str += random.choice(ascii_letters)
	return random_str

class dataUpload(APIView):
	permission_classes = (permissions.AllowAny)
	
	
	
	def home(self, request):
		clean_data = custom_validation(request.data)
		serializer = DataSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			r_data = random_string()
			if r_data:
				return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(status=status.HTTP_400_BAD_REQUEST)



class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		clean_data = custom_validation(request.data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(clean_data)
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	##
	def post(self, request):
		data = request.data
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)
			return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)