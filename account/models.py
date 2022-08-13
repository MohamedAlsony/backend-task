from decimal import Decimal
from loan.constants import lenme_fee
from django.core.exceptions import ValidationError
from mysite.shared import TrackingModel
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class MyAccountManager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email:
			raise ValueError('Users must have an email address')


		user = self.model(
			email=self.normalize_email(email),
		)

		user.set_password(password)
		user.save(using=self._db)
		return user


	def create_superuser(self, email, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	email                   = models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= None
	first_name               = models.CharField(max_length=40)
	last_name                = models.CharField(max_length=40)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	#add boolean fields to differentiate between investors and borrowers
	#not the best method
	is_investor				= models.BooleanField(default=False)
	is_borrower				= models.BooleanField(default=False)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	verified                = models.BooleanField(default=False)



	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

#create token for new users
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)

class BankAccount(TrackingModel):
	user = models.OneToOneField(
		Account,

		on_delete=models.CASCADE,
	)
	# currency $ only for simplicity
	balance = models.DecimalField(
		default=0,
		max_digits=12,
		decimal_places=2,
		validators=[MinValueValidator(0)],
	)
	def transfer_to(self ,amount: Decimal, bankaccount):
		if (self.balance + Decimal(lenme_fee)) < amount:
			raise ValidationError(
				{'balance': "no enough balance in bank account"})

		self.balance -= (amount + Decimal(lenme_fee))
		bankaccount.balance += amount
		# transfer lenme_fee to lenme bankaccount
		self.save()
		bankaccount.save()

