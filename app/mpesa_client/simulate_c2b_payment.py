
import json

from fastapi import APIRouter, Header
from fastapi import Response, status
from pydantic import BaseModel

from app.mpesa_client import generate_oauth_token
from app.mpesa_client.settings import MpesaSandboxSettings
from app.http_client.http import Http

from typing import Union


router = APIRouter(prefix="/app/v1")

# Initialize MpesaSandboxSettings
sandbox = MpesaSandboxSettings()

# Safaricom Paybill Mpesa URL:
# https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate


class SimulateC2BMpesaRequest(BaseModel):
    ShortCode: str = "600700"
    CommandID: str = "CustomerPayBillOnline"
    Amount: str = "20000"
    Msisdn: str = "254720928891"
    BillRefNumber: str = "test"


class C2BMpesaResponse(BaseModel):
    MerchantRequestID: str = ""  # "29115-34620561-1",
    CheckoutRequestID: str = ""  # "ws_CO_191220191020363925",
    ResponseCode: str = "0"
    ResponseDescription: str = ""  # "Success. Request accepted for processing",
    CustomerMessage: str = ""  # "Success. Request accepted for processing"


# Define the summary and description for this API:
api_summary = "Simulate C2B Payment (Paybill)"
api_description = "Simulate a Customer to Business (C2B) Request"


@router.post("/m-pesa/simulate-paybill-request", tags=["Paybill, C2B"], summary=api_summary, description=api_description,
             response_model=C2BMpesaResponse)
async def mpesa_simulate_paybill_request_resource(response: Response, c2b_mpesa_request: SimulateC2BMpesaRequest,
                                                  user_agent: Union[str, None] = Header(default=None, include_in_schema=False)):

    c2b_response_model = C2BMpesaResponse()

    # get a token:
    username = sandbox.c2b_consumer_key
    password = sandbox.c2b_consumer_secret

    mpesa_token_response = await generate_oauth_token.mpesa_generate_oauth_token(username, password)

    if mpesa_token_response.success:
        lipa_na_mpesa_response = await simulate_c2b_mpesa_request(c2b_mpesa_request, mpesa_token_response.access_token)
        if lipa_na_mpesa_response.ResponseCode == "0":
            #  add logic here
            response.status_code = status.HTTP_200_OK
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return c2b_response_model


async def simulate_c2b_mpesa_request(c2b_mpesa_request: SimulateC2BMpesaRequest, bearer: str):

    c2b_mpesa_response = C2BMpesaResponse()

    server = sandbox.sandbox_url
    c2b_mpesa_resource = "/mpesa/c2b/v1/"
    c2b_mpesa_end_point = "simulate"

    # Create the URL for token generation
    url = server + c2b_mpesa_resource + c2b_mpesa_end_point

    # Set the headers for the request
    headers = {"Authorization": f"Bearer {bearer}", "Content-Type": "application/json"}

    param = json.dumps(c2b_mpesa_request.dict())

    print(param)

    # Make a request to simulate the paybill payment:
    response = await Http.post(url, headers=headers, data=param)

    print(response)

    if "errorMessage" in response:
        c2b_mpesa_response.ResponseDescription = response["errorMessage"]

    return c2b_mpesa_response
