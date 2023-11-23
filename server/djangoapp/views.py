from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .restapis import get_dealers_from_cf, get_request, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request
from .models import CarMake, CarModel, CarDealer, DealerReview
import logging
import json

logger = logging.getLogger(__name__)

# about view
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# contact view
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# login view
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# logout view
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')

# registration view
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# index view
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://andrefs894-3000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealerships = get_dealers_from_cf(url)
        context['dealerships'] = dealerships
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        return render(request, 'djangoapp/index.html', context)

# get dealer details view
def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        dealer_url = "https://andrefs894-3000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
        context["dealer"] = dealer
        review_url = "https://andrefs894-5000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/reviews/get"
        reviews = get_dealer_reviews_from_cf(review_url, id=id)
        context["reviews"] = reviews
        cars = CarModel.objects.all()
        print(cars)
        return render(request, 'djangoapp/dealer_details.html', context)

# add review view
def add_review(request, id):
    context = {}
    url = "https://andrefs894-3000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
    dealer = get_dealer_by_id_from_cf(url, id)
    context["dealer"] = dealer

    if request.method == 'GET':
        cars = CarModel.objects.all()
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)

    elif request.method == 'POST':
        car_id = request.POST["car"]
        car = CarModel.objects.get(pk=car_id)

        review_post_url = "https://andrefs894-5000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/reviews/post"
        review_get_url = "https://andrefs894-5000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/reviews/get"
        
        reviews = get_dealer_reviews_from_cf(review_get_url)
        reviews_id = []
        for review in reviews:
            reviews_id.append(review.id)
        max_id = max(reviews_id)
        next_id = max_id + 1

        if request.POST["purchase"] == 'false':
            review = {
                "id": next_id,
                "dealership": id,
                "name": request.user.username,
                "review": request.POST["review"],
                "purchase": False,
            }
        else:
            review = {
                "id": next_id,
                "dealership": id,
                "name": request.user.username,
                "review": request.POST["review"],
                "purchase": True,
                "purchase_date": request.POST["purchase_date"],
                "car_make": car.car_make.name,
                "car_model": car.name,
                "car_year": car.year
            }

        json_review=json.dumps(review)
        #print("AAAAAAAAAAAAAAAAAA")
        #print(type(json_review))
        post_request(review_post_url, json_review, id = id)
        return redirect("djangoapp:dealer_details", id = id)
