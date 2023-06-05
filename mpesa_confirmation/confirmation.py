
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


class PaymentConfirmation(BaseModel):
    receipt_id: Optional[int]
    success: bool = False
    errors: Optional[List[str]]


class PaymentConfirmationResponse(BaseModel):
    ResultCode: str = "0"
    ResultDesc: str = "Accepted"


def create_receipt(mpesa_request: MpesaRequest, transaction_date: str):

    # perform system related events here e.g. create the receipt:

    receipt = {}

    return receipt


api_summary = "Mpesa Confirmation End-point"
api_description = "This API processes a receipt."


@router.post("/receipts/payment-confirmation", tags=["Receipts"], summary=api_summary, description=api_description,
             response_model=PaymentConfirmation)
async def mpesa_confirmation_resource(background_tasks: BackgroundTasks, response: Response, mpesa_request: MpesaRequest,
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

    payment_confirmation = PaymentConfirmation()

    # check if request invoice number is numeric:
    if mpesa_request.InvoiceNumber.isnumeric():
        # do validation here:
        pass

    else:

        # value supplied was not an integer, do alphanumeric validation here:

        # add receipting creation code:
        # create the receipt object:
        receipt = create_receipt(mpesa_request, transaction_date)

    # performance monitoring
    request_time = time.perf_counter() - start

    return payment_confirmation
