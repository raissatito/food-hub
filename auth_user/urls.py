from django.urls import include, path
from .views import *

urlpatterns = [
    path("login", auth_login , name="login"),
    path("register", register, name="register"),
    path("logout", logout_auth, name="logout"),
    path("profile", profile, name="profile"),
]