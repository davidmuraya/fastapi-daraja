
from pydantic import BaseModel
from typing import Optional, List, Union
from mpesa_client import settings

# Initialize MpesaSandboxSettings
sandbox = settings.MpesaSandboxSettings()


# Define the response model for Mpesa token
class MpesaTokenResponseModel(BaseModel):
    access_token: str = ""
    expires_in: int = 0
    success: bool = False
    error: Optional[str]


# Lipa Na Mpesa Models:
class LipaNaMpesaQueryRequest(BaseModel):
    BusinessShortCode: str  # ": "174379",
    Password: str  # ": "MTc0Mzc5YmZiMjc5TliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMTYwMjE2MTY1NjI3",
    Timestamp: str  # ": "20160216165627",
    CheckoutRequestID: str  # "ws_CO_260520211133524545",


class LipaNaMpesaQueryResponse(BaseModel):
    ResponseCode: str = ""  # ": "0",
    ResponseDescription: str = ""  # ": "The service request has been accepted successsfully",
    MerchantRequestID: str = ""  # ": "100914-5655540-2",
    CheckoutRequestID: str = ""  # ": "ws_CO_23062023170648877720928891",
    ResultCode: str = ""  # "1032",
    ResultDesc: str = ""  # "Request cancelled by user"
    Success: bool = False


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

