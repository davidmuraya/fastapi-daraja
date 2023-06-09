
from typing import Union

from fastapi import APIRouter
from fastapi import Response, status, Header

from app.http_client.http import Http
from app.mpesa_client.settings import MpesaSandboxSettings
from app.mpesa_client.models import MpesaTokenResponseModel


# Create an API router
router = APIRouter(prefix="/app/v1")

# Initialize MpesaSandboxSettings
sandbox = MpesaSandboxSettings()


# Set the sandbox URL and endpoint for generating a token
server = sandbox.sandbox_url
oauth_resource = 'oauth/v1/'
token_end_point = "generate?grant_type=client_credentials"


# Define the summary and description for the API
api_summary = "Mpesa Oauth End-point"
api_description = "This API gets a token from the M-Pesa Daraja API. Use this for testing only"


# Define a route for generating Mpesa token
@router.get("/m-pesa/generate-token", tags=["M-pesa Authentication"], summary=api_summary, description=api_description,
            response_model=MpesaTokenResponseModel)
async def mpesa_generate_token_resource(response: Response, username: str, password: str,
                                        user_agent: Union[str, None] = Header(default=None, include_in_schema=False)):

    # Initialize the MpesaTokenResponseModel
    mpesa_token_response_model = MpesaTokenResponseModel()

    # Call the function to generate the Mpesa token
    mpesa_token_response = await mpesa_generate_oauth_token(username=username, password=password)

    # Assign the response to the model
    mpesa_token_response_model = mpesa_token_response

    # Set the HTTP response status code based on the success of the token generation
    if mpesa_token_response.success:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    # Print the user agent header
    print(user_agent)

    return mpesa_token_response_model


# Function to generate Mpesa OAuth token
async def mpesa_generate_oauth_token(username: str, password: str):

    # Create the URL for token generation
    url = server + oauth_resource + token_end_point

    # Set the headers for the request
    headers = {}

    # Make a request to generate the Mpesa token
    response = await Http.get(url, headers=headers, username=username, password=password)

    print(f"token response: {response}")

    # Create a model to store the token response
    mpesa_token_response_model = MpesaTokenResponseModel()

    # Set the values in the model based on the response:
    if "response_status" in response:
        mpesa_token_response_model.error = response["response_status"]

    if "error" in response:
        mpesa_token_response_model.error = response["error"]

    if "access_token" in response:
        mpesa_token_response_model.access_token = response["access_token"]
        mpesa_token_response_model.expires_in = response["expires_in"]
        mpesa_token_response_model.success = True

    print(f"mpesa_token_response_model: {mpesa_token_response_model}")

    return mpesa_token_response_model
