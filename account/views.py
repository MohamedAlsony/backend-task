from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from account.models import Account
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from account.serializers import RegistrationSerializer, BankAccountSerializer

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Register API
class RegisterAPI(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegistrationSerializer
    account_type = None
    @swagger_auto_schema(
    operation_description="api to register new account",
    request_body=openapi.Schema(
     type=openapi.TYPE_OBJECT,
     properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING , description='email', default='example@example.com'),
		'first_name': openapi.Schema(type=openapi.TYPE_STRING , description='firstname'),
		'last_name': openapi.Schema(type=openapi.TYPE_STRING , description='lastname'),
        'password': openapi.Schema(type=openapi.TYPE_STRING  , description='password'),
        'password2': openapi.Schema(type=openapi.TYPE_STRING  , description='re-enter the password')
     }),
     responses={200: RegistrationSerializer, 400 : 'Bad Request'})

    def post(self, request, *args, **kwargs):
        context = {}
        data = {**request.data, **self.set_account_type()}
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            #if valid save object and send response
            account = serializer.save()
            context = serializer.data.copy()
            context['token'] = account.auth_token.key
            context['response'] = 'success'
            return Response(data=context)


        #if not valid return error
        context = serializer.errors.copy()
        context['response'] = 'error'
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)

    def set_account_type(self) -> dict:
        data = dict()
        if self.account_type == 'investor':
            data['is_investor'] = True
        else:
            data['is_borrower'] = True
        return data


class AddBankAccount(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BankAccountSerializer

    @swagger_auto_schema(
        operation_description="api to add bank account to the user",
        request_body=BankAccountSerializer,
        responses={200: BankAccountSerializer, 400: 'Bad Request'})
    def post(self, request, *args, **kwargs):

        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


