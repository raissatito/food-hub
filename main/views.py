from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import response, HttpResponse, JsonResponse
from rest_framework import status
from .models import UserRecipe
import requests, json

@csrf_exempt
def index(request):
    if request.method == "POST":
        querystring = {}
        querystring["query"] = request.POST.get("food_name")
        if request.POST.getlist("cuisine[]") != []:
            cuisine_list = ",".join(request.POST.getlist("cuisine[]"))
            querystring["cuisine"] = cuisine_list
        if request.POST.get("diet") != "none":
            querystring["diet"] = request.POST.get("diet")
        if request.POST.getlist("intolerances[]") != []:
            intolerances_list = ",".join(request.POST.getlist("intolerances[]"))
            querystring["intolerances"] = intolerances_list
        querystring["instructionsRequired"] = "true"
        querystring["fillIngredients"] = "true"
        querystring["addRecipeInformation"] = "true"
        querystring["titleMatch"] = request.POST.get("food_name")
        querystring["ignorePantry"] = "false"
        querystring["sort"] = "calories"
        querystring["sortDirection"] = "asc"
        querystring["minCarbs"] = request.POST.get("min_carbo")
        querystring["maxCarbs"] = request.POST.get("max_carbo")
        querystring["minProtein"] = request.POST.get("min_protein")
        querystring["maxProtein"] = request.POST.get("max_protein")
        querystring["minCalories"] = request.POST.get("min_calories")
        querystring["maxCalories"] = request.POST.get("max_calories")
        querystring["minFat"] = request.POST.get("min_fat")
        querystring["maxFat"] = request.POST.get("max_fat")
        querystring["minAlcohol"] = request.POST.get("min_alcohol")
        querystring["maxAlcohol"] = request.POST.get("max_alcohol")
        querystring["minSugar"] = request.POST.get("min_sugar")
        querystring["maxSugar"] = request.POST.get("max_sugar")
        querystring["offset"] = "0"
        querystring["number"] = "12"
        querystring["limitLicense"] = "false"
        querystring["ranking"] = "2"
        return redirect("result", query=json.dumps(querystring))
    else:
        return render(request, "index.html")

@csrf_exempt
def result(request, query):
    query = json.loads(query)
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch"

    headers = {
        "X-RapidAPI-Key": "73945d3bc6mshbbb114e5737b534p1e15edjsn076a31989e9d",
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=query)
    result = response.json()
    return render(request, "result.html", result)

@csrf_exempt
def analyze(request):
    if request.method == "POST":
        payload = {}
        payload["title"] = request.POST.get("food_name")
        ingredient_list = request.POST.get("ingredients").split(",")
        payload["ingredients"] = ingredient_list
        payload["instructions"] = request.POST.get("steps")
        payload = json.dumps(payload)
        return redirect("analyze-result", payload=payload)
    else:
        return render(request, "analyze.html")

@csrf_exempt
def analyze_result(request,payload):
    if request.method == "POST":
        if request.POST.getlist("share[]") != []:
            is_shared = True
        else:
            is_shared = False
        recipe = UserRecipe(user=request.user, recipe_value=request.session["analyze_response"], is_public=is_shared, image_link=request.POST.get("image_link"))
        recipe.save()
        return redirect("profile")
    else:
        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/analyze"

        querystring = {"language":"en","includeNutrition":"true","includeTaste":"false"}

        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "73945d3bc6mshbbb114e5737b534p1e15edjsn076a31989e9d",
            "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }

        response = requests.request("POST", url, json=json.loads(payload), headers=headers, params=querystring)
        result = response.json()
        request.session["analyze_response"] = result
        return render(request, "analyze_result.html", result)
    
@csrf_exempt
def discover(request):
    recipe_list = UserRecipe.objects.filter(is_public=True).values("recipe_value", "image_link")[::1]
    return render(request, "discover.html", {"results": recipe_list})

@csrf_exempt
def delete(request, recipe_id):
    recipe = UserRecipe.objects.get(recipe_id=recipe_id)
    recipe.delete()
    return redirect("profile")

@csrf_exempt
def set_visibility(request, recipe_id):
    recipe = UserRecipe.objects.get(recipe_id=recipe_id)
    if recipe.is_public:
        recipe.is_public = False
    else:
        recipe.is_public = True
    recipe.save()
    return redirect("profile")