from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
import logging
from .models import CarMake, CarModel
from django.http import JsonResponse
from .models import CarMake, CarModel
from .populate import initiate

logger = logging.getLogger(__name__)
def get_cars(request):
    count = CarMake.objects.count()
    
    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })

    return JsonResponse({"CarModels": cars})

def get_cars(request):
    count = CarModel.objects.count()

    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')

    cars = [
        {
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        }
        for car_model in car_models
    ]

    return JsonResponse({"CarModels": cars})


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        user = authenticate(
            username=data['userName'],
            password=data['password']
        )

        if user:
            login(request, user)
            return JsonResponse({"userName": user.username, "status": "Authenticated"})
        else:
            return JsonResponse({"status": "Failed"})

    return JsonResponse({"status": "Invalid request"})


@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("userName")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Already Registered"})

        user = User.objects.create_user(
            username=username,
            password=data.get("password"),
            email=data.get("email"),
            first_name=data.get("firstName"),
            last_name=data.get("lastName")
        )

        login(request, user)

        return JsonResponse({"status": True, "userName": username})

    return JsonResponse({"status": False})