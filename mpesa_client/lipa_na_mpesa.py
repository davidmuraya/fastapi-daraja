
import json

from fastapi import APIRouter, Header, HTTPException
from fastapi import Response, status, BackgroundTasks
from pydantic import BaseModel, validator
from mpesa_client import utils

from mpesa_client import generate_oauth_token
import app

from typing import Optional, List, Union
from mpesa_client import settings

router = APIRouter(prefix="/app/v1")

# Initialize MpesaSandboxSettings
sandbox = settings.MpesaSandboxSettings()


# Safaricom Lipa Na Mpesa URL:
# https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest

class LipaNaMpesaRequest(BaseModel):

    BusinessShortCode: str = sandbox.lipa_na_mpesa_business_short_code
    TransactionType: str = "CustomerPayBillOnline"
    Amount: float = 0.00
    PartyA: str = "254708374149"
    PartyB: str = sandbox.lipa_na_mpesa_business_short_code
    PhoneNumber: str = "254720928891"
    CallBackURL: str = sandbox.lipa_na_mpesa_callback_url
    AccountReference: str = "jw101000"
    TransactionDesc: str = "Test"

    # todo validators:
    # encoded_password = validator('Password', allow_reuse=True)(get_encoded_password)
    # time_stamp = validator('Timestamp', allow_reuse=True)(get_transaction_time)


class LipaNaMpesa(BaseModel):

    BusinessShortCode: str = sandbox.lipa_na_mpesa_business_short_code
    Password: str = ""
    Timestamp: str = ""
    TransactionType: str = "CustomerPayBillOnline"
    Amount: float = 0.00
    PartyA: str = "254708374149"
    PartyB: Optional[str]
    PhoneNumber: str = "254720928891"
    CallBackURL: str = sandbox.lipa_na_mpesa_callback_url
    AccountReference: str = "jw101000"
    TransactionDesc: str = "Test"


class LipaNaMpesaResponse(BaseModel):
    MerchantRequestID: str = ""  # "29115-34620561-1",
    CheckoutRequestID: str = ""  # "ws_CO_191220191020363925",
    ResponseCode: str = "-1"  # Default value
    ResponseDescription: str = ""  # "Success. Request accepted for processing",
    CustomerMessage: str = ""  # "Success. Request accepted for processing"
    Success: bool = False


# Define the summary and description for this API:
api_summary = "Lipa na M-Pesa End-point"
api_description = "M-PESA express (STK Push/NI push) is a Merchant/Business initiated C2B (Customer to Business) Payment."


# Define a route for generating M-PESA express (STK Push/NI push)
@router.post("/m-pesa/lipa-na-mpesa", tags=["Lipa Na M-Pesa"], summary=api_summary, description=api_description,
             response_model=LipaNaMpesaResponse)
async def mpesa_lipa_na_mpesa_resource(response: Response, lipa_na_mpesa_request: LipaNaMpesaRequest,
                                       user_agent: Union[str, None] = Header(default=None, include_in_schema=False)):

    lipa_na_mpesa_response_model = LipaNaMpesaResponse()
    lipa_na_mpesa = LipaNaMpesa()
    lipa_na_mpesa.Amount = lipa_na_mpesa_request.Amount
    lipa_na_mpesa.BusinessShortCode = lipa_na_mpesa_request.BusinessShortCode
    lipa_na_mpesa.AccountReference = lipa_na_mpesa_request.AccountReference
    lipa_na_mpesa.CallBackURL = lipa_na_mpesa_request.CallBackURL
    lipa_na_mpesa.PartyA = lipa_na_mpesa_request.PartyA
    lipa_na_mpesa.PartyB = lipa_na_mpesa_request.PartyB
    lipa_na_mpesa.TransactionDesc = lipa_na_mpesa_request.TransactionDesc
    lipa_na_mpesa.TransactionType = lipa_na_mpesa_request.TransactionType

    # requested amount must be greater than 0:
    if lipa_na_mpesa_request.Amount <= 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Amount must be greater than 0")

    # get a token:
    username = sandbox.lipa_na_mpesa_consumer_key
    password = sandbox.lipa_na_mpesa_consumer_secret

    mpesa_token_response = await generate_oauth_token.mpesa_generate_oauth_token(username, password)

    if mpesa_token_response.success:

        lipa_na_mpesa.Password = utils.get_encoded_password()
        lipa_na_mpesa.Timestamp = utils.get_transaction_time()

        lipa_na_mpesa_response = await initiate_lipa_na_mpesa_payment(lipa_na_mpesa, mpesa_token_response.access_token)

        lipa_na_mpesa_response_model = lipa_na_mpesa_response

        if lipa_na_mpesa_response.Success:
            response.status_code = status.HTTP_200_OK
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return lipa_na_mpesa_response_model


async def initiate_lipa_na_mpesa_payment(lipa_na_mpesa_request: LipaNaMpesa, bearer: str):

    lipa_na_mpesa_response = LipaNaMpesaResponse()

    server = sandbox.sandbox_url
    lipa_na_mpesa_resource = "mpesa/stkpush/v1/"
    lipa_na_mpesa_end_point = "processrequest"

    # Create the URL for the stkpush:
    url = server + lipa_na_mpesa_resource + lipa_na_mpesa_end_point

    # Set the headers for the request:
    headers = {"Authorization": f"Bearer {bearer}", "Content-Type": "application/json"}

    param = json.dumps(lipa_na_mpesa_request.dict())

    print(f"param: {param}")

    # Make a request to generate the STK Push:
    response = await app.Http.post(url, headers=headers, data=param)

    print(response)

    if "ResponseCode" in response:
        lipa_na_mpesa_response.ResponseCode = response["ResponseCode"]
        lipa_na_mpesa_response.ResponseDescription = response["ResponseDescription"]
        lipa_na_mpesa_response.CheckoutRequestID = response["CheckoutRequestID"]
        lipa_na_mpesa_response.CustomerMessage = response["CustomerMessage"]
        lipa_na_mpesa_response.MerchantRequestID = response["MerchantRequestID"]
        lipa_na_mpesa_response.Success = True

    if not lipa_na_mpesa_response.Success:
        if "errorMessage" in response["response"]:

            # convert the error back to a dict:
            error = json.loads(response["response"])

            error_code = error["errorCode"]
            error_message = error["errorMessage"]

            lipa_na_mpesa_response.ResponseDescription = f"{error_code}, {error_message}"

    print(f"lipa_na_mpesa_response: {lipa_na_mpesa_response}")
    return lipa_na_mpesa_response
