from django.contrib import admin
from django.urls import path,include,re_path

from .views import  indexView,PostContentView,writePostView,selectPostAjaxView,ajaxDraftsView,ajaxDraftsContentView,EmailSettingsView,ads
from  .views import NewProfileView,notificationView,allCommentList,DraftsView,Sort_View,searchPostView,postSuccess,apiAllPost,apiAllPostRecommend,apiGetPost,apiGetSort,apiGetSortContent,getCarousel
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
app_name="topic"

urlpatterns = [
    path('',indexView.as_view(),name="index"),
    re_path('ads.txt',ads,name="ads"),
    path('drafts/<str:type>/', DraftsView.as_view(), name="drafts"),
    path('postContent/<str:postId>/<str:slug>/',PostContentView.as_view(),name="postContent"),
    path('writePost/<str:type>/',writePostView.as_view(),name="writePost"),
    path('api/selectPost/',selectPostAjaxView,name="AjaxPost"),
    path('api/drafts/',ajaxDraftsView.as_view(),name="writeDrafts"),
    path('api/drafts/<str:draftsId>/',ajaxDraftsContentView.as_view(),name="writeDraftsContent"),
    path('settings/email/',EmailSettingsView.as_view(),name="emailSettings"),
    path('accounts/profile/',NewProfileView.as_view(),name="new_profile"),
    path('api/notifications/',notificationView,name="notifications"),
    path('api/allCommentList/',allCommentList,name="allCommentList"),
    path('sort/',Sort_View.as_view(),name='Sort'),
    path('sort/<int:node_id>/',Sort_View.as_view(),name='SortContent'),
    path('search/',searchPostView,name='searchContent'),
    path('success/<str:username>/',postSuccess,name='postSuccess'),   
    path('api/allPost/',apiAllPost,name='apiAllpost'),
    path('api/allPost/recommend/',apiAllPostRecommend,name='apiAllPostRecommend'),
    path('api/getPost/',apiGetPost,name='apiGetPost'),
    path('api/getSort/',apiGetSort,name='apiGetSort'),
    path('api/getSortContent/',apiGetSortContent,name='apiGetSortContent'),
    path('api/getCarousel/',getCarousel,name='getCarousel'),


]
