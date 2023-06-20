from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('home', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('upload', views.upload, name="upload"),
    path('unauthorized', views.unauthorized, name="unauthorized"), 
    path('uploadfile',views.uploadfile, name="uploadfile")
]