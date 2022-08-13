from rest_framework import serializers
from .models import Loan
from investor.serializers import LoanOfferSerializer
class LoanSerializer(serializers.ModelSerializer):
	loan_offer = LoanOfferSerializer(read_only=True, required=False)
	monthly_installment = serializers.DecimalField( required=False, max_digits=12, decimal_places=2)

	class Meta:
		model = Loan
		fields = '__all__'
		read_only_fields = ['loan_state']
