
from loan.constants import lenme_fee
import threading
from investor.models import InvestorTransaction
class InvestorTransactionTask(threading.Thread):
    def __init__(self, loan):
        self.loan = loan

        threading.Thread.__init__(self)

    def run(self):
        investor_transaction = InvestorTransaction.objects.create(
            user=self.loan.loan_offer.user,
            amount=self.loan.loan_offer.loan_request.amount,
            extra_fee = lenme_fee,
            loan=self.loan
        )
        investor_transaction.save()
