from django.urls import path, re_path
from . import views

urlpatterns = [
    path('profile/', views.profile),
    re_path('id(?P<user_id>\w+)', views.profile_by_id),
]
