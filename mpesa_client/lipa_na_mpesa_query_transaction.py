import json

from fastapi import APIRouter, Header, HTTPException
from fastapi import Response, status, BackgroundTasks
from pydantic import BaseModel, validator
from mpesa_client import utils

from mpesa_client import generate_oauth_token
from http_client import Http

from typing import Optional, List, Union
from mpesa_client import settings
from mpesa_client.models import LipaNaMpesaQueryResponse, LipaNaMpesaQueryRequest

router = APIRouter(prefix="/app/v1")

# Initialize MpesaSandboxSettings
sandbox = settings.MpesaSandboxSettings()


# Safaricom Lipa Na Mpesa Query URL:
# https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query

# Define the summary and description for this API:
api_summary = "Lipa na M-Pesa Query End-point"
api_description = "Use this API to check the status of a Lipa Na M-Pesa Online Payment."


# Define a route for generating M-PESA express (STK Push/NI push)
@router.post("/m-pesa/lipa-na-mpesa/query", tags=["Lipa Na M-Pesa"], summary=api_summary, description=api_description,
             response_model=LipaNaMpesaQueryResponse)
async def mpesa_lipa_na_mpesa_query_resource(response: Response, lipa_na_mpesa_checkout_id: str,
                                             user_agent: Union[str, None] = Header(default=None, include_in_schema=False)):
    password = utils.get_encoded_password()
    timestamp = utils.get_transaction_time()
    lipa_na_mpesa_query = LipaNaMpesaQueryRequest(BusinessShortCode=sandbox.lipa_na_mpesa_business_short_code,
                                                  Password=password, Timestamp=timestamp, CheckoutRequestID=lipa_na_mpesa_checkout_id)

    lipa_na_mpesa_query_response = LipaNaMpesaQueryResponse()

    # get a token:
    username = sandbox.lipa_na_mpesa_consumer_key
    password = sandbox.lipa_na_mpesa_consumer_secret

    mpesa_token_response = await generate_oauth_token.mpesa_generate_oauth_token(username, password)

    if mpesa_token_response.success:
        query_lipa_na_mpesa_response = await query_lipa_na_mpesa_payment_status(lipa_na_mpesa_query, mpesa_token_response.access_token)
        lipa_na_mpesa_query_response = query_lipa_na_mpesa_response

        if query_lipa_na_mpesa_response.Success:
            response.status_code = status.HTTP_200_OK
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return lipa_na_mpesa_query_response


async def query_lipa_na_mpesa_payment_status(lipa_na_mpesa_query_request: LipaNaMpesaQueryRequest,
                                             bearer: str) -> LipaNaMpesaQueryResponse:
    lipa_na_mpesa_query_response = LipaNaMpesaQueryResponse()

    # https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query
    server = sandbox.sandbox_url
    lipa_na_mpesa_resource = "mpesa/stkpushquery/v1/"
    lipa_na_mpesa_query_end_point = "query"

    # Create the URL for the stkpush query:
    url = server + lipa_na_mpesa_resource + lipa_na_mpesa_query_end_point

    # Set the headers for the request:
    headers = {"Authorization": f"Bearer {bearer}", "Content-Type": "application/json"}

    param = json.dumps(lipa_na_mpesa_query_request.dict())

    print(f"param: {param}")

    # Make a request to generate the STK Push:
    response = await Http.post(url, headers=headers, data=param)

    print(response)

    if "ResponseCode" in response:
        lipa_na_mpesa_query_response.ResponseCode = response["ResponseCode"]
        lipa_na_mpesa_query_response.ResponseDescription = response["ResponseDescription"]
        lipa_na_mpesa_query_response.CheckoutRequestID = response["CheckoutRequestID"]
        lipa_na_mpesa_query_response.MerchantRequestID = response["MerchantRequestID"]
        lipa_na_mpesa_query_response.ResultDesc = response["ResultDesc"]
        lipa_na_mpesa_query_response.ResultCode = response["ResultCode"]
        lipa_na_mpesa_query_response.Success = True

    if not lipa_na_mpesa_query_response.Success:
        if "errorMessage" in response["response"]:
            # convert the error back to a dict:
            error = json.loads(response["response"])

            error_code = error["errorCode"]
            error_message = error["errorMessage"]

            lipa_na_mpesa_query_response.ResponseDescription = f"{error_code}, {error_message}"

    print(f"lipa_na_mpesa_query_response: {lipa_na_mpesa_query_response}")

    return lipa_na_mpesa_query_response
