from .models import AppUser
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from .views import UserLogin, UserRegister
import json
from importlib import import_module
from django.conf import settings


# Create your tests here.
class LoginTest(APITestCase):

    
    def test_user_register(self):
        data =json.dumps({"username":"user1","email":"email@example.com","password":"password"})
        client = APIRequestFactory()
        request = client.post(path='/register',data=data,content_type='application/json')
        response = UserRegister.as_view()(request)
        self.assertEqual( response.status_code ,201)
       
    def test_user_login(self):
        data =json.dumps({"email":"email@example.com","password":"password"})
        user = AppUser.objects.create_user(email = "email@example.com",password="password")
        client = APIRequestFactory()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request = client.post(path='/login',data=data,content_type='application/json')
        request.session = engine.SessionStore(session_key)      
        response = UserLogin.as_view()(request)
        self.assertEqual( response.status_code ,200)
        
            
    