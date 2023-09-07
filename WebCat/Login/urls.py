from django.urls import path, re_path
from . import views

urlpatterns = [
    path('sign_up/', views.sign_up),
    re_path(r'^check_email', views.check_email),
    re_path(r'^register', views.register),
    path('set_session_variable/', views.set_session_variable),
    path('check_authorize/', views.authorize),
    path('log_out/', views.log_out),
]