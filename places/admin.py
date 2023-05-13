from django.contrib import admin
from .models import Place, PlaceIMG, Review

# Register your models here.
admin.site.register(Place)
admin.site.register(PlaceIMG)
admin.site.register(Review)