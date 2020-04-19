from django.contrib import admin
from django.urls import path,include

app_name="users"

from .views import  notificationView,editProfile,editProfileApi,uploadPicture,agreeView,lookUserProfile
from  .views import  follow,profileFollow
urlpatterns = [
    path('notification/',notificationView.as_view(),name="notification"),
    path('editProfile/',editProfile, name="editProfile"),
    path('api/editProfile/',editProfileApi,name="editProfileApi"),
    path('api/uploadPicture/',uploadPicture,name="uploadPicture"),
    path('api/agreebutton/',agreeView,name="agreebutton"),
    path('profile/<int:id>/',lookUserProfile,name="lookProfile"),
    path('api/follow/',follow,name='follow'),
    path('api/profileFollow/',profileFollow,name='profileFollow'),

]















