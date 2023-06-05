
from datetime import datetime
import time

from fastapi import APIRouter, Header
from fastapi import Response, status, BackgroundTasks
from pydantic import BaseModel


from typing import Optional, List, Union


router = APIRouter(prefix="/app/v1")


class MpesaRequest(BaseModel):
    TransactionType: str
    TransID: str
    TransTime: str
    TransAmount: float
    BusinessShortCode: str
    BillRefNumber: str
    InvoiceNumber: str
    OrgAccountBalance: float
    ThirdPartyTransID: str
    MSISDN: str
    FirstName: str
    MiddleName: str
    LastName: str


class PaymentValidation(BaseModel):
    ResultCode: str = "0"
    ResultDesc: str = "Accepted"


def some_function(customer_number: str):
    # check if the client is valid here:

    validation_response = {}

    return validation_response


api_summary = "Mpesa Confirmation End-point"
api_description = "This API processes a receipt."


@router.post("/receipts/payment-validation", tags=["Receipts"], summary=api_summary, description=api_description,
             response_model=PaymentValidation)
async def mpesa_validation_resource(background_tasks: BackgroundTasks, response: Response, mpesa_request: MpesaRequest,
                                      user_agent: Union[str, None] = Header(default=None, include_in_schema=False)):

    # log time
    start = time.perf_counter()

    # check transaction time:
    # default date time:
    transaction_date_time = (datetime.today()).strftime('%Y-%m-%d %H:%M')
    transaction_date = (datetime.today()).strftime('%Y-%m-%d')

    try:
        mpesa_request_time = datetime.strptime(mpesa_request.TransTime, "%Y%m%d%H%M%S").date()
        transaction_date_time = mpesa_request_time.strftime('%Y-%m-%d %H:%M')
        transaction_date = mpesa_request_time.strftime('%Y-%m-%d')

    except ValueError as e:
        error_on_date_conversion = f"M-Pesa Date conversion error: Date:{mpesa_request.TransTime} does not conform to %d %b %Y"

    payment_validation = PaymentValidation()

    # check if request invoice number is numeric:
    if mpesa_request.InvoiceNumber.isnumeric():

        # try and convert to int:
        id = int(mpesa_request.InvoiceNumber)

        # do further validation with id above here:

        # upon failure:
        payment_validation.ResultCode = "C2B00012"
        payment_validation.ResultDesc = "Invalid Account Number"
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:

        # value supplied was not an integer
        # do further validation:
        policy_number_check_response = some_function(mpesa_request.InvoiceNumber)

        if policy_number_check_response.success:

            response.status_code = status.HTTP_200_OK

        else:
            # it is alphanumeric but a valid client was not found was not found:

            payment_validation.ResultCode = "C2B00012"
            payment_validation.ResultDesc = "Invalid Account Number"
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    # performance monitoring
    request_time = time.perf_counter() - start

    return payment_validation


"""
Other Result Error Codes
ResultCode ResultDesc
C2B00011 Invalid MSISDN
C2B00012 Invalid Account Number
C2B00013 Invalid Amount
C2B00014 Invalid KYC Details
C2B00015 Invalid Shortcode
C2B00016 Other Error
"""