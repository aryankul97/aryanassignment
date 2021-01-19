from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
import datetime
from app.cardutil import *

@csrf_exempt
@api_view(["POST"])
def ProcessPayment(request):
#    try:
        data = request.data
        CreditCardNumber = data['CreditCardNumber']
        CardHolder = data['CardHolder']
        ExpirationDate = data['ExpirationDate']
        SecurityCode = data['SecurityCode']
        Amount = data['Amount']
        ExpirationDate = datetime.datetime.strptime(ExpirationDate, '%d/%m/%y')
        print(CreditCardNumber)
        content = {}
        if check_validations(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount):
            Amount = float(Amount)
            if Amount <= 20.0:
                return CheapPaymentGateway(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount)
            elif Amount > 20.0 and Amount <= 500.0:
                try:
                    return ExpensivePaymentGateway(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount)
                except:
                    for x in range(0, 1):
                        pay = CheapPaymentGateway(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount)
                        if not pay:
                            return CheapPaymentGateway(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount)
                    content = {'msg':'Internal Server Error'}
                    return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif Amount > 500.0:
                try:
                    return PremiumPaymentGateway(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount)
                except:
                    for x in range(0,5):
                        pay = CheapPaymentGateway(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount)
                        if not pay:
                            return CheapPaymentGateway(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount)
                    content = {'msg':'Internal Server Error'}
                    return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                content = {'msg':'Internal Server Error'}
                return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return check_validations(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount)
#    except:
#        content = {'msg':'Internal Server Error'}
#        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)