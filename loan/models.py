from mysite.shared import TrackingModel
from decimal import Decimal
from .constants import loan_status_choices, lenme_fee
from django.core.validators import MinValueValidator
from django.db import models
from account.models import Account
from borrower.models import LoanRequest
from investor.models import LoanOffer
# Create your models here.
class Loan(TrackingModel):
    loan_status = models.CharField(max_length=15, choices=loan_status_choices, default='funded')
    loan_offer = models.OneToOneField(
        LoanOffer,
        on_delete=models.CASCADE,
    )
    @property
    def monthly_installment(self):
        loan_offer = self.loan_offer
        loan_request = loan_offer.loan_request
        amount = Decimal(loan_request.amount)
        period = Decimal(loan_request.loan_period)
        rate = Decimal(loan_offer.annual_interest_rate)
        installment = amount * (1 + (rate/100) * period/12) /period
        return round(installment,2)

    def save(self, *args, **kwargs):
        if self.id == None:
            loan_offer = self.loan_offer
            loan_request = loan_offer.loan_request
            loan_offer.accepted = True
            loan_request.available = False

            loan_request.save()
            loan_offer.save()
        super(Loan, self).save(*args, **kwargs)





