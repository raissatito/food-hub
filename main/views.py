from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import requests

@csrf_exempt
def index(request):
    if request.method == "POST":
        querystring = {}
        querystring["query"] = request.POST.get("food_name")
        if request.POST.getlist("cuisine") != []:
            querystring["cuisine"] = ",".join(request.POST.getlist("cuisine"))
        if request.POST.get("diet") != "none":
            querystring["diet"] = request.POST.get("diet")
        if request.POST.getlist("intolerances") != []:
            querystring["intolerances"] = "".join(request.POST.getlist("intolerances"))
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
        querystring["number"] = "9"
        querystring["instructionsRequired"] = "true"
        querystring["fillIngredients"] = "false"
        querystring["addRecipeInformation"] = "true"
        querystring["ignorePantry"] = "true"
        querystring["sort"] = "calories"
        querystring["sortDirection"] = "asc"
        querystring["limitLicense"] = "false"
        querystring["ranking"] = "2"
        print(request.POST.getlist("cuisine"))
        return redirect("result", query=querystring)
    else:
        return render(request, "index.html")

@csrf_exempt
def result(request, query):
    # url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch"

    # querystring = query

    # headers = {
    #     "X-RapidAPI-Key": "73945d3bc6mshbbb114e5737b534p1e15edjsn076a31989e9d",
    #     "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    # }

    # response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)
    return render(request, "result.html")
