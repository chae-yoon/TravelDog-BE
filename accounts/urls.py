from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.account, name='account'),
    path('login/', views.login, name='login'),
]