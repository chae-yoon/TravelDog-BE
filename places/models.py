from django.db import models
from django.conf import settings

# Create your models here.
class Place(models.Model):
    areaName = models.CharField(max_length=50)
    partName = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    keyword = models.CharField(max_length=250)
    address = models.CharField(max_length=300)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    tel = models.CharField(max_length=30)
    usedTime = models.CharField(max_length=200)
    homePage = models.URLField()
    content = models.TextField()
    provisionSupply = models.CharField(max_length=300)
    petFacility = models.CharField(max_length=300)
    restaurant = models.CharField(max_length=300)
    parkingLog = models.CharField(max_length=300)
    mainFacility = models.CharField(max_length=300)
    usedCost = models.CharField(max_length=300)
    policyCautions = models.CharField(max_length=300)
    emergencyResponse = models.CharField(max_length=300)
    memo = models.TextField()
    bathFlag = models.CharField(max_length=10)
    provisionFlag = models.CharField(max_length=10)
    petFlag = models.CharField(max_length=10)
    petWeight = models.CharField(max_length=10)
    dogBreed = models.CharField(max_length=10)
    emergencyFlag = models.CharField(max_length=10)
    entranceFlag = models.CharField(max_length=10)
    parkingFlag = models.CharField(max_length=10)
    inOutFlag = models.CharField(max_length=10)

class PlaceIMG(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='imageList')
    image = models.URLField()

class Review(models.Model):
    points = zip(range(1, 6), range(1, 6))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_reviews')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='place_reviews')
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews', blank=True)
    star = models.IntegerField(choices=points)