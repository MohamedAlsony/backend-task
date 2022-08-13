from django.urls import path
from investor import views

app_name = 'investor'

urlpatterns = [
    path('get-offers', views.GetOffersAPI.as_view()),
    path('create-offer', views.CreateOffersAPI.as_view()),

]
