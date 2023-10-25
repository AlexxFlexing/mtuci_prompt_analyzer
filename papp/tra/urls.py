from django.urls import path
from . import views


urlpatterns = [
    path("",views.dataUpload.home, name="home")
]

#