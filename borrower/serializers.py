from rest_framework import serializers
from .models import LoanRequest, InstallmentTransaction

class LoanRequestSerializer(serializers.ModelSerializer):

	class Meta:
		model = LoanRequest
		fields = '__all__'
		read_only_fields = ['available']

class InstallmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = InstallmentTransaction
		fields = '__all__'

