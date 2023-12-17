from django.http import JsonResponse
import sys
import os
from django.contrib.auth import login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import AppUser
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, DataSerializer
from rest_framework import permissions, status, generics
from .validations import custom_validation, validate_email, validate_password
from rest_framework.authtoken.models import Token
import requests



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


class dataUpload(APIView):
    permission_classes = (permissions.AllowAny,) 

    def post(self, request):    
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            def make_request_to_fastapi(get):
                fastapi_url = "http://localhost:8000/api/data"   # Тут наш апи с моделью
                try:
                    response = requests.post(url=fastapi_url, json={"prompt": get, "stream": False})        
                    if response.status_code == 200: 
                        content = response.content.decode('utf-8')      
                        return content
                    else:
                        return JsonResponse({"error": "Failed to retrieve data from FastAPI server"}, status=500)
                except requests.exceptions.RequestException as e:
                    return JsonResponse({"error": str(e)}, status=500)
            
            if serializer.data:
                return JsonResponse({'data' : make_request_to_fastapi(get=serializer.data["body"])}, status=status.HTTP_200_OK)
        
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)



class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)											# JSON data input format:                         
	def post(self, request):																#                               
		clean_data = custom_validation(request.data)										#	{"username":"user", "email":"email@example.com",  "password":"password"}           
		serializer = UserRegisterSerializer(data=clean_data)								#	 
		if serializer.is_valid(raise_exception=True):	
			user = serializer.create(clean_data)	
													
			token = Token.objects.create(user=user)                                                 
			if user:																		
				return Response({'token': token.key},	status=status.HTTP_201_CREATED)			
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):																	# JSON data input format:      
	permission_classes = (permissions.AllowAny,)											#            {"email":"email@example.com",  "password":"password"}               
	authentication_classes = (SessionAuthentication,)                          				#	 
	def post(self, request):																#	  
		data = request.data																	#                           
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			token, created = Token.objects.get_or_create(user=user)
			login(request, user)
			return Response({'token': token.key},status=status.HTTP_200_OK)


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



class UserListView(generics.ListAPIView):
	queryset = AppUser.objects.all()
	serializer_class = UserSerializer
	permission_classes = (permissions.IsAdminUser,)	
	def get(self,request):
		serializer = UserSerializer(request.user)
		return Response({'data' : serializer.data}, status=status.HTTP_200_OK)