from mysite.tasks import InvestorTransactionTask
from loan.serializers import LoanSerializer
from loan.models import Loan
from investor.models import LoanOffer
from investor.serializers import LoanOfferSerializer
from rest_framework.authentication import TokenAuthentication

from rest_framework import status
from account.models import Account
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GetRequestsAPI(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoanRequestSerializer

    @swagger_auto_schema(
    operation_description="api to show all available loan requests",
     responses={200: LoanRequestSerializer, 400 : 'Bad Request'})

    def get(self, request, *args, **kwargs):
        queryset = LoanRequest.objects.filter(available=True)
        serializer = self.serializer_class(queryset, many=True)
        return  Response(serializer.data)


class CreateRequestsAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LoanRequestSerializer

    @swagger_auto_schema(
        operation_description="api to create loan request",
        request_body=LoanRequestSerializer,
        responses={200: LoanRequestSerializer, 400: 'Bad Request'})
    def post(self, request, *args, **kwargs):

        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetRequestOfferAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LoanOfferSerializer

    @swagger_auto_schema(
    operation_description="api to show all available loan request offers",
     responses={200: LoanOfferSerializer, 400 : 'Bad Request'})

    def get(self, request,loan_request_id ,*args, **kwargs):
        queryset = LoanOffer.objects.select_related('loan_request').filter(accepted=False, loan_request_id=loan_request_id)
        serializer = self.serializer_class(queryset, many=True)
        return  Response(serializer.data)

class AcceptOfferAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LoanSerializer

    @swagger_auto_schema(
    operation_description="api to accept offer",
     responses={200: LoanSerializer, 400 : 'Bad Request'})

    def post(self, request,loan_offer_id ,*args, **kwargs):
        print('zzz')
        print(loan_offer_id)
        loan_offer = LoanOffer.objects.select_related('loan_request').filter(accepted=False, id=loan_offer_id, loan_request__available=True, loan_request__user_id=request.user.id).first()
        loan_request = getattr(loan_offer, 'loan_request', None)
        #if not loan_request:
            #return Response({'response':'error'}, status=status.HTTP_404_NOT_FOUND)
        loan = Loan.objects.create(loan_offer=loan_offer)
        loan.save()
        InvestorTransactionTask(loan).start()
        serializer = self.serializer_class(loan)
        return  Response(serializer.data)

class PayInstallmentAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InstallmentSerializer

    @swagger_auto_schema(
        operation_description="api to pay installments",
        request_body=InstallmentSerializer,
        responses={200: InstallmentSerializer, 400: 'Bad Request'})
    def post(self, request, *args, **kwargs):

        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





