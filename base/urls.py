from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('createpost/', views.createpost, name='createpost'),
    path('deletepost/<str:pk>', views.deletepost, name='deletepost'),
    path('commentspost/<str:pk>', views.commentspost, name='commentspost'),
    path('userprofile/<str:pk>', views.userprofile, name='userprofile'),
    path('myposts/', views.myposts, name='myposts')
]
