from django.db.models import Q
from rest_framework.authentication import TokenAuthentication

from rest_framework import status
from account.models import Account
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GetLoanAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LoanSerializer

    @swagger_auto_schema(
    operation_description="api to show all my loans",
     responses={200: LoanSerializer, 400 : 'Bad Request'})

    def get(self, request, *args, **kwargs):
        queryset = Loan.objects.select_related('loan_offer', 'loan_offer__loan_request').filter(
            Q(loan_offer__user_id=request.user.id) | Q(loan_offer__loan_request__user_id=request.user.id)
        )
        serializer = self.serializer_class(queryset, many=True)
        return  Response(serializer.data)


