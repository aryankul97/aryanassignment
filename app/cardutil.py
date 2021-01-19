from rest_framework.response import Response
from rest_framework import status
from itertools import groupby
import re
import uuid
import datetime

def check_credit_card(card_number):
    pattern = re.compile(r'(?:\d{4}-){3}\d{4}|\d{16}')
    num = str(card_number)
    if pattern.fullmatch(num):
        return True
    else:
        return False

def check_validations(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount):
    if CreditCardNumber is None:
        content = {'msg': 'Credit Card Number is Mandatory'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif CardHolder is None:
        content = {'msg': 'Card Holder Name is Mandatory'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif ExpirationDate is None:
        content = {'msg': 'Expiration Date is Mandatory'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif Amount is None:
        content = {'msg': 'Amount is Mandatory'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif len(str(SecurityCode)) > 3:
        content = {'msg': 'Security Code cannot be greater than 3 digits.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif float(Amount) < 0:
        content = {'msg': 'Amount cannot be less than 0.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif ExpirationDate.date() < datetime.date.today():
        content = {'msg': 'Invalid Expiration Date'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif not check_credit_card(CreditCardNumber):
        content = {'msg': 'Invalid Credit Card Number'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        return True

#Following are the examples of payment gateway functions, just for testing purpose

def CheapPaymentGateway(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount):
    try:
        complete_str = str(datetime.datetime.now()) + str(CardHolder) + str(CreditCardNumber) + str(ExpirationDate) + str(SecurityCode) + str(Amount)
        content = {'paymentgateway':'Cheap Payment Gateway', 'msg':'Payment Processed', 'transaction_id':str(uuid.uuid5(uuid.NAMESPACE_DNS, complete_str))}
        return Response(content, status=status.HTTP_200_OK)
    except:
        return False

def ExpensivePaymentGateway(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount):
    try:
        complete_str = str(datetime.datetime.now()) + str(CardHolder) + str(CreditCardNumber) + str(ExpirationDate) + str(SecurityCode) + str(Amount)
        content = {'paymentgateway':'Expensive Payment Gateway', 'msg':'Payment Processed', 'transaction_id':str(uuid.uuid5(uuid.NAMESPACE_DNS, complete_str))}
        return Response(content, status=status.HTTP_200_OK)
    except:
        return False

def PremiumPaymentGateway(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount):
    try:
        complete_str = str(datetime.datetime.now()) + str(CardHolder) + str(CreditCardNumber) + str(ExpirationDate) + str(SecurityCode) + str(Amount)
        content = {'paymentgateway':'Premium Payment Gateway', 'msg':'Payment Processed', 'transaction_id':str(uuid.uuid5(uuid.NAMESPACE_DNS, complete_str))}
        return Response(content, status=status.HTTP_200_OK)
    except:
        return False