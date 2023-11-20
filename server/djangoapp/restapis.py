import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# http get requests
def get_request(url, **kwargs):
    # print(kwargs)
    # print("GET from {} ".format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    # print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

# get dealers from cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result
        for dealer in dealers:
            dealer_doc = dealer
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# get dealers from cloud function, by dealer id
def get_dealer_by_id_from_cf(url, id):
    results = []
    json_result = get_request(url, id=id)
    if json_result:
        dealers = json_result
        for dealer in dealers:
            dealer_doc = dealer
            if dealer_doc["id"] == id:
                dealer_obj = CarDealer(address=dealer_doc["address"], 
                                       city=dealer_doc["city"], 
                                       full_name=dealer_doc["full_name"],
                                       id=dealer_doc["id"], 
                                       lat=dealer_doc["lat"], 
                                       long=dealer_doc["long"],
                                       short_name=dealer_doc["short_name"],
                                       st=dealer_doc["st"], 
                                       zip=dealer_doc["zip"])                    
                results.append(dealer_obj)
    return results[0]

# get dealer reviews from cloud function
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
    if json_result:
        reviews = json_result
        for dealer_review in reviews:
            if "purchase_date" not in dealer_review:
                review_obj = DealerReview(dealership=dealer_review["dealership"],
                                    name=dealer_review["name"],
                                    purchase=dealer_review["purchase"],
                                    review=dealer_review["review"],
                                    id=None,
                                    purchase_date=None,
                                    car_make=None,
                                    car_model=None,
                                    car_year=None,
                                    sentiment=None
                                    )
            else:
                review_obj = DealerReview(dealership=dealer_review["dealership"],
                                    name=dealer_review["name"],
                                    purchase=dealer_review["purchase"],
                                    review=dealer_review["review"],
                                    id=dealer_review["id"],
                                    purchase_date=dealer_review["purchase_date"],
                                    car_make=dealer_review["car_make"],
                                    car_model=dealer_review["car_model"],
                                    car_year=dealer_review["car_year"],
                                    sentiment=None
                                    )
            """sentiment = analyze_review_sentiments(review_obj.review)
            print(sentiment)
            review_obj.sentiment = sentiment"""
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



