from pydantic import BaseModel
from dotenv import dotenv_values

config = dotenv_values(".env")


class MpesaSandboxSettings(BaseModel):
    """
    Please consider storing these values in a secure location e.g. firestore
    populate a .env file with the following values:
    # M-Pesa Sandbox Settings:
        C2B_CONSUMER_KEY=""
        C2B_CONSUMER_SECRET=""
        LIPA_NA_MPESA_CONSUMER_KEY=""
        LIPA_NA_MPESA_CONSUMER_SECRET=""
        LIPA_NA_MPESA_PASSKEY=""
        C2B_CONFIRMATION_URL=""
        C2B_VALIDATION_URL=""
        LIPA_NA_MPESA_CALLBACK_URL=""
        LIPA_NA_MPESA_BUSINESS_SHORT_CODE=""

    """

    sandbox_url: str = "https://sandbox.safaricom.co.ke/"
    c2b_consumer_key: str = config.get("C2B_CONSUMER_KEY")
    c2b_consumer_secret: str = config.get("C2B_CONSUMER_SECRET")
    lipa_na_mpesa_consumer_key: str = config.get("LIPA_NA_MPESA_CONSUMER_KEY")
    lipa_na_mpesa_consumer_secret: str = config.get("LIPA_NA_MPESA_CONSUMER_SECRET")
    lipa_na_mpesa_passkey: str = config.get("LIPA_NA_MPESA_PASSKEY")
    c2b_confirmation_url: str = config.get("C2B_CONFIRMATION_URL")
    c2b_validation_url: str = config.get("C2B_VALIDATION_URL")
    lipa_na_mpesa_callback_url: str = config.get("LIPA_NA_MPESA_CALLBACK_URL")
    lipa_na_mpesa_business_short_code: str = config.get("LIPA_NA_MPESA_BUSINESS_SHORT_CODE")


class MpesaProductionSettings(BaseModel):
    production_url: str = "https://sandbox.safaricom.co.ke/"

