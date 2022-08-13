from pprint import pprint
from rest_framework.authtoken.models import Token
from account.models import *
from django.test import TestCase,Client, TransactionTestCase
from rest_framework.test import APIClient
from django.test import SimpleTestCase

import json


class TestViews(TransactionTestCase):
    data = dict()
    # Create fake data and client and add app urls to vars
    def setUp(self):
        self.client = APIClient()
        self.register_investor_url = '/api/account/register/investor'
        self.register_borrower_url = '/api/account/register/borrower'

    # check if data is correct and response is correct
    def test_flow(self):
        self.registration_borrower_account()
        self.registration_investor_account()
        self.add_bank_account(self.data['investor_account'].get('token'), 5050)
        self.create_loan_request()
        self.create_loan_offer()
        self.accept_loan_offer()
        for i in range(self.data['loan_request']['loan_period']+1):
            self.pay_installments()
        self.check_loan_status()
    def registration_borrower_account(self):
        account_data = {
  "email": "borrower@e.com",
  "first_name": "borrower",
  "last_name": "1",
  "password": "string123",
  "password2": "string123"
}
        response = self.client.post(self.register_borrower_url, account_data, format='json')
        self.assertEqual(response.status_code, 200)
        # add bank account
        self.add_bank_account(response.data.get('token'), 500)
        print('print account data')
        pprint(response.data)
        self.data['borrower_account'] = response.data

    def registration_investor_account(self):
        account_data = {
            "email": "investor@e.com",
            "first_name": "investor",
            "last_name": "1",
            "password": "string123",
            "password2": "string123"
        }
        response = self.client.post(self.register_investor_url, account_data, format='json')
        self.assertEqual(response.status_code, 200)
        # add bank account
        #self.add_bank_account(response.data.get('token'), 5050)
        print('print account data')
        pprint(response.data)
        self.data['investor_account'] = response.data

    def add_bank_account(self, token, balance):

        bank_account_data = {
  "balance": balance,

}
        # add token to headers
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        url = '/api/account/add-bank-account'
        response = self.client.post(url, bank_account_data, format='json')
        self.assertEqual(response.status_code, 200)

        pprint(response.data)


    def create_loan_request(self):

        loan_request_data = {
  "amount": 5000,
  "loan_period": 6,

}
        # add token to headers
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.data['borrower_account'].get('token'))
        url = '/api/borrower/create-request'
        response = self.client.post(url, loan_request_data, format='json')
        self.assertEqual(response.status_code, 200)
        print('print accountloan request response')
        pprint(response.data)
        self.data['loan_request'] = response.data

    def create_loan_offer(self):

        loan_offer_data = {
  "loan_request": self.data['loan_request'].get('id'),
  "annual_interest_rate": 15
}
        # add token to headers
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.data['investor_account'].get('token'))
        url = '/api/investor/create-offer'
        response = self.client.post(url, loan_offer_data, format='json')
        self.assertEqual(response.status_code, 200)
        print('print loan offer  response')
        pprint(response.data)
        self.data['loan_offer'] = response.data

    def accept_loan_offer(self):
        # add token to headers
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.data['borrower_account'].get('token'))
        url = "/api/borrower/accept-offer/" + str(self.data['loan_offer'].get('id'))
        response = self.client.post(url,  format='json')
        print(response)
        self.assertEqual(response.status_code, 200)
        print('print accept loan offer  response')
        pprint(response.data)
        self.data['loan'] = response.data

    def pay_installments(self):
        pay_data = {
  "amount": self.data['loan'].get('monthly_installment'),

  "loan": self.data['loan'].get('id')
}
        # add token to headers
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.data['borrower_account'].get('token'))
        url = '/api/borrower/pay-installment'
        response = self.client.post(url, pay_data, format='json')
        #self.assertEqual(response.status_code, 200)
        print('print loan offer  response')
        pprint(response.data)

    def check_loan_status(self):
        # add token to headers
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.data['investor_account'].get('token'))
        url = '/api/loan/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        print('print loan offer  response')
        pprint(response.data)
        self.data['loan_offer'] = response.data









