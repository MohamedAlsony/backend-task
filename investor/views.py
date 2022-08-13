from rest_framework.authentication import TokenAuthentication

from rest_framework import status
from account.models import Account
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GetOffersAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LoanOfferSerializer

    @swagger_auto_schema(
    operation_description="api to show my loan offers",
     responses={200: LoanOfferSerializer, 400 : 'Bad Request'})

    def get(self, request, *args, **kwargs):
        queryset = LoanOffer.objects.filter(user_id=request.user.id)
        serializer = self.serializer_class(queryset, many=True)
        return  Response(serializer.data)


class CreateOffersAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateLoanOfferSerializer

    @swagger_auto_schema(
        operation_description="api to create loan Offer",
        request_body=LoanOfferSerializer,
        responses={200: LoanOfferSerializer, 400: 'Bad Request'})
    def post(self, request, *args, **kwargs):

        if request.user.is_borrower:
            context = {'response': 'error', 'error_msg': 'not allowed'}
            return Response(context, status=status.HTTP_403_FORBIDDEN)
        #bank_account = getattr(request.user, 'bankaccount', None)
        #if not bank_account:
            #context = {'response': 'error', 'error_msg': 'this investor has no bankaccount'}
            #return Response(context, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



