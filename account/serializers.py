from rest_framework import serializers
from account.models import Account, BankAccount
class RegistrationSerializer(serializers.ModelSerializer):
	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = Account
		fields = ['email', 'first_name', 'last_name', 'password', 'password2', 'is_investor', 'is_borrower']
		extra_kwargs = {
				'password': {'write_only': True, 'min_length': 8, 'max_length': 50},
		}


	def	save(self) :

		account = Account(
			email=self.validated_data['email'],
			first_name=self.validated_data['first_name'],
			last_name=self.validated_data['last_name'],
			is_borrower=self.validated_data.get('is_borrower', False),
			is_investor=self.validated_data.get('is_investor', False),
				)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		account.set_password(password)
		account.save()
		return account

class BankAccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = BankAccount
		fields = '__all__'