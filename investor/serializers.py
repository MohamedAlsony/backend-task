from rest_framework import serializers
from .models import LoanOffer, InvestorTransaction
from borrower.serializers import LoanRequestSerializer

class LoanOfferSerializer(serializers.ModelSerializer):
	loan_request = LoanRequestSerializer( required=False)

	class Meta:
		model = LoanOffer
		fields = '__all__'
		read_only_fields = ['accepted']

class CreateLoanOfferSerializer(serializers.ModelSerializer):

	class Meta:
		model = LoanOffer
		fields = '__all__'
		read_only_fields = ['accepted']

class InvestorTransactionSerializer(serializers.ModelSerializer):
			class Meta:
				model = InvestorTransaction
				fields = '__all__'
