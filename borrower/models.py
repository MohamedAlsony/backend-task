from datetime import timedelta
from django.core.exceptions import ValidationError
from mysite.shared import TrackingModel
from django.core.validators import MinValueValidator
from django.db import models
from account.models import Account
# Create your models here.

class LoanRequest(TrackingModel):
    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
    )
    # currency $ only for simplicity
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    # loan period in months
    loan_period = models.PositiveSmallIntegerField(default=0)
    available = models.BooleanField(default=True)

class InstallmentTransaction(TrackingModel):
    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
    )

    loan = models.ForeignKey(
        'loan.Loan',
        on_delete=models.CASCADE,
    )
    # currency $ only for simplicity
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    @property
    def passed(self):
        if self.amount >= self.loan.monthly_installment:
            return True
        return False

    @property
    def deadline(self):
        cls = self.__class__
        last_installment = cls.objects.filter(user_id=self.user_id).last()
        if not last_installment:
            date = self.loan.created_at
        else:
            date = max(self.created_at, self.loan.created_at)
        return date + timedelta(days=30)



    def clean(self):
        if self.amount > self.user.bankaccount.balance:
            raise ValidationError(
                {'amount': "no enough balance in bank account"})

    def save(self, *args, **kwargs):
        loan = self.loan
        cls = self.__class__
        installments = cls.objects.only('amount').values_list('amount', flat=True)
        monthly_installment = loan.monthly_installment
        if sum(installments) < (monthly_installment * loan.loan_offer.loan_request.loan_period):
            loan.loan_offer.loan_request.user.bankaccount.transfer_to(monthly_installment,
                loan.loan_offer.user.bankaccount)
        else:
            loan.loan_status = 'completed'
            loan.save()
        super(InstallmentTransaction, self).save(*args, **kwargs)



