from django.db import models
from django.utils.timezone import now

# user class
class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.username
        
# carmake class
class CarMake(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name

# carmodel class
class CarModel(models.Model):
    dealer_id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    TYPE_CHOICES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    ]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='car_models')
    car_type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    year = models.DateField()

    def __str__(self):
        return self.name

# cardealer class
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# dealerreview class
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return "Review: " + self.review



