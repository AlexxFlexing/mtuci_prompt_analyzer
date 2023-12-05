from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from .views import UserLogin, UserRegister
import json
# Create your tests here.
class LoginTest(APITestCase):

    
    def test_user_register(self):
        data =json.dumps({"username":"user1","email":"email@example.com","password":"password"})
        print(data)
        client = APIRequestFactory()
        #client = APIClient()
        request = client.post(path='/register',data=data,content_type='application/json')
        response = UserRegister.as_view()(request)
        self.assertEqual( response.status_code ,201)
        
    def test_user_login(self):
        data =json.dumps({"email":"email@example.com","password":"password"})
        print(data)
        client = APIRequestFactory()
        #client = APIClient()
        request = client.post(path='/login',data=data,content_type='application/json')
        response =UserLogin.as_view()(request)
        self.assertEqual( response.status_code ,200)
            
    