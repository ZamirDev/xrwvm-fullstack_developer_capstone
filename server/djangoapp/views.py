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
from .restapis import get_request
from django.http import JsonResponse
from .restapis import get_request, analyze_review_sentiments

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
    from django.http import JsonResponse


def get_dealerships(request, state="All"):

    dealerships = [
        {
            "id": 1,
            "name": "Honda Dealer",
            "state": "CA",
            "city": "San Francisco"
        },
        {
            "id": 2,
            "name": "Toyota Dealer",
            "state": "TX",
            "city": "Dallas"
        }
    ]

    return JsonResponse({"status": 200, "dealers": dealerships})

def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealer = get_request(endpoint)

        if dealer is None:
            dealer = {}

        return JsonResponse({"status": 200, "dealer": dealer})

    return JsonResponse({"status": 400, "message": "Bad Request"})

def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        if reviews is None:
            reviews = []

        for review in reviews:
            response = analyze_review_sentiments(review['review'])
            review['sentiment'] = response.get('sentiment', 'neutral')

        return JsonResponse({"status": 200, "reviews": reviews})

    return JsonResponse({"status": 400, "message": "Bad Request"})