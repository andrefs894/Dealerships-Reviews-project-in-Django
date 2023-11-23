import requests
import json
from .models import CarDealer, DealerReview
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from requests.auth import HTTPBasicAuth


# http get requests
def get_request(url, api_key=False, **kwargs):
    if api_key:
        try:
            if "3000" in url:
                response = requests.get(url, headers={'Content-Type': 'application/json'},
                                            params={'id': kwargs.get("id")},
                                            auth=HTTPBasicAuth('apikey', api_key))
            if "5000" in url:
                response = requests.get(url, headers={'Content-Type': 'application/json'},
                                            params={'dealership': kwargs.get("id")},
                                            auth=HTTPBasicAuth('apikey', api_key))
        except:
            print("Network exception occurred")
    else:
        try:
            if "3000" in url:
                response = requests.get(url, headers={'Content-Type': 'application/json'},
                                            params={'id': kwargs.get("id")})
            if "5000" in url:
                response = requests.get(url, headers={'Content-Type': 'application/json'},
                                            params={'dealership': kwargs.get("id")})
        except:
            print("Network exception occurred")

    json_data = json.loads(response.text)
    return json_data

# http post requests
def post_request(url, json_payload, **kwargs):
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(url, headers=headers, params=kwargs, data=json_payload)
    print(response.text)
    return response

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
            if dealer_review["purchase"] is False:
                review_obj = DealerReview(dealership=dealer_review["dealership"],
                                    name=dealer_review["name"],
                                    purchase=dealer_review["purchase"],
                                    review=dealer_review["review"],
                                    id=dealer_review["id"],
                                    purchase_date=None,
                                    car_make=None,
                                    car_model=None,
                                    car_year=None,
                                    sentiment=analyze_review_sentiments(dealer_review["review"])
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
                                    sentiment=analyze_review_sentiments(dealer_review["review"])
                                    )
            results.append(review_obj)
    return results

# get sentiment from reviews using NLU
def analyze_review_sentiments(review):
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/6ca8aa54-1444-4f73-b4f9-813129b34b32"
    api_key = "xAAVCcEcppvZC2nAjcPu1xOvRjEPHa28etFJ2BsmOVT3"   
    version = '2021-08-01'
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(version=version, authenticator=authenticator)
    nlu.set_service_url(url)
    try:
        response = nlu.analyze(text=review, features=Features(sentiment=SentimentOptions())).get_result()
        sentiment_label = response["sentiment"]["document"]["label"]
    except:
        sentiment_label = "neutral"
    return sentiment_label
