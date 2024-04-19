
from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('change_profile_picture/', views.change_profile_picture, name='change_profile_picture')
    
]
