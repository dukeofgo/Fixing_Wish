from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('users', views.users),
    path('users/new', views.add_user),
    path('users/<int:id>/dashboard', views.dashboard),
    path('users/login', views.user_login),
    path('users/logout', views.user_logout),
    path('users/edit', views.user_edit),
    path('users/update', views.user_update),
    path('wishes', views.wishes),
    path('wishes/add', views.new_wish),
    path('wishes/new', views.add_wish),
    path('wishes/edit', views.wish),
    path('wishes/update', views.update_wish),
    path('wishes/destroy', views.delete_wish),    
    path('wishes/granted', views.granted_wish),  
    path('wishes/like', views.like_wish),  
    path('wishes/unlike', views.unlike_wish),     
    path('wishes/stat', views.stat), 
]