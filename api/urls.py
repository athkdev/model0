from django.urls import path

from .views import get_users, login, signup, logout

urlpatterns = [
    path('user/all', get_users, name='get_user'),
    path('user/login', login, name='login'),
    path('user/signup', signup, name='signup'),
    path('user/logout', logout, name='logout'),
]