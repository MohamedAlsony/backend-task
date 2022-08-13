from django.urls import path
from account import views


app_name = 'account'

urlpatterns = [
    path('register/investor', views.RegisterAPI.as_view(account_type='investor')),
    path('register/borrower', views.RegisterAPI.as_view(account_type='borrower')),
    path('add-bank-account', views.AddBankAccount.as_view()),

]
