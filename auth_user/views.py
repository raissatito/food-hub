from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from main.models import UserRecipe

@csrf_exempt
def auth_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return redirect("login")
    else:
        return render(request, "login.html")

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect("login")
        else:
            return redirect("register")
    else:
        return render(request, "register.html")

@csrf_exempt
def logout_auth(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@csrf_exempt
def profile(request):
    if request.user.is_authenticated:
        user_model = User.objects.get(username=request.user.username)
        recipe_list = UserRecipe.objects.filter(user=user_model).values("recipe_value", "image_link", "is_public", "recipe_id")[::1]
        return render(request, "profile.html", {"results": recipe_list})
    return redirect("login")
