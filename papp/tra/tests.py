from django.test import TestCase
from rest_framework.test import APIRequestFactory
from views import UserLogin
# Create your tests here.
class LoginTest(TestCase):

    def log_in(self, data, title="log_in_test",body="bebebe"):
        factory = APIRequestFactory
        request = factory.post(path='/login',data=data,format='json',title=title,body=body)
        return request
    def test_login(self):
        data = {"email":"email@example.com",  "password":"password"} 
        url = UserLogin
        resp = self.log_in(data)
        self.assertEqual(resp.status_code,200)
            
    