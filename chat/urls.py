
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('chat/<int:id>', views.chat, name="chat"),
    path('search/', views.search, name='search'),
    path('send_request/<int:id>/', views.send_request, name='send_request'),
    path('accept_request/<int:id>/', views.accept_request, name='accept_request'),
    path('unfriend/<int:id>/', views.unfriend, name='unfriend'),
    
]
