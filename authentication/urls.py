from django.urls import path
from .views import *

urlpatterns = [
    path('signin/', signIn_page, name='sign-in'),
    path('signup/', signUp_page, name='sign-up'),
    path('signup-user/', signupView, name='signup-user'),
    path('signin-user/', signInView, name='signin-user'),
    path('logout/', logoutView, name='sign-in'),
]
