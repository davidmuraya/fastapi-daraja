import app
from typing import Optional, List, Union


from fastapi import APIRouter

from fastapi import Depends, Response, status, HTTPException, Header
from pydantic import BaseModel

from mpesa_client import settings


router = APIRouter(prefix="/app/v1")

# https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials

sandbox = settings.MpesaSandboxSettings()

server = sandbox.sandbox_url
oauth_resource = 'oauth/v1/'
token_end_point = "generate?grant_type=client_credentials"


class MpesaTokenResponseModel(BaseModel):
    access_token: str = ""
    expires_in: int = 0
    success: bool = False
    error: Optional[str]


api_summary = "Mpesa Oauth End-point"
api_description = "This API processes a receipt."


@router.get("/m-pesa/generate-token", tags=["M-pesa Authentication"], summary=api_summary, description=api_description,
            response_model=MpesaTokenResponseModel)
async def mpesa_generate_token_resource(response: Response, username: str, password: str,
                                        user_agent: Union[str, None] = Header(default=None, include_in_schema=False)):

    mpesa_token_response_model = MpesaTokenResponseModel()
    mpesa_token_response = await mpesa_generate_oauth_token(username=username, password=password)

    mpesa_token_response_model = mpesa_token_response

    if mpesa_token_response.success:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    print(user_agent)

    return mpesa_token_response_model


async def mpesa_generate_oauth_token(username: str, password: str):

    url = server + oauth_resource + token_end_point

    headers = {}

    response = await app.Http.get(url, headers=headers, username=username, password=password)

    print(response)

    # set the values:
    mpesa_token_response_model = MpesaTokenResponseModel()

    if "response_status" in response:
        mpesa_token_response_model.error = response["response_status"]

    if "error" in response:
        mpesa_token_response_model.error = response["error"]

    if "access_token" in response:
        mpesa_token_response_model.access_token = response["access_token"]
        mpesa_token_response_model.expires_in = response["expires_in"]
        mpesa_token_response_model.success = True

    return mpesa_token_response_model
