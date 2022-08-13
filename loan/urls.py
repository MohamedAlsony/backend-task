from django.urls import path
from loan import views


app_name = 'loan'

urlpatterns = [
    path('', views.GetLoanAPI.as_view()),

]
