from django.urls import path
from . import views

app_name = 'places'
urlpatterns = [
    path('', views.placeList, name='placeList'),
    path('<int:place_pk>/', views.placeDetail, name='placeDetail'),
]