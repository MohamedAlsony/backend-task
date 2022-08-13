from django.urls import path
from borrower import views


app_name = 'borrower'

urlpatterns = [
    path('get-all-requests', views.GetRequestsAPI.as_view()),
    path('create-request', views.CreateRequestsAPI.as_view()),
    path('get-request-offers/<int:loan_request_id>', views.GetRequestOfferAPI.as_view()),
    path('pay-installment', views.PayInstallmentAPI.as_view()),
    path('accept-offer/<int:loan_offer_id>', views.AcceptOfferAPI.as_view()),

]
