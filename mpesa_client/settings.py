from pydantic import BaseModel


class MpesaSandboxSettings(BaseModel):
    """
    Please consider storing these values in a secure location e.g. firestore
    """

    sandbox_url: str = "https://sandbox.safaricom.co.ke/"
    consumer_key: str = "wLs9wxNfPrda0fIy7MUjwWuRWW5xQ8N5"
    consumer_secret: str = "hQowLbqAnrNvQVOI"
    passkey: str = "hQowLbqAnrNvQVOI"
    confirmation_url = ""
    validation_url = ""
    lipa_na_mpesa_callback_url = ""
    lipa_na_mpesa_business_short_code = "200300"


class MpesaProductionSettings(BaseModel):
    production_url: str = "https://sandbox.safaricom.co.ke/"

