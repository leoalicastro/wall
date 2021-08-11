from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('wall', views.wall),
    path('login', views.login),
    path('message', views.message),
    path('comment/<int:message_id>', views.comment),
    path('delete/<int:message_id>', views.delete),
    path('logout', views.logout)
]