from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.account, name='account'),
    path('signup/', views.signup, name='signup'),
    path('password/', views.password, name='password'),
    path('<str:username>/', views.profile, name='profile'),
]