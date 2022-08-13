from decimal import Decimal
from loan.constants import lenme_fee
from django.core.exceptions import ValidationError
from mysite.shared import TrackingModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from account.models import Account
from borrower.models import LoanRequest
# Create your models here.

class LoanOffer(TrackingModel):
    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
    )
    loan_request = models.OneToOneField(
        LoanRequest,
        on_delete=models.CASCADE,
    )
    annual_interest_rate = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        decimal_places=2,
        max_digits=5,
        help_text='Interest rate from 0 - 100'
    )
    accepted = models.BooleanField(default=False)

class InvestorTransaction(TrackingModel):
    user = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
    )

    loan = models.OneToOneField(
        'loan.Loan',
        on_delete=models.CASCADE,
    )
    # currency $ only for simplicity
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    # currency $ only for simplicity
    extra_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    def clean(self):
        if (self.amount + self.extra_fee) > self.user.bankaccount.balance:
            raise ValidationError(
                {'amount': "no enough balance in bank account"})

    def save(self, *args, **kwargs):
        if self.id == None:
            loan = self.loan
            loan.loan_offer.user.bankaccount.transfer_to(self.amount + self.extra_fee, loan.loan_offer.loan_request.user.bankaccount)
        super(InvestorTransaction, self).save(*args, **kwargs)




