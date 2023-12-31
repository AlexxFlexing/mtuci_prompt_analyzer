from django.urls import path
from . import views


urlpatterns = [
    path("home",views.dataUpload.as_view(), name="home"),
    path('register', views.UserRegister.as_view(), name='register'),
	path('login', views.UserLogin.as_view(), name='login'),
	path('logout', views.UserLogout.as_view(), name='logout'),
	path('user', views.UserView.as_view(), name='user'),  
    path('userlist',views.UserListView.as_view(), name = 'userlist')  
]

#